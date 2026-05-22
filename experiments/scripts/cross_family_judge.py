"""
Cross-Family Judge Evaluation
Re-judge Exp 4 (LLM-as-Judge) and Exp 5 (LoRA) responses using a different
model family to validate evaluation robustness and mitigate same-family bias.

Usage:
  $env:OPENROUTER_API_KEY = "sk-or-v1-..."
  python experiments/scripts/cross_family_judge.py

Requires: existing results in experiments/results/
"""

import json
import os
import sys
import time
import pandas as pd
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gpt_judge_evaluation import call_openrouter, parse_judge_scores, JUDGE_PROMPT


def judge_exp4_responses(
    input_path: str = "experiments/results/tutoring_quality_results.csv",
    output_path: str = "experiments/results/cross_family_judge_exp4.csv",
    model: str = "meta-llama/llama-3-70b-instruct",
):
    """Re-judge Exp 4 responses with cross-family model."""

    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} responses for cross-family evaluation")
    print(f"Judge model: {model}")
    print("=" * 60)

    results = []
    for idx, row in df.iterrows():
        question = row.get("question", "")
        reference = row.get("reference_answer", "")
        response = str(row.get("system_response", ""))

        if not response or response == "nan":
            continue

        print(f"[{idx+1}/{len(df)}] {question[:50]}...")

        prompt = JUDGE_PROMPT.format(
            question=question,
            reference_answer=reference,
            system_response=response[:1500],
        )

        judge_response = call_openrouter(prompt, model=model)
        scores = parse_judge_scores(judge_response)

        if scores["overall"] == 0:
            print(f"  WARNING: Parse failed. Raw: {judge_response[:100]}...")

        results.append({
            "question_id": row.get("question_id", idx),
            "question": question,
            "accuracy": scores["accuracy"],
            "clarity": scores["clarity"],
            "educational_value": scores["educational_value"],
            "completeness": scores["completeness"],
            "overall": scores["overall"],
            "judge_raw_response": judge_response,
        })

        print(f"  Scores: A={scores['accuracy']:.1f} C={scores['clarity']:.1f} "
              f"E={scores['educational_value']:.1f} Comp={scores['completeness']:.1f} "
              f"Overall={scores['overall']:.1f}")

        time.sleep(1)

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # Compare with Qwen judge
    print("\n" + "=" * 60)
    print("CROSS-FAMILY COMPARISON: Qwen2.5-72B vs LLaMA-3-70B")
    print("=" * 60)

    qwen_df = pd.read_csv("experiments/results/gpt_judge_results.csv")
    n = min(len(qwen_df), len(results_df))

    metrics = ["accuracy", "clarity", "educational_value", "completeness", "overall"]
    print(f"{'Metric':<20} {'Qwen':>10} {'LLaMA':>10} {'Diff':>10}")
    print("-" * 50)
    for m in metrics:
        qwen_mean = qwen_df[m].head(n).mean()
        llama_mean = results_df[m].head(n).mean()
        diff = llama_mean - qwen_mean
        print(f"{m:<20} {qwen_mean:>10.2f} {llama_mean:>10.2f} {diff:>+10.2f}")

    # Correlation analysis
    print(f"\nPer-dimension Pearson correlation (n={n}):")
    for m in metrics:
        corr = qwen_df[m].head(n).corr(results_df[m].head(n))
        print(f"  {m}: r = {corr:.3f}")

    print(f"\nResults saved to: {output_path}")
    return results_df


def judge_exp5_responses(
    input_path: str = "experiments/results/finetune_comparison_responses.csv",
    output_path: str = "experiments/results/cross_family_judge_exp5.csv",
    model: str = "meta-llama/llama-3-70b-instruct",
):
    """Re-judge Exp 5 (LoRA) responses with cross-family model."""

    df = pd.read_csv(input_path)
    print(f"\nLoaded {len(df)} LoRA comparison responses")
    print(f"Judge model: {model}")
    print("=" * 60)

    results = []
    for idx, row in df.iterrows():
        q = row["question"]
        ref = row.get("reference_answer", "")
        print(f"[{idx+1}/{len(df)}] {q[:50]}...")

        # Judge base response
        base_prompt = JUDGE_PROMPT.format(
            question=q, reference_answer=ref,
            system_response=str(row["base_response"])[:1500]
        )
        base_raw = call_openrouter(base_prompt, model=model)
        base_scores = parse_judge_scores(base_raw)

        # Judge fine-tuned response
        ft_prompt = JUDGE_PROMPT.format(
            question=q, reference_answer=ref,
            system_response=str(row["finetuned_response"])[:1500]
        )
        ft_raw = call_openrouter(ft_prompt, model=model)
        ft_scores = parse_judge_scores(ft_raw)

        if base_scores["overall"] == 0 or ft_scores["overall"] == 0:
            print(f"  WARNING: Parse failed.")

        results.append({
            "question_id": row.get("question_id", idx),
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
        time.sleep(1)

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # Summary
    print("\n" + "=" * 60)
    print("LoRA COMPARISON (LLaMA-3-70B Judge)")
    print("=" * 60)
    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    print(f"{'Metric':<20} {'Base':>10} {'LoRA':>10} {'Diff':>10}")
    print("-" * 50)
    for m in metrics:
        base_mean = results_df[f"base_{m}"].mean()
        ft_mean = results_df[f"ft_{m}"].mean()
        diff = ft_mean - base_mean
        print(f"{m:<20} {base_mean:>10.2f} {ft_mean:>10.2f} {diff:>+10.2f}")

    print(f"\nResults saved to: {output_path}")
    return results_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cross-family judge evaluation")
    parser.add_argument("--model", "-m", default="meta-llama/llama-3-70b-instruct",
                        help="Cross-family judge model (OpenRouter)")
    parser.add_argument("--exp", choices=["4", "5", "all"], default="all",
                        help="Which experiment to re-judge")
    args = parser.parse_args()

    if not os.environ.get("OPENROUTER_API_KEY"):
        print("ERROR: Set OPENROUTER_API_KEY environment variable.")
        sys.exit(1)

    if args.exp in ("4", "all"):
        judge_exp4_responses(model=args.model)
    if args.exp in ("5", "all"):
        judge_exp5_responses(model=args.model)
