"""
Generate publication-quality charts from experiment results.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
CHARTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)


def plot_tutoring_quality(results_path: str):
    """Plot tutoring quality metrics."""
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Tutoring Quality Evaluation Results", fontsize=14, fontweight="bold")

    # BLEU scores
    axes[0, 0].bar(range(len(df)), df["bleu"], color="steelblue", alpha=0.8)
    axes[0, 0].set_title("BLEU Scores per Question")
    axes[0, 0].set_xlabel("Question ID")
    axes[0, 0].set_ylabel("BLEU Score")
    axes[0, 0].axhline(y=df["bleu"].mean(), color="red", linestyle="--", label=f'Mean: {df["bleu"].mean():.3f}')
    axes[0, 0].legend()

    # ROUGE-L scores
    axes[0, 1].bar(range(len(df)), df["rouge_l"], color="coral", alpha=0.8)
    axes[0, 1].set_title("ROUGE-L Scores per Question")
    axes[0, 1].set_xlabel("Question ID")
    axes[0, 1].set_ylabel("ROUGE-L Score")
    axes[0, 1].axhline(y=df["rouge_l"].mean(), color="red", linestyle="--", label=f'Mean: {df["rouge_l"].mean():.3f}')
    axes[0, 1].legend()

    # Response time
    axes[1, 0].bar(range(len(df)), df["response_time"], color="green", alpha=0.8)
    axes[1, 0].set_title("Response Time per Question")
    axes[1, 0].set_xlabel("Question ID")
    axes[1, 0].set_ylabel("Time (seconds)")

    # Quality metrics
    quality_metrics = ["has_code_block", "has_explanation", "has_example"]
    quality_means = [df[m].mean() for m in quality_metrics]
    axes[1, 1].bar(quality_metrics, quality_means, color=["purple", "orange", "cyan"], alpha=0.8)
    axes[1, 1].set_title("Response Quality Metrics")
    axes[1, 1].set_ylabel("Proportion")
    axes[1, 1].set_ylim(0, 1)

    plt.tight_layout()
    chart_path = os.path.join(CHARTS_DIR, "tutoring_quality.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {chart_path}")


def plot_prompt_comparison(results_path: str):
    """Plot prompt strategy comparison."""
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Prompt Strategy Comparison", fontsize=14, fontweight="bold")

    strategies = df["strategy"].unique()
    colors = ["steelblue", "coral", "green"]

    # Word count comparison
    word_means = [df[df["strategy"] == s]["word_count"].mean() for s in strategies]
    axes[0, 0].bar(strategies, word_means, color=colors[:len(strategies)], alpha=0.8)
    axes[0, 0].set_title("Average Word Count")
    axes[0, 0].set_ylabel("Words")

    # Response time comparison
    time_means = [df[df["strategy"] == s]["response_time"].mean() for s in strategies]
    axes[0, 1].bar(strategies, time_means, color=colors[:len(strategies)], alpha=0.8)
    axes[0, 1].set_title("Average Response Time")
    axes[0, 1].set_ylabel("Seconds")

    # Code inclusion rate
    code_means = [df[df["strategy"] == s]["has_code"].mean() for s in strategies]
    axes[1, 0].bar(strategies, code_means, color=colors[:len(strategies)], alpha=0.8)
    axes[1, 0].set_title("Code Block Inclusion Rate")
    axes[1, 0].set_ylabel("Proportion")

    # Completeness score
    comp_means = [df[df["strategy"] == s]["completeness_score"].mean() for s in strategies]
    axes[1, 1].bar(strategies, comp_means, color=colors[:len(strategies)], alpha=0.8)
    axes[1, 1].set_title("Completeness Score")
    axes[1, 1].set_ylabel("Score")

    plt.tight_layout()
    chart_path = os.path.join(CHARTS_DIR, "prompt_comparison.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {chart_path}")


def plot_ablation_study(results_path: str):
    """Plot ablation study results."""
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Ablation Study Results", fontsize=14, fontweight="bold")

    configs = df["config"].unique()
    config_labels = {
        "full_system": "Full System",
        "no_knowledge_tracking": "w/o KT",
        "no_adaptive_hints": "w/o AH",
        "basic_tutor": "Basic",
    }
    labels = [config_labels.get(c, c) for c in configs]
    colors = ["steelblue", "coral", "green", "purple"]

    # Response time
    time_means = [df[df["config"] == c]["response_time"].mean() for c in configs]
    axes[0].bar(labels, time_means, color=colors[:len(configs)], alpha=0.8)
    axes[0].set_title("Average Response Time")
    axes[0].set_ylabel("Seconds")
    axes[0].tick_params(axis="x", rotation=45)

    # Success rate
    success_means = [df[df["config"] == c]["success"].mean() for c in configs]
    axes[1].bar(labels, success_means, color=colors[:len(configs)], alpha=0.8)
    axes[1].set_title("Success Rate")
    axes[1].set_ylabel("Rate")
    axes[1].set_ylim(0, 1)
    axes[1].tick_params(axis="x", rotation=45)

    # Response length
    len_means = [df[df["config"] == c]["response_length"].mean() for c in configs]
    axes[2].bar(labels, len_means, color=colors[:len(configs)], alpha=0.8)
    axes[2].set_title("Average Response Length")
    axes[2].set_ylabel("Characters")
    axes[2].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    chart_path = os.path.join(CHARTS_DIR, "ablation_study.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {chart_path}")


if __name__ == "__main__":
    # Generate charts if results exist
    tutoring_path = os.path.join(RESULTS_DIR, "tutoring_quality_results.csv")
    if os.path.exists(tutoring_path):
        plot_tutoring_quality(tutoring_path)

    prompt_path = os.path.join(RESULTS_DIR, "prompt_comparison_results.csv")
    if os.path.exists(prompt_path):
        plot_prompt_comparison(prompt_path)

    ablation_path = os.path.join(RESULTS_DIR, "ablation_results.csv")
    if os.path.exists(ablation_path):
        plot_ablation_study(ablation_path)

    print("Chart generation complete.")
