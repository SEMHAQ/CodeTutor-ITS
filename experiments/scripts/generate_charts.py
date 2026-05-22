"""
Generate publication-quality charts from experiment results.
MDPI Applied Sciences style: Arial font, four-color scheme, clean spines.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# === Global style ===
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["font.size"] = 12         # tick labels
matplotlib.rcParams["axes.labelsize"] = 13    # axis labels
matplotlib.rcParams["axes.titlesize"] = 14    # subplot titles
matplotlib.rcParams["axes.titleweight"] = "bold"
matplotlib.rcParams["legend.fontsize"] = 11
matplotlib.rcParams["axes.linewidth"] = 0.75

# Four-color palette (matching architecture diagram)
BLUE   = "#6699cc"
GREEN  = "#66bb66"
ORANGE = "#e6994d"
PURPLE = "#9966cc"
COLORS = [BLUE, GREEN, ORANGE, PURPLE]
RED    = "#cc4444"

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
CHARTS_DIR  = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

BAR_WIDTH = 0.65


def _clean_axes(ax):
    """Remove top/right spines, set line width."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_linewidth(0.75)
    ax.tick_params(width=0.75, length=3)


def _save(fig, name):
    chart_path = os.path.join(CHARTS_DIR, name)
    fig.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved: {chart_path}")


# ============================================================
# Figure 2: GPT-as-Judge Evaluation
# ============================================================
def plot_gpt_judge(results_path: str):
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # --- Left: bar chart by dimension ---
    dimensions = ["accuracy", "clarity", "educational_value", "completeness"]
    dim_labels = ["Accuracy", "Clarity", "Educational\nValue", "Completeness"]
    means = [df[d].mean() for d in dimensions]
    stds  = [df[d].std() for d in dimensions]
    dim_colors = [BLUE, GREEN, ORANGE, PURPLE]

    bars = axes[0].bar(dim_labels, means, yerr=stds, capsize=4,
                       color=dim_colors, width=BAR_WIDTH,
                       edgecolor="none", linewidth=0)
    axes[0].set_ylabel("Score (1–5)")
    axes[0].set_ylim(0, 6.2)
    axes[0].axhline(y=3, color="gray", linestyle=":", linewidth=0.75, alpha=0.6)
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color="gray", linestyle=":", linewidth=0.75, label="Adequate Threshold")]
    axes[0].legend(handles=legend_elements, loc="upper right", frameon=False)
    # Value labels above error bars
    for bar, mean, std in zip(bars, means, stds):
        axes[0].text(bar.get_x() + bar.get_width() / 2, mean + std + 0.08,
                     f"{mean:.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")
    _clean_axes(axes[0])

    # --- Right: histogram of overall scores ---
    axes[1].hist(df["overall"], bins=10, color=BLUE, edgecolor="white", linewidth=0.5)
    axes[1].set_xlabel("Overall Score")
    axes[1].set_ylabel("Count")
    mean_val = df["overall"].mean()
    axes[1].axvline(x=mean_val, color=RED, linestyle="--", linewidth=0.75)
    legend_hist = [Line2D([0], [0], color=RED, linestyle="--", linewidth=0.75,
                          label=f"Mean = {mean_val:.2f}")]
    axes[1].legend(handles=legend_hist, loc="upper left", frameon=False)
    _clean_axes(axes[1])

    plt.tight_layout()
    _save(fig, "gpt_judge_evaluation.pdf")


# ============================================================
# Figure 3: Tutoring Quality (2x2)
# ============================================================
def plot_tutoring_quality(results_path: str):
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.subplots_adjust(wspace=0.35, hspace=0.40)

    # --- BLEU ---
    axes[0, 0].bar(range(len(df)), df["bleu"], color=BLUE, width=BAR_WIDTH, edgecolor="none")
    axes[0, 0].set_xlabel("Question ID")
    axes[0, 0].set_ylabel("BLEU Score")
    m = df["bleu"].mean()
    axes[0, 0].axhline(y=m, color=RED, linestyle="--", linewidth=0.75)
    from matplotlib.lines import Line2D
    axes[0, 0].legend(handles=[Line2D([0], [0], color=RED, linestyle="--", linewidth=0.75,
                                       label=f"Mean = {m:.3f}")],
                       loc="upper left", frameon=False)
    _clean_axes(axes[0, 0])

    # --- ROUGE-L ---
    axes[0, 1].bar(range(len(df)), df["rouge_l"], color=ORANGE, width=BAR_WIDTH, edgecolor="none")
    axes[0, 1].set_xlabel("Question ID")
    axes[0, 1].set_ylabel("ROUGE-L Score")
    m = df["rouge_l"].mean()
    axes[0, 1].axhline(y=m, color=RED, linestyle="--", linewidth=0.75)
    axes[0, 1].legend(handles=[Line2D([0], [0], color=RED, linestyle="--", linewidth=0.75,
                                       label=f"Mean = {m:.3f}")],
                       loc="upper left", frameon=False)
    _clean_axes(axes[0, 1])

    # --- Response Time ---
    axes[1, 0].bar(range(len(df)), df["response_time"], color=GREEN, width=BAR_WIDTH, edgecolor="none")
    axes[1, 0].set_xlabel("Question ID")
    axes[1, 0].set_ylabel("Response Time (s)")
    _clean_axes(axes[1, 0])

    # --- Response Quality (value labels on bars, no legend) ---
    quality_metrics = ["has_code_block", "has_explanation", "has_example"]
    quality_labels  = ["Code Block", "Explanation", "Example"]
    quality_means   = [df[m].mean() for m in quality_metrics]
    q_colors = [PURPLE, ORANGE, BLUE]
    bars = axes[1, 1].bar(quality_labels, quality_means, color=q_colors, width=BAR_WIDTH, edgecolor="none")
    axes[1, 1].set_ylabel("Proportion")
    axes[1, 1].set_ylim(0, 1.15)
    for bar, val in zip(bars, quality_means):
        axes[1, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                         f"{val:.2f}", ha="center", va="bottom", fontsize=10)
    _clean_axes(axes[1, 1])

    _save(fig, "tutoring_quality.pdf")


# ============================================================
# Figure 4: Ablation Study (1x3)
# ============================================================
def plot_ablation_study(results_path: str):
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    config_labels = {
        "full_system": "Full",
        "no_knowledge_tracking": "w/o KT",
        "no_adaptive_hints": "w/o AH",
        "basic_tutor": "Basic",
    }
    configs = df["config"].unique()
    labels  = [config_labels.get(c, c) for c in configs]
    ab_colors = [BLUE, ORANGE, GREEN, PURPLE]

    # --- Response Time ---
    time_means = [df[df["config"] == c]["response_time"].mean() for c in configs]
    axes[0].bar(labels, time_means, color=ab_colors[:len(configs)], width=BAR_WIDTH, edgecolor="none")
    axes[0].set_ylabel("Response Time (s)")
    axes[0].tick_params(axis="x", labelsize=11)
    _clean_axes(axes[0])

    # --- Success Rate ---
    success_means = [df[df["config"] == c]["success"].mean() for c in configs]
    axes[1].bar(labels, success_means, color=ab_colors[:len(configs)], width=BAR_WIDTH, edgecolor="none")
    axes[1].set_ylabel("Success Rate")
    axes[1].set_ylim(0, 1)
    axes[1].tick_params(axis="x", labelsize=11)
    _clean_axes(axes[1])

    # --- Response Length ---
    len_means = [df[df["config"] == c]["response_length"].mean() for c in configs]
    axes[2].bar(labels, len_means, color=ab_colors[:len(configs)], width=BAR_WIDTH, edgecolor="none")
    axes[2].set_ylabel("Response Length (chars)")
    axes[2].tick_params(axis="x", labelsize=11)
    _clean_axes(axes[2])

    plt.tight_layout()
    _save(fig, "ablation_study.pdf")


# ============================================================
# Figure 5: Prompt Comparison (2x2)
# ============================================================
def plot_prompt_comparison(results_path: str):
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    strategies = df["strategy"].unique()
    str_colors = [BLUE, ORANGE, GREEN]

    # Word count
    word_means = [df[df["strategy"] == s]["word_count"].mean() for s in strategies]
    axes[0, 0].bar(strategies, word_means, color=str_colors[:len(strategies)], width=BAR_WIDTH, edgecolor="none")
    axes[0, 0].set_ylabel("Words")
    _clean_axes(axes[0, 0])

    # Response time
    time_means = [df[df["strategy"] == s]["response_time"].mean() for s in strategies]
    axes[0, 1].bar(strategies, time_means, color=str_colors[:len(strategies)], width=BAR_WIDTH, edgecolor="none")
    axes[0, 1].set_ylabel("Seconds")
    _clean_axes(axes[0, 1])

    # Code inclusion
    code_means = [df[df["strategy"] == s]["has_code"].mean() for s in strategies]
    axes[1, 0].bar(strategies, code_means, color=str_colors[:len(strategies)], width=BAR_WIDTH, edgecolor="none")
    axes[1, 0].set_ylabel("Proportion")
    _clean_axes(axes[1, 0])

    # Completeness
    comp_means = [df[df["strategy"] == s]["completeness_score"].mean() for s in strategies]
    axes[1, 1].bar(strategies, comp_means, color=str_colors[:len(strategies)], width=BAR_WIDTH, edgecolor="none")
    axes[1, 1].set_ylabel("Score")
    _clean_axes(axes[1, 1])

    plt.tight_layout()
    _save(fig, "prompt_comparison.pdf")


# ============================================================
# Figure 6: System vs Baseline
# ============================================================
def plot_comparison(results_path: str):
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    metric_labels = ["Accuracy", "Clarity", "Educational", "Completeness", "Overall"]
    sys_means  = [df[f"sys_{m}"].mean() for m in metrics]
    base_means = [df[f"base_{m}"].mean() for m in metrics]

    x = np.arange(len(metrics))
    w = 0.35

    axes[0].bar(x - w/2, sys_means, w, label="CodeTutor-ITS", color=BLUE, edgecolor="none")
    axes[0].bar(x + w/2, base_means, w, label="Raw LLM", color=ORANGE, edgecolor="none")
    axes[0].set_ylabel("Score (1–5)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metric_labels)
    axes[0].set_ylim(0, 5.5)
    axes[0].axhline(y=3, color="gray", linestyle=":", linewidth=0.75, alpha=0.6)
    axes[0].legend(frameon=False)
    _clean_axes(axes[0])

    # Win/Loss/Tie
    wins   = sum(1 for m in metrics if df[f"sys_{m}"].mean() > df[f"base_{m}"].mean())
    losses = sum(1 for m in metrics if df[f"sys_{m}"].mean() < df[f"base_{m}"].mean())
    ties   = len(metrics) - wins - losses
    axes[1].pie([wins, losses, ties],
                labels=["System Wins", "Baseline Wins", "Tie"],
                autopct="%1.0f%%",
                colors=[GREEN, ORANGE, "#cccccc"],
                startangle=90,
                textprops={"fontsize": 8})
    _clean_axes(axes[1])
    axes[1].spines["bottom"].set_visible(False)
    axes[1].spines["left"].set_visible(False)

    plt.tight_layout()
    _save(fig, "system_vs_baseline.pdf")


# ============================================================
# Figure 7: LoRA Fine-tune Comparison
# ============================================================
def plot_finetune_comparison(results_path: str):
    df = pd.read_csv(results_path)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    metrics = ["accuracy", "clarity", "educational", "completeness", "overall"]
    metric_labels = ["Accuracy", "Clarity", "Edu.", "Comp.", "Overall"]
    base_means = [df[f"base_{m}"].mean() for m in metrics]
    ft_means   = [df[f"ft_{m}"].mean() for m in metrics]

    x = np.arange(len(metrics))
    w = 0.35

    axes[0].bar(x - w/2, base_means, w, label="Base Model", color="#999999", edgecolor="none")
    axes[0].bar(x + w/2, ft_means, w, label="LoRA Fine-tuned", color=GREEN, edgecolor="none")
    axes[0].set_ylabel("Score (1–5)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metric_labels)
    axes[0].set_ylim(0, 5.5)
    axes[0].axhline(y=3, color="gray", linestyle=":", linewidth=0.75, alpha=0.6)
    axes[0].legend(frameon=False, loc="lower right")
    _clean_axes(axes[0])

    # Improvement
    improvements = [ft_means[i] - base_means[i] for i in range(len(metrics))]
    imp_colors = [GREEN if v >= 0 else ORANGE for v in improvements]
    bars = axes[1].bar(metric_labels, improvements, color=imp_colors, width=BAR_WIDTH, edgecolor="none")
    axes[1].set_ylabel("Score Difference")
    axes[1].axhline(y=0, color="black", linewidth=0.75)
    for bar, v in zip(bars, improvements):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                     f"{v:+.2f}", ha="center", va="bottom", fontsize=8)
    _clean_axes(axes[1])

    plt.tight_layout()
    _save(fig, "finetune_comparison.pdf")


if __name__ == "__main__":
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
