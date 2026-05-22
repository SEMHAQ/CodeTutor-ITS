"""
Experiment 2: Prompt Strategy Comparison
Compare different prompting strategies (zero-shot, few-shot, CoT).
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

# Different prompt strategies
PROMPT_STRATEGIES = {
    "zero_shot": "请解释以下编程概念：{question}",
    "few_shot": """请参考以下示例来解释编程概念：

示例1：
问题：什么是变量？
回答：变量是程序中用来存储数据的容器。你可以把变量想象成一个有标签的盒子，标签是变量名，盒子里装的是值。例如，age = 25 就是创建了一个名为 age 的变量，存储了值 25。

示例2：
问题：什么是循环？
回答：循环是一种重复执行代码块的结构。比如 for 循环可以遍历一个列表中的每个元素。

现在请回答：
问题：{question}
回答：""",
    "cot": """请用逐步推理的方式来解释以下编程概念：

问题：{question}

请按以下步骤思考：
1. 首先，这个概念的定义是什么？
2. 它解决什么问题？
3. 给出一个简单的代码示例
4. 总结关键要点

回答：""",
}


def query_with_custom_prompt(prompt: str, session_id: str) -> str:
    """Query system with a custom prompt."""
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{API_BASE_URL}/api/tutor/chat",
                json={
                    "message": prompt,
                    "session_id": session_id,
                    "mode": "tutor",
                    "programming_language": "python",
                },
            )
            response.raise_for_status()
            return response.json().get("response", "")
    except Exception as e:
        print(f"Error: {e}")
        return ""


def evaluate_response_quality(response: str) -> Dict:
    """Evaluate response quality with multiple dimensions."""
    return {
        "length": len(response),
        "word_count": len(response.split()),
        "has_code": "```" in response or "    " in response,
        "has_steps": any(f"{i}." in response or f"{i}、" in response for i in range(1, 10)),
        "clarity_score": min(len(response.split()) / 50, 5.0),  # Normalized length score
        "completeness_score": sum([
            1 for kw in ["定义", "解释", "例如", "代码", "总结",
                         "definition", "explain", "example", "code", "summary"]
            if kw in response.lower()
        ]) / 5.0,
    }


def run_comparison(test_questions: List[str], output_path: str, questions_meta: List[Dict] = None):
    """Run prompt strategy comparison."""
    results = []

    for q_idx, question in enumerate(test_questions):
        print(f"\nQuestion {q_idx+1}/{len(test_questions)}: {question[:50]}...")

        # Get topic/difficulty from metadata if available
        meta = questions_meta[q_idx] if questions_meta and q_idx < len(questions_meta) else {}

        for strategy_name, prompt_template in PROMPT_STRATEGIES.items():
            prompt = prompt_template.format(question=question)
            session_id = f"comparison_{strategy_name}_{q_idx}"

            start_time = time.time()
            response = query_with_custom_prompt(prompt, session_id)
            response_time = time.time() - start_time

            quality = evaluate_response_quality(response)

            result = {
                "question_id": q_idx,
                "question": question,
                "topic": meta.get("topic", "unknown"),
                "difficulty": meta.get("difficulty", "unknown"),
                "strategy": strategy_name,
                "response": response,
                "response_time": response_time,
                **quality,
            }
            results.append(result)

            print(f"  [{strategy_name}] Words: {quality['word_count']}, "
                  f"Time: {response_time:.2f}s, "
                  f"Completeness: {quality['completeness_score']:.2f}")

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # Print comparison summary
    print("\n" + "=" * 60)
    print("PROMPT STRATEGY COMPARISON SUMMARY")
    print("=" * 60)

    summary = df.groupby("strategy").agg({
        "word_count": "mean",
        "response_time": "mean",
        "has_code": "mean",
        "has_steps": "mean",
        "completeness_score": "mean",
    }).round(3)

    print(summary.to_string())

    # Print per-topic breakdown
    if "topic" in df.columns and df["topic"].nunique() > 1:
        print("\n" + "=" * 60)
        print("PER-TOPIC BREAKDOWN")
        print("=" * 60)
        topic_summary = df.groupby(["topic", "strategy"]).agg({
            "completeness_score": "mean",
            "word_count": "mean",
        }).round(3)
        print(topic_summary.to_string())

    # Print per-difficulty breakdown
    if "difficulty" in df.columns and df["difficulty"].nunique() > 1:
        print("\n" + "=" * 60)
        print("PER-DIFFICULTY BREAKDOWN")
        print("=" * 60)
        diff_summary = df.groupby(["difficulty", "strategy"]).agg({
            "completeness_score": "mean",
            "word_count": "mean",
        }).round(3)
        print(diff_summary.to_string())

    print(f"\nResults saved to: {output_path}")

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", default="experiments/results/prompt_comparison_exp2.csv")
    parser.add_argument("--questions", "-q", default=None, help="Path to questions JSON file")
    args = parser.parse_args()

    # Load questions from file or use defaults
    questions_data = None
    if args.questions and os.path.exists(args.questions):
        with open(args.questions, "r", encoding="utf-8") as f:
            questions_data = json.load(f)
        test_questions = [q["question"] for q in questions_data]
        print(f"Loaded {len(test_questions)} questions from {args.questions}")
    else:
        # Default: 15 questions from exp2_questions.json
        default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "exp2_questions.json")
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                questions_data = json.load(f)
            test_questions = [q["question"] for q in questions_data]
            print(f"Loaded {len(test_questions)} questions from {default_path}")
        else:
            # Fallback to 5 questions
            test_questions = [
                "What is a list comprehension in Python?",
                "Explain the concept and working principle of recursion",
                "What is polymorphism in OOP?",
                "Explain what decorators are in Python",
                "What are time complexity and space complexity?",
            ]
            print(f"Using {len(test_questions)} default questions")

    run_comparison(test_questions, args.output, questions_meta=questions_data)
