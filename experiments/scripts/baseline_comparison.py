"""
Experiment 5: Baseline Comparison
Compare full CodeTutor-ITS system vs raw LLM (no tutoring features).
Generates baseline responses and evaluates both with GPT-as-Judge.
"""

import json
import os
import sys
import time
import pandas as pd
from typing import Dict, List, Optional

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Simple baseline prompt - just answer the question directly
BASELINE_SYSTEM_PROMPT = "You are a helpful programming assistant. Answer the student's question clearly and concisely."

# Import judge evaluation
from gpt_judge_evaluation import call_hf_inference, parse_judge_scores, JUDGE_PROMPT


def load_test_dataset(filepath: str) -> List[Dict]:
    """Load test dataset from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_baseline_via_api(question: str, session_id: str = "baseline") -> str:
    """Generate baseline response by calling the backend API with baseline mode."""
    import httpx
    try:
        with httpx.Client(timeout=120.0) as client:
            # Use a special session prefix to trigger baseline mode
            response = client.post(
                "http://localhost:8000/api/tutor/chat",
                json={
                    "message": question,
                    "session_id": f"baseline_{session_id}",
                    "mode": "baseline",  # Will be handled by backend
                    "programming_language": "python",
                },
            )
            response.raise_for_status()
            return response.json().get("response", "")
    except Exception as e:
        print(f"  API error: {e}")
        return ""


def generate_baseline_direct(question: str, model_path: str) -> str:
    """Generate baseline response directly using transformers (no tutoring features)."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # Load model (cached after first call)
    if not hasattr(generate_baseline_direct, "_model"):
        print(f"Loading model from {model_path}...")
        generate_baseline_direct._tokenizer = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True
        )
        generate_baseline_direct._model = AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
        )
        print("Model loaded.")

    tokenizer = generate_baseline_direct._tokenizer
    model = generate_baseline_direct._model

    messages = [
        {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=2048,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1,
        )

    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated_ids, skip_special_tokens=True).strip()


def generate_baselines(
    test_path: str = "experiments/data/test_questions.json",
    output_path: str = "experiments/results/baseline_responses.csv",
    method: str = "api",
    model_path: str = None,
    sample_size: int = 50,
):
    """Generate baseline responses for all test questions."""

    test_data = load_test_dataset(test_path)
    if sample_size:
        test_data = test_data[:sample_size]

    print(f"Generating baseline responses for {len(test_data)} questions...")
    print(f"Method: {method}")
    print("=" * 60)

    results = []
    for i, item in enumerate(test_data):
        question = item["question"]
        print(f"[{i+1}/{len(test_data)}] {question[:50]}...")

        start_time = time.time()
        if method == "api":
            response = generate_baseline_via_api(question, session_id=str(i))
        else:
            if not model_path:
                print("ERROR: --model-path required for direct method")
                return None
            response = generate_baseline_direct(question, model_path)
        response_time = time.time() - start_time

        results.append({
            "question_id": item.get("id", i),
            "question": question,
            "reference_answer": item.get("reference_answer", ""),
            "baseline_response": response,
            "response_time": response_time,
        })
        print(f"  Time: {response_time:.2f}s, Length: {len(response)} chars")

    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nBaseline responses saved to: {output_path}")
    return df


def compare_with_judge(
    system_results_path: str = "experiments/results/tutoring_quality_results.csv",
    baseline_results_path: str = "experiments/results/baseline_responses.csv",
    output_path: str = "experiments/results/comparison_results.csv",
    model: str = "Qwen/Qwen2.5-72B-Instruct",
    token: Optional[str] = None,
    sample_size: int = 50,
):
    """Evaluate both system and baseline responses with GPT-as-Judge."""

    if token is None:
        token = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: No HuggingFace token found.")
        return None

    system_df = pd.read_csv(system_results_path)
    baseline_df = pd.read_csv(baseline_results_path)

    # Align by question
    n = min(len(system_df), len(baseline_df), sample_size)
    system_df = system_df.head(n)
    baseline_df = baseline_df.head(n)

    print(f"Comparing {n} question pairs...")
    print(f"Judge model: {model}")
    print("=" * 60)

    results = []
    for idx in range(n):
        sys_row = system_df.iloc[idx]
        base_row = baseline_df.iloc[idx]

        question = sys_row.get("question", "")
        reference = sys_row.get("reference_answer", "")
        sys_response = str(sys_row.get("system_response", ""))
        base_response = str(base_row.get("baseline_response", ""))

        print(f"[{idx+1}/{n}] {question[:50]}...")

        # Judge system response
        sys_prompt = JUDGE_PROMPT.format(
            question=question,
            reference_answer=reference,
            system_response=sys_response[:1500],
        )
        sys_judge = call_hf_inference(sys_prompt, model=model, token=token)
        sys_scores = parse_judge_scores(sys_judge)

        time.sleep(2)  # Rate limiting

        # Judge baseline response
        base_prompt = JUDGE_PROMPT.format(
            question=question,
            reference_answer=reference,
            system_response=base_response[:1500],
        )
        base_judge = call_hf_inference(base_prompt, model=model, token=token)
        base_scores = parse_judge_scores(base_judge)

        time.sleep(2)

        results.append({
            "question_id": sys_row.get("question_id", idx),
            "question": question,
            # System scores
            "sys_accuracy": sys_scores["accuracy"],
            "sys_clarity": sys_scores["clarity"],
            "sys_educational": sys_scores["educational_value"],
            "sys_completeness": sys_scores["completeness"],
            "sys_overall": sys_scores["overall"],
            # Baseline scores
            "base_accuracy": base_scores["accuracy"],
            "base_clarity": base_scores["clarity"],
            "base_educational": base_scores["educational_value"],
            "base_completeness": base_scores["completeness"],
            "base_overall": base_scores["overall"],
        })

        print(f"  System:  A={sys_scores['accuracy']:.1f} C={sys_scores['clarity']:.1f} "
              f"E={sys_scores['educational_value']:.1f} Overall={sys_scores['overall']:.1f}")
        print(f"  Baseline: A={base_scores['accuracy']:.1f} C={base_scores['clarity']:.1f} "
              f"E={base_scores['educational_value']:.1f} Overall={base_scores['overall']:.1f}")

    # Save and summarize
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)

    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    print(f"{'Metric':<20} {'System':>10} {'Baseline':>10} {'Diff':>10} {'Winner':>10}")
    print("-" * 60)
    for m in metrics:
        sys_mean = results_df[f"sys_{m}"].mean()
        base_mean = results_df[f"base_{m}"].mean()
        diff = sys_mean - base_mean
        winner = "System" if diff > 0 else ("Baseline" if diff < 0 else "Tie")
        print(f"{m:<20} {sys_mean:>10.2f} {base_mean:>10.2f} {diff:>+10.2f} {winner:>10}")

    print(f"\nResults saved to: {output_path}")
    return results_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Baseline comparison experiment")
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # Generate baselines
    gen_parser = sub.add_parser("generate", help="Generate baseline responses")
    gen_parser.add_argument("--input", "-i", default="experiments/data/test_questions.json")
    gen_parser.add_argument("--output", "-o", default="experiments/results/baseline_responses.csv")
    gen_parser.add_argument("--method", "-m", choices=["api", "direct"], default="api",
                            help="'api' uses backend, 'direct' uses transformers locally")
    gen_parser.add_argument("--model-path", default=None, help="Model path for direct method")
    gen_parser.add_argument("--sample", "-s", type=int, default=50)

    # Compare
    cmp_parser = sub.add_parser("compare", help="Compare system vs baseline with judge")
    cmp_parser.add_argument("--system", default="experiments/results/tutoring_quality_results.csv")
    cmp_parser.add_argument("--baseline", default="experiments/results/baseline_responses.csv")
    cmp_parser.add_argument("--output", "-o", default="experiments/results/comparison_results.csv")
    cmp_parser.add_argument("--model", default="Qwen/Qwen2.5-72B-Instruct")
    cmp_parser.add_argument("--token", "-t", default=None)
    cmp_parser.add_argument("--sample", "-s", type=int, default=50)

    args = parser.parse_args()

    if args.command == "generate":
        generate_baselines(
            test_path=args.input,
            output_path=args.output,
            method=args.method,
            model_path=args.model_path,
            sample_size=args.sample,
        )
    elif args.command == "compare":
        compare_with_judge(
            system_results_path=args.system,
            baseline_results_path=args.baseline,
            output_path=args.output,
            model=args.model,
            token=args.token,
            sample_size=args.sample,
        )
    else:
        parser.print_help()
