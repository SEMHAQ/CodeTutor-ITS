# Revision Round 1: Paper Review Report

**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Target**: Applied Sciences (MDPI, SCI Q2/Q3)
**Date**: 2026-05-21

---

## Critical Issues (Must Fix)

### C1. Architecture Figure Missing
- **Location**: Section 3.1, Figure 1
- **Problem**: `\includegraphics` is commented out. The figure has no actual image.
- **Action**: Create an architecture diagram using draw.io or similar tool.

### C2. Data Inconsistency in Table 1
- **Location**: Table 1 (Tutoring Quality Assessment)
- **Problem**: Word Count Mean = 381.8 but Max = 312. This is mathematically impossible.
- **Action**: Re-verify the data from `tutoring_quality_results.csv` and correct the table.

### C3. Small Sample Size for Experiment 2
- **Location**: Section 4.2 (Prompt Strategy Comparison)
- **Problem**: Only 5 questions used. Too small for any meaningful conclusion.
- **Action**: Re-run with 50 questions (same as Experiment 1), or justify why 5 is sufficient.

### C4. No Statistical Significance Testing
- **Location**: All experiments
- **Problem**: No p-values, confidence intervals, or statistical tests reported.
- **Action**: Add at minimum: standard deviations (already have some), and a note about significance where applicable.

### C5. Weak Ablation Study Results
- **Location**: Table 3 (Ablation Study)
- **Problem**: All configurations achieve 100% success rate. Only response length differs. This doesn't strongly demonstrate module contributions.
- **Action**: Add more meaningful metrics: BLEU/ROUGE scores per configuration, LLM-as-Judge scores per configuration.

---

## Major Issues (Should Fix)

### M1. No Comparison with Existing Systems
- **Problem**: No baseline comparison with other ITS or direct LLM usage.
- **Action**: Add a brief comparison table with existing systems (qualitative is fine if quantitative data unavailable).

### M2. No Error Analysis
- **Problem**: No analysis of failure cases or low-scoring questions.
- **Action**: Add a paragraph discussing which types of questions score lower and why.

### M3. BLEU/ROUGE Scores Need Better Justification
- **Problem**: Scores of 0.119/0.129 are objectively low. The current explanation is weak.
- **Action**: Strengthen the argument that these metrics are inappropriate for evaluating educational responses, cite supporting literature.

### M4. Prompt Comparison Metrics Unclear
- **Location**: Table 2
- **Problem**: "Completeness" score is defined but not clearly explained how it's computed.
- **Action**: Add a sentence explaining how completeness is measured.

---

## Minor Issues (Nice to Fix)

### m1. Author Information
- **Problem**: Placeholder names and emails.
- **Action**: Fill in actual author details before submission.

### m2. Recent References
- **Problem**: Most references are from 2020-2023. Need more 2024-2025 references.
- **Action**: Add 3-5 more recent references on LLM-based education.

### m3. Discussion Depth
- **Problem**: Discussion section is relatively brief.
- **Action**: Expand the educational implications subsection with more specific recommendations.

### m4. Abstract Length
- **Problem**: Abstract is ~250 words. MDPI recommends 150-250 words.
- **Action**: Trim slightly if possible, currently at the upper limit.

---

## Priority Order

1. **C2** (data fix) - Quick fix, prevents credibility issues
2. **C3** (sample size) - Re-run experiment if needed
3. **C1** (architecture figure) - Create diagram
4. **C5** (ablation metrics) - Add more evaluation metrics
5. **M1** (comparison table) - Add qualitative comparison
6. **M3** (BLEU justification) - Strengthen argument
7. **C4** (statistics) - Add where applicable
8. **M2** (error analysis) - Add paragraph
9. **m1-m4** - Final polish
