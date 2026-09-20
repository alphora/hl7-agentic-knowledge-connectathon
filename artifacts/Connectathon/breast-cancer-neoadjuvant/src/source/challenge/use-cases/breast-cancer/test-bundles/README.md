# Synthetic breast-cancer patient test bundles

These 13 FHIR R4 4.0.1 cases define an implementation-neutral input and expected-result contract for source-linked neoadjuvant TNBC guidance. They follow the STEADI `bundle.json`, `assertions.json`, `SUMMARY.md`, and manifest pattern. The inputs are already diagnostic Observations, so there is no Questionnaire or SDC extraction step.

Every patient is synthetic. Every resource has the `HTEST` security label. No fixture contains a prescription, administration plan, dose, or medication order. A true applicability result means to surface guidance for oncology review; a false result concerns only this narrow review criterion and does not mean that treatment is unnecessary.

## Source and population contract

The clinical criterion follows `asco-neoadjuvant-2021`, recommendation 3.1: TNBC with clinically positive nodes and/or at least T1c disease. The source is linked in the [source manifest](../sources/manifest.yaml). The [use-case overview](../README.md) explains the later ASCO immunotherapy update and current-guidance context. These fixtures do not test pembrolizumab eligibility or complete regimen selection.

The track operationalizes this criterion for an **active, confirmed invasive primary breast cancer with explicit clinical M0 assessment**. Requiring an explicit M0 record and preserving unknown values are track-authored operational choices, not verbatim ASCO rules. Clinical T/N/M assessments are supplied inputs; participants must not infer staging solely from a tumor-size measurement. The NCI staging reference supplies T-category boundary context, including the T1b/T1c boundary at 10 mm. Its N-category section is pathological and is not used to define the clinical N assertions here; those assertions preserve the clinically node-positive versus node-negative distinction in the ASCO recommendation.

A `Condition` coded `invasive-breast-carcinoma` in the [local CodeSystem](code-system.json), with clinical status `active` and verification status `confirmed`, establishes the indexed cancer. The local CodeSystem defines synthetic fixture assertions and clinical stage categories; it is not a mapping to SNOMED CT, AJCC proprietary terminology, or an mCODE profile. There is no claim of mCODE conformance.

## Observation selection

- Evaluation time: `2026-06-15T12:00:00Z`.
- Observations are final, effective `2026-06-01T09:00:00Z`, and issued `2026-06-02T10:00:00Z`, before evaluation.
- For cases with an indexed cancer, every Observation has the same Patient subject and an explicit `focus` reference to that cancer Condition.
- Select usable Observations for that indexed cancer only. Unlinked observations, another tumor's observations, and future or nonfinal results must not supply these inputs.
- When no indexed cancer Condition exists, all tumor-specific input expressions are unknown. The diagnosis and population/applicability gates are false. The `diagnosis-absent` case intentionally includes unanchored results to detect an implementation that assembles a diagnosis from laboratory data alone.
- Each supplied case has at most one Observation per input code, one indexed Condition, and no conflicting stage or receptor assessments. Multiple cancers, conflicting or superseded results, treatment response, pathological staging, recurrent disease, and post-neoadjuvant reassessment need additional contracts beyond this fixture set.

The supplied clinical stage codes are `cT1mi`, `cT1a`, `cT1b`, `cT1c`, `cT2`, `cT3`, `cT4`; `cN0`–`cN3`; and `cM0`/`cM1`. The current cases exercise T1b, T1c, T2, N0, N1, M0, M1, and missing N/M. Other declared categories make the comparison contract explicit but are not covered by individual cases here.

## Terminology and units

Observation codes are pinned to LOINC 2.81. The five codes and exact displays were verified as active through ReasonHub on 2026-09-19; see [lookup evidence](../validation/terminology-lookups.json).

| Input | LOINC 2.81 | Value |
| --- | --- | --- |
| Estrogen receptor | `85337-4` | Qualitative result |
| Progesterone receptor | `85339-0` | Qualitative result |
| HER2 interpretation | `48676-1` | Qualitative result |
| Tumor size | `21889-1` | Component containing longest dimension |
| Maximum tumor dimension component | `33728-7` | UCUM `mm` or `cm` quantity |

Negative and positive receptor answers use LOINC answer codes `LA6577-6` and `LA6576-8`. These answer codes were checked against the [LOINC preferred answer list](https://loinc.org/85339-0/), separately from the ReasonHub concept lookups; the ReasonHub answer-code endpoint did not resolve them. The equivocal fixture uses the defined local code `equivocal`. It does not relabel an indeterminate answer code or presume a final negative HER2 interpretation.

Clinical staging and the invasive-diagnosis assertion use the local CodeSystem. There is no automatic conversion from these local codes to standard clinical terminology. A participant may map the input contract to its chosen terminology, but must document exact mappings and versions while preserving the supplied clinical meanings and unknown values.

The 15 mm and 1.5 cm cases have identical stage and applicability expectations. Size is a consistency check and data-portability exercise, not the source of the T-category expression. The exactly-10-mm case explicitly supplies cT1b.

## Required expressions

| Expression | Contract |
| --- | --- |
| `Has Active Confirmed Invasive Breast Cancer` | True when the indexed Condition exists with the required code and statuses; false if it does not. |
| `Has Nonmetastatic Disease` | cM0 → true; cM1 → false; no usable indexed clinical M assessment → unknown. |
| `In Neoadjuvant Review Population` | Diagnosis expression AND nonmetastatic expression. |
| `Is Triple Negative` | ER-negative AND PR-negative AND HER2-negative. Positive → false for that receptor; absent or unresolved → unknown. |
| `Has Clinically Positive Nodes` | cN1/cN2/cN3 → true; cN0 → false; no usable indexed N assessment → unknown. |
| `Has Clinical T1c Or Higher` | cT1c/cT2/cT3/cT4 → true; cT1mi/cT1a/cT1b → false; no usable indexed T assessment → unknown. |
| `Meets Tumor Or Node Criterion` | Clinical T expression OR clinically positive nodes expression. |
| `Neoadjuvant TNBC Guidance Applicable` | Review population AND triple-negative status AND tumor-or-node criterion. |

Use CQL three-valued Boolean semantics. `false AND null` is false; `true AND null` is null; `true OR null` is true; `false OR null` is null. Missing values must not be converted to false. Missing or unresolved HER2 does not establish TNBC.

Every assertion has an expression name and typed expected Boolean value. Unknown is JSON `null` plus `"semantics": "unknown"`. Execution errors and absent result fields are not equivalent to null. A harness should save actual engine output separately and leave the shared assertions unchanged.

## Cases

| Case | Distinguishing input | Applicability |
| --- | --- | --- |
| [tnbc-t1c-n0](cases/tnbc-t1c-n0/SUMMARY.md) | TNBC, cT1c cN0 cM0, 15 mm | true |
| [tnbc-t1b-n0-10mm](cases/tnbc-t1b-n0-10mm/SUMMARY.md) | TNBC, cT1b cN0 cM0, exactly 10 mm | false |
| [tnbc-t1b-n1](cases/tnbc-t1b-n1/SUMMARY.md) | TNBC, cT1b cN1 cM0, 8 mm | true |
| [her2-positive](cases/her2-positive/SUMMARY.md) | HER2 positive | false |
| [er-positive](cases/er-positive/SUMMARY.md) | ER positive | false |
| [her2-missing](cases/her2-missing/SUMMARY.md) | HER2 absent | unknown |
| [her2-equivocal](cases/her2-equivocal/SUMMARY.md) | HER2 unresolved | unknown |
| [tnbc-t1b-nodes-missing](cases/tnbc-t1b-nodes-missing/SUMMARY.md) | Small tumor, no N assessment | unknown |
| [tnbc-metastatic](cases/tnbc-metastatic/SUMMARY.md) | cM1 | false; outside track population |
| [tnbc-metastasis-missing](cases/tnbc-metastasis-missing/SUMMARY.md) | No M assessment | unknown |
| [diagnosis-absent](cases/diagnosis-absent/SUMMARY.md) | Unanchored results, no qualifying Condition | false |
| [tnbc-t1c-n0-cm](cases/tnbc-t1c-n0-cm/SUMMARY.md) | 1.5 cm counterpart to 15 mm | true |
| [tnbc-t2-n0](cases/tnbc-t2-n0/SUMMARY.md) | TNBC, cT2 cN0 cM0, 25 mm | true |

## Validation and participant execution

Run the standard-library fixture check from the repository root:

```sh
python3 use-cases/breast-cancer/scripts/validate_fixtures.py
```

The checker validates manifest coverage, references, patient/cancer linkage, chronology, declared codes, pinned LOINC observation versions, the 10 mm boundary, unit consistency, and all 104 typed assertions against the documented contract. It is a fixture consistency check, not an independent clinical algorithm, a CQL evaluator, or a substitute for the HL7 validator.

See [validation evidence](../validation/README.md) for the official FHIR validator run, exact versions, diagnostics, and terminology limits. Participant-generated CQL/ELM and `$apply` behavior have not been executed by this fixture preparation. Participants must report their own translation, execution, and FHIR-server round-trip results, as required by the shared track.
