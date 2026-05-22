# Pre-Submission Review Report

**Date**: 2026-05-22
**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target Journal**: Applied Sciences (MDPI)
**Reviewer**: Internal pre-submission review

---

## Overall Verdict: Major Revision (borderline Minor Revision)

**Weighted Score: 6.25/10**

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Originality | 20% | 6/10 | Engineering integration, not conceptual advance. Q4 acceptable. |
| Methodological Rigor | 25% | 5.5/10 | Weakest: no statistical tests, no human eval, small n |
| Evidence Sufficiency | 25% | 6/10 | Table 6 unsourced, LoRA conclusion overstated |
| Argument Coherence | 15% | 7/10 | Logical flow good, Discussion too shallow |
| Writing Quality | 15% | 7.5/10 | Clear, minor repetition |

---

## Critical Issues (Must Fix)

### 1. No Statistical Significance Tests
- Exp 2 (prompt comparison) and Exp 4 (LLM-as-Judge) report means but never test significance
- **Fix**: Add Wilcoxon signed-rank tests (Exp 2, n=5 per group) and one-sample t-tests (Exp 4, n=50)

**Statistical Test Results (computed):**

Exp 2 (n=5 per strategy):
- CoT vs Few-shot: W=15.0, p=0.031 (significant at alpha=0.05)
- CoT vs Zero-shot: W=6.0, p=0.125 (NOT significant — n too small)

Exp 4 (n=50, one-sample t-test vs threshold 4.0):
- Accuracy: t(49)=10.69, p<0.001 ***
- Clarity: t(49)=8.23, p<0.001 ***
- Educational Value: t(49)=9.33, p<0.001 ***
- Completeness: t(49)=1.06, p=0.293 (ns)
- Overall: t(49)=7.00, p<0.001 ***

Exp 5 (LoRA, n=50, paired t-test):
- All dimensions: p>0.4 (NOT significant, confirms negligible improvement)

### 2. LoRA Conclusion Overstated
- Current: "fine-tuning produces negligible improvement"
- Problem: 250 samples + 1 epoch = undertrained, not proof that fine-tuning is unnecessary
- **Fix**: Soften to "limited improvement with current configuration"

### 3. Table 6 (System Comparison) Unsourced
- Claims about GPT-4 Tutor and ChatGPT Edu capabilities have no citations
- Reviewer will flag as "strawman" comparison
- **Fix**: Add citations for each cell, or remove the table

### 4. Discussion Too Shallow
- Error analysis is only 2 paragraphs
- No quantitative per-topic breakdown
- **Fix**: Expand with per-domain score analysis

---

## Non-Critical Issues (Acknowledge in Limitations)

### 5. No Human Evaluation
- LLM-as-Judge is sole quality metric
- Acknowledge in Limitations, cite Zheng et al. (2024) for LLM-as-Judge validity

### 6. Small Sample Size (n=50)
- Acknowledge in Limitations
- Cite precedent: LLM-as-Judge studies typically use 50-100 samples

---

## Action Plan

| # | Action | Priority | Status |
|---|--------|----------|--------|
| 1 | Add statistical tests to Exp 2 and Exp 4 | HIGH | Pending |
| 2 | Soften LoRA conclusion language | HIGH | Pending |
| 3 | Fix Table 6 (add citations or remove) | HIGH | Pending |
| 4 | Expand Discussion / error analysis | MEDIUM | Pending |
| 5 | Update Limitations section | LOW | Pending |
