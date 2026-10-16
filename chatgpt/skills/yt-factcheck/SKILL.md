---
name: yt-factcheck
description: >-
  Extract and rigorously verify factual claims in YouTube scripts, classifying evidence,
  eliminating fabricated studies or citations, and protecting creators from misinformation liabilities.
---

# yt-factcheck — Script Claim Verification & Evidence Audit

Factual inaccuracies, unverified health claims, and fabricated statistics destroy creator credibility and risk YouTube community guideline strikes or algorithmic demotions. This workflow audits every factual assertion before recording.

## Absolute Verification Standards
> **CRITICAL FACT-CHECKING INTEGRITY RULES**:
> 1. **Zero Hallucination Tolerance**: NEVER invent study titles, author names, journal publications, university institutions, or clinical trial outcomes.
> 2. **Religious Text Integrity**: For Islamic citations (Quran verses or Hadith), NEVER fabricate surah/ayah references or invent Hadith authenticity grades (Sahih/Hasan/Da'if). If an exact source cannot be verified word-for-word, flag for creator verification with certified scholars.
> 3. **Medical & Psychological Scrutiny**: Distinguish between peer-reviewed scientific consensus, preliminary animal studies, clinical hypotheses, and creator opinions. Always insist on professional medical disclaimers.
> 4. **Acknowledge Uncertainty**: If a historical or scientific question is actively debated among experts, present both sides rather than asserting a disputed theory as settled fact.

## Claim Classification System
Every extracted claim is tagged with one of four statuses:
- **[VERIFIED]**: Backed by established consensus, primary documentation, reputable peer-reviewed journals, or official government databases.
- **[DISPUTED]**: Significant conflicting evidence exists among recognized domain experts or institutions.
- **[UNSUPPORTED]**: No credible evidence found; likely an urban legend, viral rumor, or marketing myth.
- **[REQUIRES CITATION]**: Plausible assertion, but lacks a specific primary source, date, or author attribution.

## High-Risk Scrutiny Domains
- **Mental Health & Psychological Awareness**: Diagnostic criteria (DSM-5/ICD-11), trauma claims, therapeutic techniques, clinical labels (narcissism, gaslighting, PTSD).
- **Physical Health & Nutrition**: Diets, supplements, biochemical mechanisms, disease prevention.
- **Financial & Crypto Advice**: Yield promises, historical ROI claims, tax regulations.
- **Science & Technology**: Benchmarks, algorithmic behavior, engineering constraints.
- **Current Events & History**: Timelines, casualty numbers, direct quotes.

## Fact-Check Report Architecture
For each audited assertion:
1. **Extracted Script Line**: The exact words written in the draft.
2. **The Factual Claim**: The underlying factual proposition being asserted.
3. **Classification**: `[VERIFIED]`, `[DISPUTED]`, `[UNSUPPORTED]`, or `[REQUIRES CITATION]`.
4. **Primary Evidence / Sources**: Credible references, publisher, year, or URL.
5. **Recommended Script Revision**: A corrected, responsible phrasing that preserves entertainment value while protecting accuracy.

## Sample Fact-Check Audit Card
```markdown
### Claim 01 | The Sleep Statistic
- **Script Excerpt**: "Stanford neuroscientists proved that looking at blue light after 10 PM destroys 80% of your deep sleep permanently."
- **Status**: [UNSUPPORTED / EXAGGERATED]
- **Evidence Review**: Blue light disrupts melatonin onset and sleep latency (e.g., Chang et al., PNAS 2015), but peer-reviewed literature does NOT support an "80% permanent destruction of deep sleep."
- **Liability**: Exaggerated medical claim; triggers skepticism and medical community pushback.
- **Corrected Script Phrasing**:
  "Clinical sleep studies show that bright screen light before bed suppresses melatonin and significantly delays deep REM sleep cycles. Here is what happens inside your brain..."
```

## What to Hand Back
1. Complete Claim Audit Log with status badges.
2. Critical Flagged Assertions requiring immediate creator attention.
3. **Corrected Script Draft**: Clean revised script with substantiated phrasing.
4. Next step: **Accept script corrections or provide creator citations?**
