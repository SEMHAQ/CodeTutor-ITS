"""
Experiment 4: GPT-as-Judge Evaluation
Use HuggingFace Inference API to evaluate response quality on multiple dimensions.
Requires: HUGGINGFACE_TOKEN environment variable or huggingface-cli login.
"""

import json
import os
import re
import sys
import time
import pandas as pd
from typing import Dict, List, Optional

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Judge prompt template
JUDGE_PROMPT = """You are an expert evaluator of educational programming tutoring responses.

Evaluate the following tutoring response to a student's programming question.

**Question:** {question}

**Reference Answer:** {reference_answer}

**System Response:** {system_response}

Rate the system response on each dimension (1-5 scale):
- 1 = Very Poor
- 2 = Poor
- 3 = Adequate
- 4 = Good
- 5 = Excellent

**Dimensions to evaluate:**
1. **Accuracy** (1-5): Is the information technically correct? Are there any errors?
2. **Clarity** (1-5): Is the explanation easy to understand for a beginner?
3. **Educational Value** (1-5): Does it help the student learn, not just give the answer? Does it explain concepts and reasoning?
4. **Completeness** (1-5): Does it cover the key points from the reference answer?

Respond in this exact JSON format (no other text):
{{"accuracy": <score>, "clarity": <score>, "educational_value": <score>, "completeness": <score>, "overall": <average>}}"""


def call_hf_inference(prompt: str, model: str = "Qwen/Qwen2.5-72B-Instruct",
                      token: Optional[str] = None, max_retries: int = 3) -> str:
    """Call HuggingFace Inference API."""
    try:
        from huggingface_hub import InferenceClient
    except ImportError:
        raise ImportError("pip install huggingface_hub")

    client = InferenceClient(token=token)

    for attempt in range(max_retries):
        try:
            response = client.chat_completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 10 * (attempt + 1)
                print(f"  API error: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  API failed after {max_retries} attempts: {e}")
                return ""


# --- Local judge (runs on GPU, no API cost) ---
_local_judge_model = None
_local_judge_tokenizer = None


def call_local_judge(prompt: str, model_path: str = None) -> str:
    """Call a local LLM as judge (zero cost, runs on GPU)."""
    global _local_judge_model, _local_judge_tokenizer

    if _local_judge_model is None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if model_path is None:
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            import config
            model_path = config.LLM_MODEL_PATH

        print(f"Loading local judge model from {model_path}...")
        _local_judge_tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        _local_judge_model = AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
        )
        print("Local judge model loaded.")

    messages = [
        {"role": "system", "content": "You are an expert evaluator. Respond only in JSON format."},
        {"role": "user", "content": prompt},
    ]
    text = _local_judge_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = _local_judge_tokenizer([text], return_tensors="pt").to(_local_judge_model.device)

    import torch
    with torch.no_grad():
        outputs = _local_judge_model.generate(
            **inputs, max_new_tokens=200, temperature=0.1, do_sample=True, top_p=0.9
        )
    generated = outputs[0][inputs["input_ids"].shape[1]:]
    return _local_judge_tokenizer.decode(generated, skip_special_tokens=True).strip()


def parse_judge_scores(response: str) -> Dict[str, float]:
    """Parse JSON scores from judge response."""
    default = {"accuracy": 0, "clarity": 0, "educational_value": 0, "completeness": 0, "overall": 0}
    if not response:
        return default

    try:
        # Try to find JSON in the response
        json_match = re.search(r'\{[^}]+\}', response)
        if json_match:
            scores = json.loads(json_match.group())
            # Validate scores are in range
            for key in ["accuracy", "clarity", "educational_value", "completeness"]:
                if key in scores:
                    scores[key] = max(1, min(5, float(scores[key])))
            if "overall" not in scores:
                vals = [scores.get(k, 0) for k in ["accuracy", "clarity", "educational_value", "completeness"]]
                scores["overall"] = sum(vals) / len(vals) if vals else 0
            return {**default, **scores}
    except (json.JSONDecodeError, ValueError):
        pass

    return default


def run_judge_evaluation(
    results_path: str = "experiments/results/tutoring_quality_results.csv",
    output_path: str = "experiments/results/gpt_judge_results.csv",
    model: str = "Qwen/Qwen2.5-72B-Instruct",
    token: Optional[str] = None,
    sample_size: int = 50,
):
    """Run GPT-as-Judge evaluation on existing results."""

    # Get token from environment if not provided
    if token is None:
        token = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: No HuggingFace token found.")
        print("Set HUGGINGFACE_TOKEN environment variable or run: huggingface-cli login")
        return None

    # Load existing results
    df = pd.read_csv(results_path)
    if sample_size and len(df) > sample_size:
        df = df.head(sample_size)

    print(f"Loaded {len(df)} responses to evaluate.")
    print(f"Judge model: {model}")
    print("=" * 60)

    results = []
    for idx, row in df.iterrows():
        question = row.get("question", "")
        reference = row.get("reference_answer", "")
        response = row.get("system_response", "")

        if not response or pd.isna(response):
            continue

        print(f"[{idx+1}/{len(df)}] Evaluating: {question[:50]}...")

        prompt = JUDGE_PROMPT.format(
            question=question,
            reference_answer=reference,
            system_response=response[:1500],  # Truncate to avoid token limits
        )

        judge_response = call_hf_inference(prompt, model=model, token=token)
        scores = parse_judge_scores(judge_response)

        result = {
            "question_id": row.get("question_id", idx),
            "question": question,
            "accuracy": scores["accuracy"],
            "clarity": scores["clarity"],
            "educational_value": scores["educational_value"],
            "completeness": scores["completeness"],
            "overall": scores["overall"],
            "judge_raw_response": judge_response,
        }
        results.append(result)

        print(f"  Scores: A={scores['accuracy']:.1f} C={scores['clarity']:.1f} "
              f"E={scores['educational_value']:.1f} Comp={scores['completeness']:.1f} "
              f"Overall={scores['overall']:.1f}")

        # Rate limiting - HF free tier
        time.sleep(2)

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # Print summary
    print("\n" + "=" * 60)
    print("GPT-AS-JUDGE EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total evaluated: {len(results)}")
    print(f"Average Accuracy:        {results_df['accuracy'].mean():.2f} (std: {results_df['accuracy'].std():.2f})")
    print(f"Average Clarity:         {results_df['clarity'].mean():.2f} (std: {results_df['clarity'].std():.2f})")
    print(f"Average Educational:     {results_df['educational_value'].mean():.2f} (std: {results_df['educational_value'].std():.2f})")
    print(f"Average Completeness:    {results_df['completeness'].mean():.2f} (std: {results_df['completeness'].std():.2f})")
    print(f"Average Overall:         {results_df['overall'].mean():.2f} (std: {results_df['overall'].std():.2f})")
    print(f"\nResults saved to: {output_path}")

    return results_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GPT-as-Judge evaluation")
    parser.add_argument("--input", "-i", default="experiments/results/tutoring_quality_results.csv")
    parser.add_argument("--output", "-o", default="experiments/results/gpt_judge_results.csv")
    parser.add_argument("--model", "-m", default="Qwen/Qwen2.5-72B-Instruct",
                        help="HuggingFace model for judging")
    parser.add_argument("--token", "-t", default=None, help="HuggingFace API token")
    parser.add_argument("--sample", "-s", type=int, default=50, help="Number of samples to evaluate")
    args = parser.parse_args()

    run_judge_evaluation(
        results_path=args.input,
        output_path=args.output,
        model=args.model,
        token=args.token,
        sample_size=args.sample,
    )
