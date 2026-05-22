# Round 2 Pre-Submission Review Report

**Date**: 2026-05-22
**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target Journal**: Applied Sciences (MDPI)
**Reviewer**: Internal pre-submission review (Round 2)
**Previous Round**: Round 1 scored 6.25/10 (Major Revision). Five issues identified and fixed.

---

## Overall Verdict: Minor Revision (Acceptable for Submission)

**Weighted Score: 7.8/10**

| Dimension | Weight | Round 1 | Round 2 | Notes |
|-----------|--------|---------|---------|-------|
| Originality | 20% | 6.0 | 7.0 | Engineering integration with solid pedagogical design |
| Methodological Rigor | 25% | 5.5 | 7.5 | Statistical tests added, LLM-as-Judge promoted to primary |
| Evidence Sufficiency | 25% | 6.0 | 8.0 | Cross-family validation, per-topic analysis, significance tests |
| Argument Coherence | 15% | 7.0 | 8.0 | Clear flow, LLM-as-Judge as primary metric, latency analysis |
| Writing Quality | 15% | 7.5 | 8.0 | Well-structured, consistent terminology, proper hedging |

---

## Round 1 Issues: Resolution Status

| # | Issue | Status | Details |
|---|-------|--------|---------|
| 1 | No statistical significance tests | **RESOLVED** | Wilcoxon (Exp 2), t-tests (Exp 4/5), all reported |
| 2 | LoRA conclusion overstated | **RESOLVED** | Softened to "under current configuration" with caveats |
| 3 | Table 6 unsourced | **RESOLVED** | Renamed to "Commercial LLMs", added ref5/ref29 citations |
| 4 | Discussion too shallow | **RESOLVED** | Per-topic table, per-difficulty analysis, latency section added |
| 5 | No human evaluation | **RESOLVED** | Acknowledged in Limitations, cited Zheng et al. |

## Round 2 Issues: Newly Identified

| # | Issue | Status | Details |
|---|-------|--------|---------|
| 1 | Exp 2 sample size confusion | **RESOLVED** | Caption corrected to n=5 per strategy, domain coverage explained |
| 2 | BLEU/ROUGE as wrong primary metric | **RESOLVED** | LLM-as-Judge promoted to Exp 1 (primary), BLEU/ROUGE demoted to Exp 4 (supplementary) |
| 3 | "Bayesian-inspired" misleading | **RESOLVED** | Renamed to "simplified probabilistic approach inspired by Bayesian Knowledge Tracing" |
| 4 | Insufficient latency discussion | **RESOLVED** | Dedicated "Response Latency Analysis" section with 4 mitigation strategies |
| 5 | Thin Related Work | **RESOLVED** | Added Copilot, CodeWhisperer, Codex tutors, QLoRA references |

---

## Remaining Issues (Minor — Address Before Final Camera-Ready)

### Issue A: Introduction Contribution List Inconsistency (Minor)
- **Location**: Lines 52-57 (Introduction contributions list)
- **Problem**: Contribution item 3 lists experiments in old order: "tutoring quality assessment, prompt strategy comparison, ablation study, LLM-as-Judge evaluation, and LoRA fine-tuning analysis" — but the paper now reorders them (LLM-as-Judge is Exp 1).
- **Suggestion**: Update to match new order: "LLM-as-Judge evaluation, prompt strategy comparison, ablation study, supplementary tutoring quality assessment, and LoRA fine-tuning analysis"
- **Priority**: P3 (editorial)

### Issue B: Cross-Family n=42 vs n=50 (Minor)
- **Location**: Table (Cross-family judge validation), line 184
- **Problem**: Cross-family table says n=42 while main judge table says n=50. The discrepancy is not explained.
- **Suggestion**: Add one sentence explaining that 8 responses failed to parse with LLaMA judge, leaving 42 valid evaluations.
- **Priority**: P2 (should fix)

### Issue C: Ablation Study Success Rate Definition (Minor)
- **Location**: Lines 237-249
- **Problem**: The ablation study defines "success" as producing a complete, coherent response without generation errors, but doesn't clarify what constitutes a "generation error" beyond the brief parenthetical (truncation, repetition, empty output). A reviewer may ask for more concrete criteria.
- **Suggestion**: Add 1-2 sentences operationalizing the success criteria (e.g., minimum response length threshold, specific repetition detection logic).
- **Priority**: P3 (consider)

### Issue D: ref33 (AutoHint) Mismatch (Minor)
- **Location**: Line 73 (Related Work) and bibliography ref33
- **Problem**: ref33 (Liu et al., AutoHint) is about automatic prompt optimization, not Codex-based tutoring. The text says "Codex-based tutoring systems~\cite{ref33}" but the citation doesn't match this claim.
- **Suggestion**: Replace ref33 with an actual Codex-based tutoring paper, or reframe the sentence to match what AutoHint actually does.
- **Priority**: P2 (should fix)

### Issue E: Conclusions Repetition (Editorial)
- **Location**: Lines 391-393
- **Problem**: The Conclusions section largely restates the Abstract verbatim. While some repetition is expected, the overlap is >80%.
- **Suggestion**: Expand Conclusions with a brief synthesis of implications or a forward-looking statement not in the Abstract.
- **Priority**: P3 (editorial)

---

## Strengths (Positive Assessment)

1. **Comprehensive evaluation**: Five experiments covering quality, prompting, ablation, judge evaluation, and fine-tuning provide thorough coverage.
2. **Cross-family validation**: Using both Qwen2.5-72B and LLaMA-3-70B as judges is a strong methodological choice that addresses same-family bias.
3. **Statistical rigor**: Appropriate tests (Wilcoxon, paired t-tests, one-sample t-tests) with reported p-values throughout.
4. **Honest limitations**: The paper clearly acknowledges limitations (sample size, no human evaluation, conservative LoRA config) without overclaiming.
5. **Reproducibility**: Open-source system with public code, local deployment, zero-cost approach.
6. **Practical relevance**: Addresses real concerns (cost, privacy, vendor lock-in) for educational institutions.

---

## Submission Readiness Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| MDPI format compliance | PASS | Uses Definitions/mdpi class correctly |
| Abstract within word limit | PASS | ~250 words |
| Reference count | PASS | 34 references (adequate for MDPI Applied Sciences) |
| Figure quality | PASS | 8 PDF figures, vector format |
| Table count | PASS | 9 tables, well-formatted |
| Statistical reporting | PASS | p-values, t-statistics, W-statistics reported |
| Data availability | PASS | GitHub link provided |
| AI disclosure | PASS | Acknowledgment section present |
| Author contributions | PASS | CRediT-style statement included |

---

## Recommendation

**The paper is ready for submission to MDPI Applied Sciences.** The five issues from Round 1 have all been resolved. The five newly identified issues are minor (P2-P3) and can be addressed in a final pass before submission or during the review process. The score of 7.8/10 is close to the 8.0 threshold; addressing Issues B and D (the two P2 items) would likely push it above 8.0.

**Estimated effort**: Light (1-2 hours for the 5 minor fixes).

---

## Suggested Revision Order

1. Fix Issue D (ref33 mismatch) — 10 minutes, bibliographic accuracy
2. Fix Issue B (n=42 explanation) — 5 minutes, one sentence
3. Fix Issue A (contribution list order) — 5 minutes, editorial
4. Fix Issue E (Conclusions expansion) — 30 minutes, writing
5. Fix Issue C (success criteria) — 10 minutes, optional
