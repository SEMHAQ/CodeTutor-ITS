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
    chart_path = os.path.join(CHARTS_DIR, "tutoring_quality.pdf")
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
    chart_path = os.path.join(CHARTS_DIR, "prompt_comparison.pdf")
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
    chart_path = os.path.join(CHARTS_DIR, "ablation_study.pdf")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {chart_path}")


def plot_gpt_judge(results_path: str):
    """Plot GPT-as-Judge evaluation results."""
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("GPT-as-Judge Evaluation Results", fontsize=14, fontweight="bold")

    # Radar-style bar chart for dimensions
    dimensions = ["accuracy", "clarity", "educational_value", "completeness"]
    dim_labels = ["Accuracy", "Clarity", "Educational\nValue", "Completeness"]
    means = [df[d].mean() for d in dimensions]
    stds = [df[d].std() for d in dimensions]
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"]

    bars = axes[0].bar(dim_labels, means, yerr=stds, capsize=5, color=colors, alpha=0.85, edgecolor="black", linewidth=0.5)
    axes[0].set_title("Average Scores by Dimension")
    axes[0].set_ylabel("Score (1-5)")
    axes[0].set_ylim(0, 5.5)
    axes[0].axhline(y=3, color="gray", linestyle=":", alpha=0.5, label="Adequate (3)")
    axes[0].legend()
    # Add value labels on bars
    for bar, mean in zip(bars, means):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     f'{mean:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Distribution of overall scores
    axes[1].hist(df["overall"], bins=10, color="steelblue", alpha=0.8, edgecolor="black", linewidth=0.5)
    axes[1].set_title("Distribution of Overall Scores")
    axes[1].set_xlabel("Overall Score")
    axes[1].set_ylabel("Count")
    axes[1].axvline(x=df["overall"].mean(), color="red", linestyle="--",
                    label=f'Mean: {df["overall"].mean():.2f}')
    axes[1].legend()

    plt.tight_layout()
    chart_path = os.path.join(CHARTS_DIR, "gpt_judge_evaluation.pdf")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {chart_path}")


def plot_comparison(results_path: str):
    """Plot system vs baseline comparison."""
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("CodeTutor-ITS vs Raw LLM Baseline", fontsize=14, fontweight="bold")

    # Grouped bar chart
    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    metric_labels = ["Accuracy", "Clarity", "Educational", "Completeness", "Overall"]

    sys_means = [df[f"sys_{m}"].mean() for m in metrics]
    base_means = [df[f"base_{m}"].mean() for m in metrics]

    x = range(len(metrics))
    width = 0.35

    bars1 = axes[0].bar([i - width/2 for i in x], sys_means, width, label="CodeTutor-ITS",
                         color="#2196F3", alpha=0.85, edgecolor="black", linewidth=0.5)
    bars2 = axes[0].bar([i + width/2 for i in x], base_means, width, label="Raw LLM",
                         color="#FF5722", alpha=0.85, edgecolor="black", linewidth=0.5)

    axes[0].set_title("Score Comparison by Dimension")
    axes[0].set_ylabel("Score (1-5)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metric_labels)
    axes[0].set_ylim(0, 5.5)
    axes[0].legend()
    axes[0].axhline(y=3, color="gray", linestyle=":", alpha=0.5)

    # Win/Loss/Tie analysis
    wins = sum(1 for m in metrics if df[f"sys_{m}"].mean() > df[f"base_{m}"].mean())
    losses = sum(1 for m in metrics if df[f"sys_{m}"].mean() < df[f"base_{m}"].mean())
    ties = len(metrics) - wins - losses

    pie_colors = ["#4CAF50", "#F44336", "#9E9E9E"]
    axes[1].pie([wins, losses, ties], labels=["System Wins", "Baseline Wins", "Tie"],
                autopct="%1.0f%%", colors=pie_colors, startangle=90)
    axes[1].set_title("Win/Loss/Tie Across Dimensions")

    plt.tight_layout()
    chart_path = os.path.join(CHARTS_DIR, "system_vs_baseline.pdf")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {chart_path}")


def plot_finetune_comparison(results_path: str):
    """Plot fine-tuned vs base model comparison."""
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("LoRA Fine-tuned vs Base Model", fontsize=14, fontweight="bold")

    # Grouped bar chart
    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    metric_labels = ["Accuracy", "Clarity", "Educational", "Completeness", "Overall"]

    base_means = [df[f"base_{m}"].mean() for m in metrics]
    ft_means = [df[f"ft_{m}"].mean() for m in metrics]

    x = range(len(metrics))
    width = 0.35

    axes[0].bar([i - width/2 for i in x], base_means, width, label="Base Model",
                color="#9E9E9E", alpha=0.85, edgecolor="black", linewidth=0.5)
    axes[0].bar([i + width/2 for i in x], ft_means, width, label="LoRA Fine-tuned",
                color="#4CAF50", alpha=0.85, edgecolor="black", linewidth=0.5)

    axes[0].set_title("Score Comparison by Dimension")
    axes[0].set_ylabel("Score (1-5)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metric_labels)
    axes[0].set_ylim(0, 5.5)
    axes[0].legend()
    axes[0].axhline(y=3, color="gray", linestyle=":", alpha=0.5)

    # Improvement chart
    improvements = [(ft_means[i] - base_means[i]) for i in range(len(metrics))]
    colors = ["#4CAF50" if v >= 0 else "#F44336" for v in improvements]
    axes[1].bar(metric_labels, improvements, color=colors, alpha=0.85, edgecolor="black", linewidth=0.5)
    axes[1].set_title("Improvement After Fine-tuning")
    axes[1].set_ylabel("Score Difference")
    axes[1].axhline(y=0, color="black", linewidth=0.5)
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    chart_path = os.path.join(CHARTS_DIR, "finetune_comparison.pdf")
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

    judge_path = os.path.join(RESULTS_DIR, "gpt_judge_results.csv")
    if os.path.exists(judge_path):
        plot_gpt_judge(judge_path)

    comparison_path = os.path.join(RESULTS_DIR, "comparison_results.csv")
    if os.path.exists(comparison_path):
        plot_comparison(comparison_path)

    finetune_path = os.path.join(RESULTS_DIR, "finetune_comparison.csv")
    if os.path.exists(finetune_path):
        plot_finetune_comparison(finetune_path)

    print("Chart generation complete.")
