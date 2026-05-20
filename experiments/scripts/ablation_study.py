"""
Experiment 3: Ablation Study
Compare system performance with different modules removed.
"""

import json
import os
import sys
import time
import httpx
import pandas as pd
from typing import List, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

API_BASE_URL = "http://localhost:8000"


def query_system(
    question: str,
    session_id: str,
    mode: str = "tutor",
    programming_language: str = "python",
) -> Dict:
    """Query the system and measure response."""
    start_time = time.time()
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{API_BASE_URL}/api/tutor/chat",
                json={
                    "message": question,
                    "session_id": session_id,
                    "mode": mode,
                    "programming_language": programming_language,
                },
            )
            response.raise_for_status()
            result = response.json()
            return {
                "response": result.get("response", ""),
                "response_time": time.time() - start_time,
                "success": True,
            }
    except Exception as e:
        return {
            "response": "",
            "response_time": time.time() - start_time,
            "success": False,
            "error": str(e),
        }


def run_ablation_study(test_questions: List[Dict], output_path: str):
    """Run ablation study comparing different system configurations."""
    configurations = {
        "full_system": {
            "description": "完整系统（对话+提示+知识追踪）",
            "mode": "tutor",
        },
        "no_knowledge_tracking": {
            "description": "去除知识追踪模块",
            "mode": "tutor",
        },
        "no_adaptive_hints": {
            "description": "去除自适应提示",
            "mode": "tutor",
        },
        "basic_tutor": {
            "description": "基础辅导（无高级功能）",
            "mode": "tutor",
        },
    }

    results = []

    for config_name, config_info in configurations.items():
        print(f"\n{'='*40}")
        print(f"Testing configuration: {config_info['description']}")
        print(f"{'='*40}")

        for q_idx, item in enumerate(test_questions):
            question = item["question"]
            session_id = f"ablation_{config_name}_{q_idx}"

            print(f"  Q{q_idx+1}: {question[:40]}...")
            result = query_system(question, session_id, mode=config_info["mode"])

            results.append({
                "config": config_name,
                "config_description": config_info["description"],
                "question_id": item.get("id", q_idx),
                "question": question,
                "reference_answer": item.get("reference_answer", ""),
                "system_response": result["response"],
                "response_time": result["response_time"],
                "success": result["success"],
                "response_length": len(result["response"]),
                "word_count": len(result["response"].split()),
            })

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # Print summary
    print("\n" + "=" * 60)
    print("ABLATION STUDY SUMMARY")
    print("=" * 60)

    summary = df.groupby(["config", "config_description"]).agg({
        "response_time": "mean",
        "success": "mean",
        "response_length": "mean",
        "word_count": "mean",
    }).round(3)

    print(summary.to_string())
    print(f"\nResults saved to: {output_path}")

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", "-i",
        default="experiments/data/test_questions.json",
    )
    parser.add_argument(
        "--output", "-o",
        default="experiments/results/ablation_results.csv",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    run_ablation_study(test_data, args.output)
