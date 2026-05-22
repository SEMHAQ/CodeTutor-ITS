# Revision Tracking Template

## Paper Information

| Field | Value |
|-------|-------|
| Paper Title | Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education |
| Revision Round | 5 (Final pre-submission) |
| Date | 2026-05-22 |
| Previous Decision | Round 4: Accept (8.2/10) |
| Target Journal | Applied Sciences (MDPI) |
| Current Score | 8.5/10 (Strong Accept — ready for submission) |

---

## Revision Tracking Table — Round 1 Issues (All Resolved)

| # | Issue Description | Reviewer | Type | Section | Resolution Summary | Location of Change | Status |
|---|-------------------|----------|------|---------|-------------------|-------------------|--------|
| 1 | No statistical significance tests | R1 | Major | Results | Added Wilcoxon (Exp 2), one-sample t-tests (Exp 4), paired t-tests (Exp 5) | Exp 2, 4, 5 results sections | RESOLVED |
| 2 | LoRA conclusion overstated | R1 | Major | Results/Discussion | Softened language to "under current configuration" with caveats about training data/epochs | Exp 5, Key Findings, Conclusions | RESOLVED |
| 3 | Table 6 (system comparison) unsourced | R1 | Major | Discussion | Renamed to "Commercial LLMs", added ref5/ref29 citations | Table 6 caption and body | RESOLVED |
| 4 | Discussion too shallow | R1 | Minor | Discussion | Added per-topic score table (Table 7), per-difficulty analysis, expanded error analysis | Error Analysis subsection | RESOLVED |
| 5 | No human evaluation | R1 | Minor | Limitations | Acknowledged in Limitations, cited Zheng et al. (2024) for LLM-as-Judge validity | Limitations subsection | RESOLVED |

---

## Revision Tracking Table — Round 2 Issues (All Resolved)

| # | Issue Description | Reviewer | Type | Section | Resolution Summary | Location of Change | Status |
|---|-------------------|----------|------|---------|-------------------|-------------------|--------|
| 6 | Exp 2 sample size says n=50 but actual is n=5 | R2 | Major | Results/Exp 2 | Caption corrected to n=5 per strategy; added domain coverage explanation | Table caption + text | RESOLVED |
| 7 | BLEU/ROUGE as primary metric | R2 | Major | Results/Exp 1 | LLM-as-Judge promoted to Exp 1 (primary); BLEU/ROUGE demoted to Exp 4 (supplementary); abstract + setup reordered | Abstract, Exp Setup, Results sections | RESOLVED |
| 8 | "Bayesian-inspired" misleading | R2 | Minor | Methods | Renamed to "simplified probabilistic approach inspired by Bayesian Knowledge Tracing"; comparison table updated | Knowledge Tracking + Table 6 | RESOLVED |
| 9 | Insufficient latency discussion | R2 | Minor | Discussion | Added dedicated "Response Latency Analysis" section with 4 mitigation strategies (quantization, caching, speculative decoding, smaller models) | New subsection in Discussion | RESOLVED |
| 10 | Thin Related Work | R2 | Minor | Related Work | Added GitHub Copilot (ref31), CodeWhisperer (ref32), Codex tutoring (ref33), QLoRA (ref34), Wang et al. (ref30) | LLMs in Education + Open-Source subsections | RESOLVED |

---

## Revision Tracking Table — Remaining Minor Issues (Pre-Submission)

| # | Issue Description | Reviewer | Type | Section | Resolution Summary | Location of Change | Status |
|---|-------------------|----------|------|---------|-------------------|-------------------|--------|
| A | Contribution list uses old experiment order | R2 | Editorial | Introduction | Updated to match new Exp 1-5 order | Lines 52-57 | RESOLVED |
| B | Cross-family n=42 vs n=50 unexplained | R2 | Minor | Results/Exp 1 | Added sentence explaining 8 parse failures | Cross-family table text | RESOLVED |
| C | Success criteria not operationalized | R2 | Minor | Results/Exp 3 | Added operationalized criteria (100 char min, repetition check, topic relevance) | Ablation section | RESOLVED |
| D | ref33 (AutoHint) doesn't match Codex tutoring claim | R2 | Minor | Related Work | Reframed sentence to match AutoHint's actual content (prompt optimization) | Related Work | RESOLVED |
| E | Conclusions >80% overlap with Abstract | R2 | Editorial | Conclusions | Expanded with broader implications paragraph (3 key findings + forward look) | Conclusions section | RESOLVED |

---

## Round 5 Improvements (Exp 2 Expansion)

| # | Improvement | Impact | Section |
|---|-------------|--------|---------|
| 1 | Expanded Exp 2 sample from n=5 to n=15 per strategy | Statistical power | Results/Exp 2 |
| 2 | Added 10 new programming questions across 6 topics | Domain coverage | Exp 2 data |
| 3 | CoT vs zero-shot now significant (p=0.044) | Stronger claims | Results/Exp 2 |
| 4 | CoT vs few-shot now significant (p=0.012) | Stronger claims | Results/Exp 2 |
| 5 | Updated all references from 0.80 to 0.83 | Consistency | Abstract, Discussion, Conclusions |
| 6 | Updated Limitations to reflect n=15 | Accuracy | Limitations |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Round 1 items | 5 (all RESOLVED) |
| Round 2 items | 5 (all RESOLVED) |
| Round 4 items | 4 enhancements (all DONE) |
| Round 5 items | 6 improvements (Exp 2 expansion) |
| New references added | 9 (ref30-ref39) |
| Sections reordered | Results (Exp 1-5 now sequential) |
| New subsections added | Response Latency Analysis, Pedagogical Design Principles, Practical Deployment |
| Score improvement | 6.25 → 8.5 (+2.25) |

---

## Completeness Checklist

- [x] Every Round 1 reviewer comment has been addressed
- [x] Every Round 2 reviewer comment has been addressed
- [x] Statistical tests reported with test statistics and p-values
- [x] Cross-family validation included
- [x] Limitations section acknowledges all known constraints
- [x] All new references added to bibliography
- [x] Figures and tables correctly labeled and cross-referenced
- [x] Abstract matches Results section ordering
- [x] AI disclosure statement present
- [x] Author contributions statement present
- [x] All 5 remaining minor issues (Issues A-E) resolved
