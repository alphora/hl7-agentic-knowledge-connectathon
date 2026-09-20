# TNBC, exactly 10 mm, clinical T1b N0 M0

Synthetic FHIR R4 educational test case; no real patient information.

Exactly 10 mm remains T1b in this supplied clinical assessment. Neither the tumor nor node criterion is met; this is not a statement that no treatment is indicated.

- Active, confirmed invasive breast cancer Condition: present.
- Clinical assessment: cT1b, cN0, cM0.
- Longest tumor dimension: 10 mm.
- ER: negative; PR: negative; HER2: negative.
- Evaluation: 2026-06-15T12:00:00Z; observations effective June 1 and issued June 2.

| Expression | Expected |
| --- | --- |
| `Has Active Confirmed Invasive Breast Cancer` | true |
| `Has Nonmetastatic Disease` | true |
| `In Neoadjuvant Review Population` | true |
| `Is Triple Negative` | true |
| `Has Clinically Positive Nodes` | false |
| `Has Clinical T1c Or Higher` | false |
| `Meets Tumor Or Node Criterion` | false |
| `Neoadjuvant TNBC Guidance Applicable` | false |

`true` applicability means the source-linked neoadjuvant guidance should be surfaced for oncology review. It does not authorize or create a medication order. `false` describes only this track criterion.

Source locators: `asco-neoadjuvant-2021`, recommendation 3.1; `nci-breast-tnm`, T-category boundary context. Clinical node positivity follows the ASCO criterion; the NCI page's pathological N definitions are not used here. The population gate and missing-data contract are track-authored operational choices.
