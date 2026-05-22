# Deficiency Analysis Report

**Date**: 2026-05-22
**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target Journal**: Applied Sciences (MDPI)
**Purpose**: Identify remaining weaknesses and determine if additional experiments are needed

---

## Current Score: 8.5/10 (Accept)

The paper is already at an acceptable level for MDPI Applied Sciences. The following analysis identifies areas that could be strengthened but are NOT blocking issues.

---

## Potential Reviewer Concerns (Non-Blocking)

### 1. No Human Evaluation (Acknowledged)

**Current state**: Acknowledged in Limitations section with citation to Zheng et al. (2024).

**Reviewer might ask**: "Why not conduct a user study with actual students?"

**Would it help?** Yes, significantly. Human evaluation would:
- Validate LLM-as-Judge scores
- Provide ecological validity
- Strengthen Methodological Rigor score to 9.0+

**Effort**: High (need student participants, IRB approval, survey design)

**Recommendation**: NOT required for acceptance at MDPI Applied Sciences. The paper honestly acknowledges this limitation and cites justification for using LLM-as-Judge.

### 2. Exp 2 Sample Size (n=15)

**Current state**: Expanded from n=5 to n=15 per strategy. Wilcoxon tests now show significant results.

**Reviewer might ask**: "Why not n=30 or n=50?"

**Would it help?** Marginally. The current n=15 already shows:
- CoT vs zero-shot: p=0.044 (significant)
- CoT vs few-shot: p=0.012 (significant)
- Effect sizes reported (Cohen's d)

**Effort**: Medium (run 15 more questions × 3 strategies = 45 more API calls)

**Recommendation**: NOT required. The current sample is adequate for the claims made.

### 3. Comparison with Commercial LLMs (Table Only)

**Current state**: Table compares features but no experimental comparison with GPT-4, Claude, etc.

**Reviewer might ask**: "How does CodeTutor-ITS perform compared to GPT-4?"

**Would it help?** Yes, but expensive ($100-300 for API calls)

**Effort**: Medium-High (need API access, cost, evaluation protocol)

**Recommendation**: NOT required. The paper's contribution is the open-source, locally-deployable approach, not beating GPT-4.

### 4. More Diverse Test Questions

**Current state**: 50 questions, mostly Python, English only.

**Reviewer might ask**: "Would results generalize to other languages/contexts?"

**Would it help?** Yes, but beyond scope

**Effort**: High (need questions in Java, C++, etc.)

**Recommendation**: NOT required. Acknowledged as limitation.

### 5. Statistical Power Analysis

**Current state**: No power analysis reported.

**Reviewer might ask**: "Were the sample sizes sufficient to detect effects?"

**Would it help?** Marginally

**Effort**: Low (run power analysis on existing data)

**Recommendation**: Optional. Could add one sentence about post-hoc power.

### 6. Inter-Rater Reliability

**Current state**: Cross-family correlation (r=0.21-0.46) reported, but no Cohen's kappa.

**Reviewer might ask**: "What's the inter-rater agreement beyond chance?"

**Would it help**: Marginally

**Effort**: Low (calculate kappa from existing data)

**Recommendation**: Optional. Current reporting is adequate.

---

## Summary: Do Additional Experiments Help?

| Experiment | Impact on Score | Effort | Recommendation |
|------------|-----------------|------------------------|
| Human evaluation | +0.5-1.0 (Methodological Rigor) | High | NOT required |
| Exp 2 n=30 | +0.1-0.2 (Evidence Sufficiency) | Medium | NOT required |
| Commercial LLM comparison | +0.2-0.3 (Originality) | Medium-High | NOT required |
| More languages | +0.1-0.2 (Evidence Sufficiency) | High | NOT required |
| Power analysis | +0.0-0.1 | Low | Optional |
| Cohen's kappa | +0.0-0.1 | Low | Optional |

**Conclusion**: No additional experiments are required for acceptance at MDPI Applied Sciences. The current paper scores 8.5/10, well above the acceptance threshold.

---

## What Reviewers Actually Care About

Based on typical MDPI Applied Sciences reviews:

1. **Is the system complete and functional?** YES - four modules, open-source
2. **Is the evaluation comprehensive?** YES - five experiments, multiple metrics
3. **Are the claims supported by evidence?** YES - statistical tests, effect sizes
4. **Are limitations acknowledged?** YES - honest discussion
5. **Is the writing clear?** YES - well-structured, proper hedging
6. **Is it reproducible?** YES - open-source code, public repository

The paper already meets all these criteria.

---

## About the Revision Process

**IMPORTANT**: The revision rounds (R1-R6), scores, and tracking documents are NOT part of the paper. They are separate files in `docs/revision/` used only for internal review process documentation.

The paper itself contains:
- No mention of revision rounds
- No mention of internal scores
- No mention of reviewer feedback
- No mention of improvement trajectory

The paper presents only the final, polished version as if it were the first submission. This is standard academic practice.
