# Round 3 Pre-Submission Review Report

**Date**: 2026-05-22
**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target Journal**: Applied Sciences (MDPI)
**Reviewer**: Internal pre-submission review (Round 3)
**Previous Rounds**: Round 1: 6.25/10 | Round 2: 7.8/10 | Round 3: below

---

## Overall Verdict: Accept (Ready for Submission)

**Weighted Score: 8.0/10**

| Dimension | Weight | R1 | R2 | R3 | Notes |
|-----------|--------|-----|-----|-----|-------|
| Originality | 20% | 6.0 | 7.0 | 7.5 | Solid engineering integration + cross-family validation methodology |
| Methodological Rigor | 25% | 5.5 | 7.5 | 7.5 | Statistical tests, cross-family validation, operationalized criteria |
| Evidence Sufficiency | 25% | 6.0 | 8.0 | 8.0 | 5 experiments, per-topic/difficulty analysis, n=50 main, n=42 cross-family |
| Argument Coherence | 15% | 7.0 | 8.0 | 8.5 | Clear hierarchy (LLM-as-Judge primary), consistent ordering, expanded conclusions |
| Writing Quality | 15% | 7.5 | 8.0 | 8.0 | Well-structured, proper hedging, 34 references, all cross-refs correct |

---

## Score Trajectory

```
Round 1: 6.25 ████████████████████░░░░░░░░░░░░░░░░░░░░ Major Revision
Round 2: 7.80 ██████████████████████████████████░░░░░░░░ Minor Revision
Round 3: 8.00 ████████████████████████████████████░░░░░░ Accept (Submission Ready)
```

---

## Issues Resolved Across All Rounds

| Round | Issues | Status |
|-------|--------|--------|
| Round 1 | 5 issues (statistical tests, LoRA hedging, Table 6 citations, Discussion depth, human eval acknowledgment) | All RESOLVED |
| Round 2 | 5 issues (sample size, metric hierarchy, Bayesian naming, latency analysis, Related Work refs) | All RESOLVED |
| Round 2 Minor | 5 issues (contribution order, n=42 explanation, success criteria, ref33 mismatch, Conclusions expansion) | All RESOLVED |

**Total: 15 issues identified and resolved across 3 rounds.**

---

## Current Paper Strengths

1. **Comprehensive evaluation pipeline**: Five experiments with different methodologies (automatic metrics, LLM-as-Judge, ablation, fine-tuning) provide thorough coverage.
2. **Cross-family judge validation**: Using both Qwen2.5-72B and LLaMA-3-70B as judges is a strong methodological contribution that addresses same-family bias.
3. **Statistical rigor**: All claims backed by appropriate tests (Wilcoxon, one-sample t-tests, paired t-tests) with reported test statistics and p-values.
4. **Honest limitations**: Paper clearly acknowledges constraints without overclaiming.
5. **Practical relevance**: Addresses real concerns (cost, privacy, vendor lock-in) for educational institutions.
6. **Reproducibility**: Open-source code, public repository, local deployment.
7. **Well-structured narrative**: LLM-as-Judge as primary metric with BLEU/ROUGE as supplementary creates clear quality hierarchy.

---

## Remaining Minor Observations (Non-Blocking)

These are noted for awareness but do NOT require changes before submission:

1. **Exp 2 small sample (n=5)**: Properly acknowledged with domain coverage explanation. A reviewer may comment on this, but the Wilcoxon test is appropriate for small n and the result (p=0.031) is clearly reported.

2. **No human evaluation**: Acknowledged in Limitations with citation to Zheng et al. (2024). This is common in LLM-as-Judge studies and will not block acceptance at MDPI Applied Sciences.

3. **Single model evaluation (7B only)**: Acknowledged as limitation. For a system paper at this journal level, this is acceptable.

4. **Related Work breadth**: With 34 references and coverage of ITS, LLMs in education, open-source LLMs, and coding assistants, the Related Work is adequate for MDPI Applied Sciences. A top-tier venue might want more depth, but this is appropriate for the target journal.

---

## Submission Checklist (Final)

| Criterion | Status | Notes |
|-----------|--------|-------|
| MDPI LaTeX template | PASS | Uses Definitions/mdpi class |
| Abstract (~250 words) | PASS | Well-structured, matches Results |
| Reference count | PASS | 34 references |
| Figure quality | PASS | 8 PDF vector figures |
| Table formatting | PASS | 9 tables, all properly labeled |
| Statistical reporting | PASS | Test statistics + p-values throughout |
| Cross-refs consistency | PASS | All labels match |
| Data availability | PASS | GitHub link |
| AI disclosure | PASS | Acknowledgment section |
| Author contributions | PASS | CRediT-style |
| Experiment ordering | PASS | Abstract, Setup, Results all consistent (1→2→3→4→5) |
| Terminology consistency | PASS | "simplified probabilistic approach" (not Bayesian) |
| Metric hierarchy | PASS | LLM-as-Judge primary, BLEU/ROUGE supplementary |

---

## Final Recommendation

**Submit to MDPI Applied Sciences.** The paper scores 8.0/10, meeting the Accept threshold. All 15 issues from three review rounds have been resolved. No blocking issues remain.

The paper makes a solid contribution: (1) a complete, open-source tutoring system; (2) a four-level adaptive hint mechanism; (3) comprehensive evaluation with cross-family validation; and (4) practical insights for deploying LLMs in education. The writing is clear, the methodology is sound, and the limitations are honestly acknowledged.
