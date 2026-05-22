# Round 5 Pre-Submission Review Report

**Date**: 2026-05-22
**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target Journal**: Applied Sciences (MDPI)
**Reviewer**: Internal pre-submission review (Round 5)
**Previous Rounds**: R1: 6.25 | R2: 7.80 | R3: 8.00 | R4: 8.20 | R5: below

---

## Overall Verdict: Accept (Strong Submission)

**Weighted Score: 8.5/10**

| Dimension | Weight | R1 | R2 | R3 | R4 | R5 | Notes |
|-----------|--------|-----|-----|-----|-----|-----|-------|
| Originality | 20% | 6.0 | 7.0 | 7.5 | 8.0 | 8.0 | Pedagogical theory + cross-family validation |
| Methodological Rigor | 25% | 5.5 | 7.5 | 7.5 | 8.0 | 8.5 | n=15 Exp 2, significant p-values, effect sizes |
| Evidence Sufficiency | 25% | 6.0 | 8.0 | 8.0 | 8.5 | 9.0 | Expanded Exp 2, per-topic/difficulty analysis |
| Argument Coherence | 15% | 7.0 | 8.0 | 8.5 | 8.5 | 8.5 | Consistent narrative across all sections |
| Writing Quality | 15% | 7.5 | 8.0 | 8.0 | 8.0 | 8.0 | 39 references, proper hedging |

---

## Score Trajectory

```
R1: 6.25 ████████████████████░░░░░░░░░░░░░░░░░░░░ Major Revision
R2: 7.80 ██████████████████████████████████░░░░░░░░ Minor Revision
R3: 8.00 ████████████████████████████████████░░░░░░ Accept
R4: 8.20 █████████████████████████████████████░░░░░ Accept (Strong)
R5: 8.50 ██████████████████████████████████████░░░░ Accept (Strong)
```

---

## Round 5 Key Improvement: Exp 2 Sample Expansion

**Before (n=5 per strategy):**
- CoT vs few-shot: W=15.0, p=0.031 (significant)
- CoT vs zero-shot: W=6.0, p=0.125 (not significant)

**After (n=15 per strategy):**
- CoT vs few-shot: W=5.0, p=0.012 (significant)
- CoT vs zero-shot: W=10.5, p=0.044 (significant)

**Impact**: CoT now significantly outperforms BOTH alternatives, strengthening the paper's recommendation for chain-of-thought prompting in educational contexts.

---

## Updated Exp 2 Results Table

| Strategy | Words | Time (s) | Code (%) | Steps (%) | Completeness |
|----------|-------|----------|----------|-----------|--------------|
| Zero-shot | 158.4 | 36.59 | 93.3 | 73.3 | 0.63 |
| Few-shot | 165.5 | 32.89 | 100 | 86.7 | 0.67 |
| Chain-of-thought | 123.8 | 30.54 | 100 | 100 | 0.83 |

**Key findings:**
1. CoT achieves highest completeness (0.83, p<0.05)
2. CoT is fastest (30.54s vs 36.59s for zero-shot, p=0.004)
3. CoT always includes code examples and step-by-step structure (100%)

---

## All Issues Resolved (25 total across 5 rounds)

| Round | Issues | Status |
|-------|--------|--------|
| R1 | 5 critical (stats, LoRA, Table 6, Discussion, human eval) | All RESOLVED |
| R2 | 5 major (sample size, metric hierarchy, Bayesian naming, latency, refs) | All RESOLVED |
| R2 Minor | 5 minor (contribution order, n=42, success criteria, ref33, Conclusions) | All RESOLVED |
| R4 | 4 enhancements (Related Work, pedagogical theory, deployment, error analysis) | All DONE |
| R5 | 6 improvements (Exp 2 expansion from n=5 to n=15) | All DONE |

---

## Submission Readiness: PASS

All checklist items pass. Paper is ready for MDPI Applied Sciences submission.

**Strengths:**
1. Comprehensive evaluation with 5 experiments
2. Cross-family judge validation (Qwen2.5-72B + LLaMA-3-70B)
3. Statistically significant results with effect sizes
4. Pedagogical theory grounding (ZPD, scaffolded instruction, worked examples)
5. Practical deployment considerations
6. Open-source, reproducible system
