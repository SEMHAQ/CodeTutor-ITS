# Round 6 Pre-Submission Review Report

**Date**: 2026-05-22
**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target Journal**: Applied Sciences (MDPI)
**Reviewer**: Internal pre-submission review (Round 6)
**Previous Rounds**: R1: 6.25 | R2: 7.80 | R3: 8.00 | R4: 8.20 | R5: 8.50 | R6: below

---

## Overall Verdict: Accept (Strong Submission)

**Weighted Score: 8.5/10**

| Dimension | Weight | R1 | R2 | R3 | R4 | R5 | R6 | Notes |
|-----------|--------|-----|-----|-----|-----|-----|-----|-------|
| Originality | 20% | 6.0 | 7.0 | 7.5 | 8.0 | 8.0 | 8.0 | Integrated system + cross-family validation |
| Methodological Rigor | 25% | 5.5 | 7.5 | 7.5 | 8.0 | 8.5 | 8.5 | n=15 Exp 2, statistical tests, effect sizes |
| Evidence Sufficiency | 25% | 6.0 | 8.0 | 8.0 | 8.5 | 9.0 | 9.0 | Per-topic/difficulty, concrete error patterns |
| Argument Coherence | 15% | 7.0 | 8.0 | 8.5 | 8.5 | 8.5 | 8.5 | Theory → system → evaluation → implications |
| Writing Quality | 15% | 7.5 | 8.0 | 8.0 | 8.0 | 8.0 | 8.0 | 39 references, proper hedging, clear structure |

---

## Score Trajectory

```
R1: 6.25 ████████████████████░░░░░░░░░░░░░░░░░░░░ Major Revision
R2: 7.80 ██████████████████████████████████░░░░░░░░ Minor Revision
R3: 8.00 ████████████████████████████████████░░░░░░ Accept
R4: 8.20 █████████████████████████████████████░░░░░ Accept (Strong)
R5: 8.50 ██████████████████████████████████████░░░░ Accept (Strong)
R6: 8.50 ██████████████████████████████████████░░░░ Accept (Strong)
```

---

## Strengths

### 1. Comprehensive Evaluation Pipeline
Five experiments with different methodologies provide thorough coverage:
- Exp 1: LLM-as-Judge (primary quality metric)
- Exp 2: Prompt strategy comparison (n=15, statistically significant)
- Exp 3: Ablation study (module contribution)
- Exp 4: BLEU/ROUGE-L (supplementary metrics)
- Exp 5: LoRA fine-tuning analysis

### 2. Statistical Rigor
All claims backed by appropriate tests:
- One-sample t-tests for LLM-as-Judge scores
- Wilcoxon signed-rank tests for Exp 2 (n=15)
- Paired t-tests for Exp 5 (LoRA comparison)
- Effect sizes reported (Cohen's d)
- p-values and test statistics throughout

### 3. Cross-Family Validation
Using both Qwen2.5-72B and LLaMA-3-70B as judges addresses same-family bias:
- n=42 valid paired observations
- Moderate inter-judge correlations (r=0.21-0.46)
- Consistent quality ordering across model families

### 4. Pedagogical Theory Grounding
System design based on established theories:
- Vygotsky's Zone of Proximal Development (ZPD)
- Scaffolded instruction (Wood et al.)
- Worked example effect (Sweller)

### 5. Practical Relevance
Addresses real concerns for educational institutions:
- Zero operational cost (local deployment)
- Data privacy (no cloud APIs)
- Modular architecture for incremental adoption
- Quantization strategies for resource-constrained settings

### 6. Reproducibility
- Open-source code on GitHub
- Public repository with experimental data
- Local deployment on consumer GPU (RTX 3090)

---

## Detailed Assessment by Dimension

### Originality (8.0/10)
**Strengths:**
- Integrated system combining adaptive hints, knowledge tracking, and exercise generation
- Cross-family validation methodology for LLM-as-Judge
- Four-level progressive hint system
- Simplified probabilistic knowledge tracking

**Minor observations:**
- Individual components (adaptive hints, knowledge tracking) exist in prior work
- The contribution is more in integration than in novel algorithms

### Methodological Rigor (8.5/10)
**Strengths:**
- Five complementary experiments
- Appropriate statistical tests for each experiment
- Cross-family validation mitigates same-family bias
- Operationalized success criteria for ablation study
- Expanded Exp 2 from n=5 to n=15

**Minor observations:**
- Exp 2 still uses relatively small sample (n=15)
- No human evaluation (acknowledged in Limitations)

### Evidence Sufficiency (9.0/10)
**Strengths:**
- n=50 for main experiments
- n=15 per strategy for Exp 2
- Per-topic analysis (5 domains)
- Per-difficulty analysis (easy/medium/hard)
- Concrete error patterns identified
- Effect sizes reported

**Minor observations:**
- Test dataset limited to 50 questions
- Single model evaluation (7B only)

### Argument Coherence (8.5/10)
**Strengths:**
- Clear narrative flow: problem → solution → evaluation → implications
- Consistent experiment ordering across Abstract, Setup, and Results
- LLM-as-Judge as primary metric with BLEU/ROUGE as supplementary
- Theory → system design → evaluation → practical implications

**Minor observations:**
- Some repetition between Abstract and Conclusions

### Writing Quality (8.0/10)
**Strengths:**
- 39 references (adequate for MDPI Applied Sciences)
- Proper hedging throughout
- Clear section structure
- MDPI LaTeX template compliance
- Professional figures and tables

**Minor observations:**
- Some verbose paragraphs in Discussion
- Occasional redundancy in explanations

---

## Issues Resolved Across All Rounds

| Round | Issues | Status |
|-------|--------|--------|
| R1 | 5 critical (stats, LoRA, Table 6, Discussion, human eval) | All RESOLVED |
| R2 | 5 major (sample size, metric hierarchy, Bayesian naming, latency, refs) | All RESOLVED |
| R2 Minor | 5 minor (contribution order, n=42, success criteria, ref33, Conclusions) | All RESOLVED |
| R4 | 4 enhancements (Related Work, pedagogical theory, deployment, error analysis) | All DONE |
| R5 | 6 improvements (Exp 2 expansion from n=5 to n=15) | All DONE |

**Total: 25 issues identified and resolved across 6 rounds.**

---

## Submission Checklist (Final)

| Criterion | Status | Notes |
|-----------|--------|-------|
| MDPI LaTeX template | PASS | Uses Definitions/mdpi class |
| Abstract (~250 words) | PASS | Well-structured, matches Results |
| Reference count | PASS | 39 references |
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

## Remaining Observations (Non-Blocking)

These are noted for awareness but do NOT require changes before submission:

1. **Exp 2 sample size (n=15)**: Expanded from n=5, now with significant results. A reviewer may suggest larger n, but the Wilcoxon tests are appropriate and results are clear.

2. **No human evaluation**: Acknowledged in Limitations with citation to Zheng et al. (2024). Common in LLM-as-Judge studies.

3. **Single model evaluation (7B only)**: Acknowledged as limitation. Acceptable for target journal.

4. **Test dataset size (50 questions)**: Acknowledged in Limitations. Adequate for system evaluation.

---

## Final Recommendation

**Submit to MDPI Applied Sciences.** The paper scores 8.5/10, well above the Accept threshold. All 25 issues from six review rounds have been resolved. No blocking issues remain.

The paper makes a solid contribution: (1) a complete, open-source tutoring system; (2) a four-level adaptive hint mechanism grounded in pedagogical theory; (3) comprehensive evaluation with cross-family validation; (4) statistically significant results with effect sizes; and (5) practical insights for deploying LLMs in education. The writing is clear, the methodology is sound, and the limitations are honestly acknowledged.

**Estimated review outcome**: Accept with minor revisions (if any).
