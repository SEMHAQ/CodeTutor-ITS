"""
Experiment 1: Evaluate Tutoring Quality
Compare system responses with ground truth using BLEU, ROUGE-L metrics.
Uses CS1QA dataset or custom test set.
"""

import json
import os
import sys
import time
import httpx
import pandas as pd
from typing import List, Dict
from rouge_score import rouge_scorer
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

API_BASE_URL = "http://localhost:8000"


def load_test_dataset(filepath: str) -> List[Dict]:
    """Load test dataset from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def query_tutor(question: str, session_id: str = "eval_session") -> str:
    """Query the tutoring system."""
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{API_BASE_URL}/api/tutor/chat",
                json={
                    "message": question,
                    "session_id": session_id,
                    "mode": "tutor",
                    "programming_language": "python",
                },
            )
            response.raise_for_status()
            return response.json().get("response", "")
    except Exception as e:
        print(f"Error querying tutor: {e}")
        return ""


def compute_bleu(reference: str, hypothesis: str) -> float:
    """Compute BLEU score."""
    ref_tokens = list(reference)
    hyp_tokens = list(hypothesis)
    smoothie = SmoothingFunction().method1
    try:
        return sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothie)
    except:
        return 0.0


def compute_rouge_l(reference: str, hypothesis: str) -> float:
    """Compute ROUGE-L score."""
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return scores["rougeL"].fmeasure


def compute_response_quality_metrics(response: str) -> Dict:
    """Compute basic quality metrics for a response."""
    return {
        "length": len(response),
        "word_count": len(response.split()),
        "has_code_block": "```" in response,
        "has_explanation": any(
            kw in response for kw in ["因为", "所以", "这是", "解释", "原因", "because", "therefore", "this is"]
        ),
        "has_example": any(
            kw in response for kw in ["例如", "比如", "示例", "for example", "e.g.", "example"]
        ),
    }


def run_evaluation(test_data_path: str, output_path: str):
    """Run the full evaluation."""
    print("Loading test dataset...")
    test_data = load_test_dataset(test_data_path)
    print(f"Loaded {len(test_data)} test cases.")

    results = []
    for i, item in enumerate(test_data):
        print(f"Evaluating {i+1}/{len(test_data)}: {item.get('question', '')[:50]}...")

        question = item["question"]
        reference = item.get("reference_answer", "")

        # Query system
        start_time = time.time()
        response = query_tutor(question, session_id=f"eval_{i}")
        response_time = time.time() - start_time

        # Compute metrics
        bleu = compute_bleu(reference, response) if reference else 0.0
        rouge_l = compute_rouge_l(reference, response) if reference else 0.0
        quality = compute_response_quality_metrics(response)

        result = {
            "question_id": i,
            "question": question,
            "reference_answer": reference,
            "system_response": response,
            "bleu": bleu,
            "rouge_l": rouge_l,
            "response_time": response_time,
            **quality,
        }
        results.append(result)

        print(f"  BLEU: {bleu:.4f}, ROUGE-L: {rouge_l:.4f}, Time: {response_time:.2f}s")

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # Print summary
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total test cases: {len(results)}")
    print(f"Average BLEU: {df['bleu'].mean():.4f}")
    print(f"Average ROUGE-L: {df['rouge_l'].mean():.4f}")
    print(f"Average response time: {df['response_time'].mean():.2f}s")
    print(f"Response has code block: {df['has_code_block'].mean()*100:.1f}%")
    print(f"Response has explanation: {df['has_explanation'].mean()*100:.1f}%")
    print(f"Results saved to: {output_path}")

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate tutoring quality")
    parser.add_argument(
        "--input", "-i",
        default="experiments/data/test_questions.json",
        help="Path to test dataset JSON",
    )
    parser.add_argument(
        "--output", "-o",
        default="experiments/results/tutoring_quality_results.csv",
        help="Path to output CSV",
    )
    args = parser.parse_args()

    run_evaluation(args.input, args.output)
