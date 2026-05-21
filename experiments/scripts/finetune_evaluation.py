"""
Experiment 7: Fine-tuned vs Base Model Evaluation
Compare LoRA fine-tuned Qwen2.5-7B with the base model using GPT-as-Judge.
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


def load_base_model():
    """Load base Qwen2.5-7B model."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"Loading base model from {config.LLM_MODEL_PATH}...")
    tokenizer = AutoTokenizer.from_pretrained(config.LLM_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_PATH, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )
    return model, tokenizer


def load_finetuned_model(lora_path: str):
    """Load LoRA fine-tuned model."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    print(f"Loading base model for LoRA merge...")
    tokenizer = AutoTokenizer.from_pretrained(config.LLM_MODEL_PATH, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_PATH, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )

    print(f"Loading LoRA weights from {lora_path}...")
    model = PeftModel.from_pretrained(base_model, lora_path)
    model = model.merge_and_unload()  # Merge LoRA into base for faster inference
    print("LoRA merged successfully.")
    return model, tokenizer


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


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lora-path", default="experiments/models/qwen2.5-7b-lora/final")
    parser.add_argument("--output", "-o", default="experiments/results/finetune_comparison.csv")
    parser.add_argument("--sample", "-s", type=int, default=50)
    parser.add_argument("--token", "-t", default=None, help="HuggingFace token for judge")
    args = parser.parse_args()

    # Get HF token
    token = args.token or os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")

    # Load test questions
    test_data = load_test_questions(sample=args.sample)
    print(f"Loaded {len(test_data)} test questions")

    # Load both models
    base_model, base_tokenizer = load_base_model()
    ft_model, ft_tokenizer = load_finetuned_model(args.lora_path)

    # Generate responses from both models
    results = []
    for i, item in enumerate(test_data):
        q = item["question"]
        ref = item.get("reference_answer", "")
        print(f"[{i+1}/{len(test_data)}] {q[:50]}...")

        # Base model response
        base_resp = generate_response(base_model, base_tokenizer, q)
        print(f"  Base: {len(base_resp)} chars")

        # Fine-tuned model response
        ft_resp = generate_response(ft_model, ft_tokenizer, q)
        print(f"  Fine-tuned: {len(ft_resp)} chars")

        results.append({
            "question_id": i,
            "question": q,
            "reference_answer": ref,
            "base_response": base_resp,
            "finetuned_response": ft_resp,
        })

    # Free GPU memory
    del base_model, ft_model
    torch.cuda.empty_cache()

    # Save responses
    df = pd.DataFrame(results)
    responses_path = args.output.replace(".csv", "_responses.csv")
    df.to_csv(responses_path, index=False, encoding="utf-8-sig")
    print(f"Responses saved to {responses_path}")

    # Judge both with GPT-as-Judge
    if not token:
        print("No HF token provided, skipping GPT-as-Judge evaluation.")
        print("Set HUGGINGFACE_TOKEN env var or use --token flag.")
        return

    print("\nStarting GPT-as-Judge evaluation...")
    judge_results = []
    for idx, row in df.iterrows():
        q = row["question"]
        ref = row["reference_answer"]
        print(f"[{idx+1}/{len(df)}] Judging: {q[:50]}...")

        # Judge base
        base_prompt = JUDGE_PROMPT.format(
            question=q, reference_answer=ref, system_response=row["base_response"][:1500]
        )
        base_scores = parse_judge_scores(call_hf_inference(base_prompt, token=token))
        time.sleep(2)

        # Judge fine-tuned
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

        print(f"  Base: {base_scores['overall']:.2f} | Fine-tuned: {ft_scores['overall']:.2f}")

    # Save and summarize
    judge_df = pd.DataFrame(judge_results)
    judge_df.to_csv(args.output, index=False, encoding="utf-8-sig")

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
