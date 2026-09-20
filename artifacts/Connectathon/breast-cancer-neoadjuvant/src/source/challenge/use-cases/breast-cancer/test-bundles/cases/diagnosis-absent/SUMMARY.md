# Receptor and staging results without cancer diagnosis

Synthetic FHIR R4 educational test case; no real patient information.

No Condition establishes active confirmed invasive breast cancer. Test results cannot manufacture that diagnosis. Without an indexed Condition, unanchored tumor-specific data is unusable and those subexpressions remain unknown. Unlinked Observations are retained only as a deliberate negative control.

- Active, confirmed invasive breast cancer Condition: absent.
- Clinical assessment: cT1c, cN0, cM0.
- Longest tumor dimension: 15 mm.
- ER: negative; PR: negative; HER2: negative.
- Evaluation: 2026-06-15T12:00:00Z; observations effective June 1 and issued June 2.

| Expression | Expected |
| --- | --- |
| `Has Active Confirmed Invasive Breast Cancer` | false |
| `Has Nonmetastatic Disease` | unknown (null) |
| `In Neoadjuvant Review Population` | false |
| `Is Triple Negative` | unknown (null) |
| `Has Clinically Positive Nodes` | unknown (null) |
| `Has Clinical T1c Or Higher` | unknown (null) |
| `Meets Tumor Or Node Criterion` | unknown (null) |
| `Neoadjuvant TNBC Guidance Applicable` | false |

`true` applicability means the source-linked neoadjuvant guidance should be surfaced for oncology review. It does not authorize or create a medication order. `false` describes only this track criterion.

Source locators: `asco-neoadjuvant-2021`, recommendation 3.1; `nci-breast-tnm`, T-category boundary context. Clinical node positivity follows the ASCO criterion; the NCI page's pathological N definitions are not used here. The population gate and missing-data contract are track-authored operational choices.
