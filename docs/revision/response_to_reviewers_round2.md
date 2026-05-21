# Response to Reviewers — Round 2 (Internal Review)

**Paper**: Design and Evaluation of an Open-Source LLM-Based Intelligent Tutoring System for Programming Education
**Journal**: Applied Sciences (MDPI)

---

## Reviewer Comments and Responses

### Comment C1: Data Inconsistency in Prompt Comparison (Table 2 vs Text)
**Issue**: Text states "0.72 vs. 0.32 and 0.24" but Table 2 shows CoT=0.80, Zero-shot=0.44, Few-shot=0.36.

**Response**: Thank you for catching this error. The text contained numbers from an earlier draft. We have corrected the text to match the table data: "0.80 vs. 0.44 and 0.36".

**Action**: Corrected text in Section 4.2.

---

### Comment C2: Sample Size Inconsistency (Table 2 Caption vs Text)
**Issue**: Text says "5 programming questions" but Table 2 caption says "n = 50 per strategy".

**Response**: The experiment was run on 50 questions (same as Experiment 1). The text incorrectly stated "5 questions" from an earlier version. We have corrected the text to "50 programming questions".

**Action**: Corrected text in Section 4.2.

---

### Comment C3: Code Block / Example Rate Inconsistency
**Issue**: Text states "74%" but Table 1 shows 76% and 78%.

**Response**: The text contained outdated percentages. We have corrected to "76% code block inclusion rate and 78% example inclusion rate" to match Table 1.

**Action**: Corrected text in Section 4.1.

---

### Comment C4: Success Metric Not Defined
**Issue**: "Success Rate" in Table 3 is not defined anywhere.

**Response**: We have added a definition in Section 3.7: success is defined as the system producing a complete, coherent response that addresses the student's question without generation errors (e.g., truncation, repetition, or empty output). We have also added this definition to the Table 3 caption.

**Action**: Added definition in Section 3.7 and Table 3 caption.

---

### Comment M1: Response Time Not Discussed as Limitation
**Issue**: Average response times (27.8-66.9s) are not discussed as a limitation.

**Response**: We agree that response time is an important usability concern. We have added a paragraph to Section 5.5 discussing this limitation: the current response times may impact real-time tutoring usability, and we discuss potential optimizations including model quantization (GGUF/GPTQ), response caching for common questions, and exploring smaller models (3B parameters) for faster inference.

**Action**: Added response time limitation paragraph to Section 5.5.

---

### Comment M2: LLM-as-Judge Limitations Underexplored
**Issue**: Using Qwen2.5-72B to judge Qwen2.5-7B outputs may introduce same-family bias.

**Response**: We acknowledge this limitation. We have added a paragraph discussing that using a model from the same family as judge may introduce systematic bias (e.g., similar tokenization patterns, similar training data preferences). We note that recent work on LLM-as-Judge evaluation suggests cross-family evaluation is preferable, and we cite Zheng et al. (2024) on this issue. We have also added this to the Limitations section.

**Action**: Added LLM-as-Judge bias discussion to Section 4.4 and Section 5.5.

---

### Comment M3: Comparison Table Lacks Citations
**Issue**: Table 5 claims about GPT-4 Tutor, ChatGPT Edu, and Ask-Elle lack citations.

**Response**: We have added citations for the compared systems' capabilities. Ask-Elle's features are cited from Gerdes et al. (2012). For GPT-4 Tutor and ChatGPT Edu, we have added a note that the comparison is based on publicly available documentation as of 2025, with references to the respective product documentation.

**Action**: Added citations and disclaimer to Table 5.

---

### Comment M4: Formula Variable Naming Convention
**Issue**: Underscored variable names are unconventional in academic notation.

**Response**: We have rewritten the formula using standard mathematical notation with subscript variables: $m = \frac{c + p}{t + w}$ where $c$ = correct attempts, $p$ = prior correct, $t$ = total attempts, $w$ = prior weight.

**Action**: Rewrote Equation (1) with standard notation.

---

### Comment m1: Author Information
**Issue**: Placeholder names and emails.

**Response**: This will be filled in before final submission.

**Action**: Deferred to final submission.

---

### Comment m2: Abstract Word Count
**Issue**: Abstract is ~250 words (MDPI limit is 150-250).

**Response**: The abstract is currently at the upper limit. We have trimmed it slightly to 245 words while preserving all key information.

**Action**: Trimmed abstract.

---

### Comment m3: Missing Recent References
**Issue**: Need more 2024-2025 references.

**Response**: We have added 2 recent references: one on LLM-as-Judge methodology (2024) and one on open-source LLMs in education (2024).

**Action**: Added 2 new references.

---

### Comment m4: Figure Caption Formatting
**Issue**: Parenthetical sub-figure labels may not render correctly.

**Response**: We have changed to (a), (b), (c), (d) sub-figure labeling convention.

**Action**: Updated figure captions.

---

### Comment m5: Abbreviation Consistency
**Issue**: "CoT" in abbreviation list but "chain-of-thought" spelled out in text.

**Response**: We have removed "CoT" from the abbreviation list since it is spelled out in the text for readability.

**Action**: Removed CoT from abbreviation list.

---

## Summary of Changes

| Change | Status |
|--------|--------|
| C1: Text data inconsistency (0.72→0.80, etc.) | Corrected |
| C2: Sample size text (5→50) | Corrected |
| C3: Code block rate text (74%→76%/78%) | Corrected |
| C4: Success metric definition | Added |
| M1: Response time limitation | Added |
| M2: LLM-as-Judge bias discussion | Added |
| M3: Comparison table citations | Added |
| M4: Formula notation | Rewritten |
| m1: Author information | Deferred |
| m2: Abstract trimmed | Trimmed to 245 words |
| m3: Recent references | Added 2 |
| m4: Figure caption format | Updated |
| m5: Abbreviation consistency | Fixed |
