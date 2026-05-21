"""
Experiment 7: Fine-tuned vs Base Model Evaluation
Compare LoRA fine-tuned Qwen2.5-7B with the base model using GPT-as-Judge.
Loads one model at a time to avoid OOM.
"""

import json
import os
import sys
import time
import torch
import pandas as pd
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config
from gpt_judge_evaluation import call_hf_inference, parse_judge_scores, JUDGE_PROMPT

TUTOR_SYSTEM_PROMPT = "You are an expert programming tutor. Explain concepts clearly with examples, use step-by-step reasoning, and encourage learning."


def generate_response(model, tokenizer, question: str, max_tokens: int = 1024) -> str:
    """Generate a response using the model."""
    messages = [
        {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1,
        )

    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated_ids, skip_special_tokens=True).strip()


def load_test_questions(filepath: str = "experiments/data/test_questions.json", sample: int = 50):
    """Load test questions."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[:sample]


def generate_all_responses(model, tokenizer, test_data, label: str):
    """Generate responses for all test questions."""
    results = []
    for i, item in enumerate(test_data):
        q = item["question"]
        print(f"  [{i+1}/{len(test_data)}] {q[:50]}...")
        resp = generate_response(model, tokenizer, q)
        print(f"    -> {len(resp)} chars")
        results.append({
            "question_id": i,
            "question": q,
            "reference_answer": item.get("reference_answer", ""),
            f"{label}_response": resp,
        })
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lora-path", default="experiments/models/qwen2.5-7b-lora/final")
    parser.add_argument("--output", "-o", default="experiments/results/finetune_comparison.csv")
    parser.add_argument("--sample", "-s", type=int, default=50)
    parser.add_argument("--token", "-t", default=None, help="HuggingFace token for judge")
    args = parser.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    token = args.token or os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")

    test_data = load_test_questions(sample=args.sample)
    print(f"Loaded {len(test_data)} test questions")

    # --- Phase 1: Generate base model responses ---
    print("\n=== Phase 1: Base Model ===")
    tokenizer = AutoTokenizer.from_pretrained(config.LLM_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_PATH, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )
    base_results = generate_all_responses(model, tokenizer, test_data, "base")

    # Free base model
    del model
    torch.cuda.empty_cache()
    time.sleep(5)

    # --- Phase 2: Generate fine-tuned model responses ---
    print("\n=== Phase 2: Fine-tuned Model ===")
    base_model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_PATH, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )
    print(f"Loading LoRA from {args.lora_path}...")
    ft_model = PeftModel.from_pretrained(base_model, args.lora_path)
    ft_model = ft_model.merge_and_unload()
    print("LoRA merged.")

    ft_results = generate_all_responses(ft_model, tokenizer, test_data, "finetuned")

    del ft_model
    torch.cuda.empty_cache()

    # --- Merge results ---
    merged = []
    for br, fr in zip(base_results, ft_results):
        merged.append({**br, "finetuned_response": fr["finetuned_response"]})

    df = pd.DataFrame(merged)
    responses_path = args.output.replace(".csv", "_responses.csv")
    df.to_csv(responses_path, index=False, encoding="utf-8-sig")
    print(f"\nResponses saved to {responses_path}")

    # --- Phase 3: GPT-as-Judge ---
    if not token:
        print("No HF token, skipping judge. Set HUGGINGFACE_TOKEN or use --token.")
        return

    print("\n=== Phase 3: GPT-as-Judge ===")
    judge_results = []
    for idx, row in df.iterrows():
        q = row["question"]
        ref = row["reference_answer"]
        print(f"[{idx+1}/{len(df)}] Judging: {q[:50]}...")

        base_prompt = JUDGE_PROMPT.format(
            question=q, reference_answer=ref, system_response=row["base_response"][:1500]
        )
        base_scores = parse_judge_scores(call_hf_inference(base_prompt, token=token))
        time.sleep(2)

        ft_prompt = JUDGE_PROMPT.format(
            question=q, reference_answer=ref, system_response=row["finetuned_response"][:1500]
        )
        ft_scores = parse_judge_scores(call_hf_inference(ft_prompt, token=token))
        time.sleep(2)

        judge_results.append({
            "question_id": row["question_id"],
            "question": q,
            "base_accuracy": base_scores["accuracy"],
            "base_clarity": base_scores["clarity"],
            "base_educational": base_scores["educational_value"],
            "base_completeness": base_scores["completeness"],
            "base_overall": base_scores["overall"],
            "ft_accuracy": ft_scores["accuracy"],
            "ft_clarity": ft_scores["clarity"],
            "ft_educational": ft_scores["educational_value"],
            "ft_completeness": ft_scores["completeness"],
            "ft_overall": ft_scores["overall"],
        })
        print(f"  Base: {base_scores['overall']:.2f} | FT: {ft_scores['overall']:.2f}")

    judge_df = pd.DataFrame(judge_results)
    judge_df.to_csv(args.output, index=False, encoding="utf-8-sig")

    # Summary
    print("\n" + "=" * 60)
    print("FINE-TUNED vs BASE MODEL COMPARISON")
    print("=" * 60)
    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    print(f"{'Metric':<20} {'Base':>10} {'Fine-tuned':>10} {'Diff':>10} {'Winner':>10}")
    print("-" * 60)
    for m in metrics:
        base_mean = judge_df[f"base_{m}"].mean()
        ft_mean = judge_df[f"ft_{m}"].mean()
        diff = ft_mean - base_mean
        winner = "Fine-tuned" if diff > 0 else ("Base" if diff < 0 else "Tie")
        print(f"{m:<20} {base_mean:>10.2f} {ft_mean:>10.2f} {diff:>+10.2f} {winner:>10}")

    print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
