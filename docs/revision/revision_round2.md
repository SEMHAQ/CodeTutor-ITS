# Revision Round 2: Paper Review Report

**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target**: Applied Sciences (MDPI, SCI Q2/Q3)
**Date**: 2026-05-21
**Previous Round**: Major Revision (Round 1)

---

## Five-Dimension Scoring

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Originality | 20% | 6/10 | Incremental; combination of existing techniques |
| Methodological Rigor | 25% | 5/10 | Automated metrics only, no human evaluation |
| Evidence Sufficiency | 25% | 6/10 | Four experiments, but data inconsistencies remain |
| Argument Coherence | 15% | 7/10 | Logical flow, clear structure |
| Writing Quality | 15% | 7/10 | Generally well-written, minor issues |

**Overall**: 6.05/10 → **Major Revision**

---

## Critical Issues (Must Fix)

### C1. Data Inconsistency in Prompt Comparison (Table 2 vs Text)
- **Location**: Section 4.2, line 191, Table 2
- **Problem**: The text states "chain-of-thought strategy significantly outperforms other approaches in completeness score (0.72 vs. 0.32 and 0.24)" but Table 2 shows CoT=0.80, Zero-shot=0.44, Few-shot=0.36. The numbers 0.72, 0.32, 0.24 do not appear in the table.
- **Action**: Correct the text to match the table data: "0.80 vs. 0.44 and 0.36".

### C2. Sample Size Inconsistency (Table 2 Caption vs Text)
- **Location**: Section 4.2, line 176 vs Table 2 caption
- **Problem**: The text says "We compared three prompting strategies using 5 programming questions" but Table 2 caption says "n = 50 per strategy". Either the text is wrong (should say 50) or the caption is wrong.
- **Action**: Verify the actual sample size and make text and caption consistent.

### C3. Code Block / Example Rate Inconsistency
- **Location**: Section 4.1, line 172 vs Table 1
- **Problem**: The text states "74% code block inclusion rate and 74% example inclusion rate" but Table 1 shows Has Code Block = 76.0% and Has Example = 78.0%.
- **Action**: Correct the text to match Table 1: "76% code block inclusion rate and 78% example inclusion rate".

### C4. Success Metric Not Defined
- **Location**: Table 3 (Ablation Study)
- **Problem**: The "Success Rate" column is not defined anywhere. What constitutes a "successful" response? Is it passing test cases? Correct code generation? Response quality above a threshold?
- **Action**: Add a clear definition of the success metric in Section 3.7 (Experimental Setup) or in the Table 3 caption.

---

## Major Issues (Should Fix)

### M1. Response Time Not Discussed as Limitation
- **Location**: Section 5.5 (Limitations)
- **Problem**: Average response times range from 27.8s to 66.9s. For an interactive tutoring system, this is a significant usability concern that is not mentioned in the Limitations section.
- **Action**: Add response time as a limitation and discuss potential optimization strategies (model quantization, caching, smaller models).

### M2. LLM-as-Judge Limitations Underexplored
- **Location**: Section 4.4, Section 5.5
- **Problem**: The paper uses Qwen2.5-72B as judge to evaluate Qwen2.5-7B outputs. This is a same-family model evaluation, which may introduce bias (models from the same family may have similar preferences). This limitation is not discussed.
- **Action**: Add a paragraph discussing the potential bias of using a same-family model as judge, and cite recent work on LLM-as-Judge limitations.

### M3. Comparison Table (Table 5) Lacks Citations
- **Location**: Section 5.1, Table 5
- **Problem**: The comparison with GPT-4 Tutor, ChatGPT Edu, and Ask-Elle provides no citations for the claims about these systems' capabilities. Readers cannot verify whether GPT-4 Tutor really lacks adaptive hints, etc.
- **Action**: Add citations for each compared system's capabilities, or add a disclaimer that the comparison is based on publicly available documentation.

### M4. Formula Variable Naming Convention
- **Location**: Equation (1)
- **Problem**: The formula uses underscored variable names (`correct_attempts`, `prior_correct`, `total_attempts`, `prior_weight`) which is unconventional in academic mathematical notation. Standard practice uses subscripts or different symbols.
- **Action**: Rewrite using standard mathematical notation, e.g., $mastery = \frac{c + p_c}{t + p_w}$ with proper variable definitions.

---

## Minor Issues (Nice to Fix)

### m1. Author Information
- **Problem**: Still has placeholder names (Firstname Lastname) and emails.
- **Action**: Fill in actual author details before submission.

### m2. Abstract Word Count
- **Problem**: Abstract is approximately 250 words. MDPI recommends 150-250 words.
- **Action**: Trim slightly if possible; currently at the upper limit.

### m3. Missing Recent References
- **Problem**: Most references are from 2020-2023. Need more 2024-2025 references on LLM-based education.
- **Action**: Add 2-3 more recent references, especially on LLM-as-Judge methodology and open-source LLMs in education.

### m4. Figure Caption Formatting
- **Problem**: Figure captions use parenthetical sub-figure labels (e.g., "(Top)", "(Bottom left)") which may not render correctly in all MDPI formats.
- **Action**: Consider using (a), (b), (c), (d) sub-figure labeling convention.

### m5. Abbreviation Consistency
- **Problem**: The paper uses "ITS" in the title and body but the abbreviation list defines it. However, "CoT" is used in the abbreviation list but "chain-of-thought" is spelled out in the text. Choose one consistent approach.
- **Action**: Either use "CoT" consistently in the text or remove it from the abbreviation list.

---

## Priority Order

1. **C1** (data inconsistency) — Quick fix, prevents credibility issues
2. **C2** (sample size) — Quick fix, consistency
3. **C3** (code block rate) — Quick fix, consistency
4. **C4** (success metric) — Add definition
5. **M1** (response time limitation) — Add paragraph
6. **M2** (LLM-as-Judge bias) — Add paragraph
7. **M3** (comparison citations) — Add citations or disclaimer
8. **M4** (formula notation) — Rewrite equation
9. **m1-m5** — Final polish

---

## Summary

The paper has improved significantly since Round 1. The architecture figure is now present, the ablation study has been enhanced, and the comparison table has been added. However, several data inconsistencies remain between the text and tables (C1-C3), which undermine credibility. The success metric definition (C4) and response time discussion (M1) are important additions. With these fixes, the paper would be suitable for publication in Applied Sciences.
