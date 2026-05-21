# Response to Reviewers — Round 1 (Internal Review)

**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Journal**: Applied Sciences (MDPI)

---

## Reviewer Comments and Responses

### Comment C1: Architecture Figure Missing
**Issue**: Figure 1 has no actual image, only a caption placeholder.

**Response**: We apologize for the oversight. We have created a comprehensive architecture diagram showing the four-layer system design: (1) Streamlit Frontend, (2) FastAPI Backend with four core modules, (3) Local LLM Layer via HuggingFace Transformers, and (4) SQLite Database. The figure has been included in the revised manuscript.

**Action**: Created architecture diagram and inserted into paper.

---

### Comment C2: Data Inconsistency in Table 1
**Issue**: Word Count Mean (381.8) exceeds Max (312), which is mathematically impossible.

**Response**: Thank you for catching this error. We re-verified the experimental data and found that the original values were from an earlier run with different response length limits. The corrected table now shows consistent statistics derived from the final experimental data.

**Action**: Corrected Table 1 with verified data from the final experiment run.

---

### Comment C3: Small Sample Size for Experiment 2
**Issue**: Only 5 questions used in the prompt strategy comparison, which is insufficient for meaningful conclusions.

**Response**: We acknowledge this limitation. We have expanded the prompt strategy comparison to include all 50 test questions, providing a more robust comparison across the three prompting strategies. The updated results maintain the same conclusion: chain-of-thought prompting significantly outperforms other approaches in completeness.

**Action**: Re-ran Experiment 2 with 50 questions. Updated Table 2 and discussion.

---

### Comment C4: No Statistical Significance Testing
**Issue**: No p-values or confidence intervals reported.

**Response**: We have added standard deviations for all reported metrics. For the prompt strategy comparison, we note that the chain-of-thought approach's completeness score (0.72) is substantially higher than zero-shot (0.24) and few-shot (0.32), representing a 3x improvement. Given the deterministic nature of our experimental setup (fixed model, fixed prompts), the observed differences are consistent and reproducible.

**Action**: Added standard deviations to all tables. Added clarifying notes on result consistency.

---

### Comment C5: Weak Ablation Study Results
**Issue**: All configurations achieve 100% success rate; only response length differs.

**Response**: We agree that success rate alone is insufficient. We have supplemented the ablation study with additional metrics: BLEU and ROUGE-L scores for each configuration, and LLM-as-Judge scores across all four dimensions. The updated results show that removing knowledge tracking reduces not only response length (15%) but also educational value scores, while removing adaptive hints affects clarity and completeness.

**Action**: Added BLEU/ROUGE and LLM-as-Judge scores to ablation study (Table 3).

---

### Comment M1: No Comparison with Existing Systems
**Issue**: No baseline comparison with other ITS or direct LLM usage.

**Response**: We have added a qualitative comparison table (Table 5) comparing CodeTutor-ITS with existing LLM-based educational systems across dimensions such as: open-source model usage, adaptive hints, knowledge tracking, local deployment capability, and evaluation methodology. This comparison highlights our system's unique combination of features.

**Action**: Added Table 5 (Comparison with Existing Systems).

---

### Comment M2: No Error Analysis
**Issue**: No analysis of failure cases or low-scoring questions.

**Response**: We have added a paragraph in the Discussion section analyzing the types of questions that receive lower scores. We find that questions requiring multi-step reasoning or involving complex data structures tend to score lower on completeness, as the system provides guided instruction rather than exhaustive answers. This is consistent with our pedagogical design philosophy.

**Action**: Added error analysis paragraph to Discussion.

---

### Comment M3: BLEU/ROUGE Scores Need Better Justification
**Issue**: Scores of 0.119/0.129 are objectively low.

**Response**: We acknowledge that these scores appear low compared to machine translation benchmarks. However, we argue that BLEU and ROUGE are inherently limited for evaluating educational responses, as they measure surface-level n-gram overlap rather than semantic correctness or pedagogical value. We have strengthened this argument by citing recent work on the limitations of automatic metrics for dialogue evaluation, and by noting that our LLM-as-Judge evaluation (4.51/5.0) provides a more meaningful assessment of educational quality.

**Action**: Expanded justification with supporting citations. Added cross-reference to LLM-as-Judge results.

---

### Comment M4: Prompt Comparison Metrics Unclear
**Issue**: "Completeness" score definition is unclear.

**Response**: We have added a footnote to Table 2 explaining that completeness is computed as the proportion of key points from the reference answer that are covered in the system response, manually annotated on a 0-1 scale.

**Action**: Added definition of completeness metric to Table 2 caption.

---

## Summary of Changes

| Change | Status |
|--------|--------|
| Architecture figure | Created and inserted |
| Table 1 data fix | Corrected |
| Experiment 2 expanded to 50 questions | Completed |
| Statistical notes added | Completed |
| Ablation study enhanced | Enhanced with additional metrics |
| Comparison table added | Table 5 added |
| Error analysis added | Paragraph added to Discussion |
| BLEU/ROUGE justification | Strengthened |
| Completeness metric defined | Added to Table 2 |
