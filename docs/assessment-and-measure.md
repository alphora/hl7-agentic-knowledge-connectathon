# STEADI assessment and measure contract

Source: supplied track revision `5034ccd6bc5971aa7e366b6b0df0b23caffe4f46`. No IEHP/HCSC customer guidance applies. The operator approved the direct CQL/FHIR implementation when CRL capabilities were insufficient for this delivery.

| Expression | Implemented meaning |
| --- | --- |
| In Screening Population | The selected patient-associated encounter is ambulatory and within the period; age at that encounter is at least 65 and track context is confirmed |
| Completed Three Question Screen | One selected completed QuestionnaireResponse has all three usable Boolean answers |
| At Increased Fall Risk | Complete any-Yes is true; complete all-No is false; incomplete or absent is unknown, independently of age eligibility |
| Exercise Intervention Applicable | In population AND increased risk |
| Consider Multifactorial Intervention | Same applicability, distinct individualized grade C guidance |
| Initial Population | At least one eligible ambulatory encounter during the measurement period |
| Denominator | Initial Population |
| Numerator | Denominator and one completed screen in the period linked to an eligible encounter |

The shared Questionnaire retains its exact versioned canonical, three required Boolean items and LOINC 2.81 bindings. Completion means status `completed` plus all three answers; an affirmative partial response does not bypass completion. Extraction is allowed for a completed younger patient's response even though guidance is inapplicable.

## Operational choices

Assessment uses the explicitly selected encounter. The adapter requires `Encounter Id` and its guidance target to agree. It selects the matching QuestionnaireResponse by explicit response ID when supplied, otherwise by a singleton match on questionnaire, patient, encounter and period. Multiple matches are an error; answers are never pooled. Duplicate required items or answers produce cardinality errors. Missing/wrong-type answers remain unusable, not false.

The Measure is period-wide and patient-based. A patient counts once if any qualifying encounter has one completed screen. An all-No screen counts in the numerator. This is a screening-completion process measure, not fall reduction, treatment quality, adherence, or CMS139FHIR equivalence.

Age is calculated at encounter start. Encounter start and response authored time lie within the inclusive measurement period. The supplied fixtures establish community residence and non-hospice/non-LTC context through the explicit `Track Context Confirmed` parameter. An AMB code alone does not establish those facts for general use.

The assessment includes `SteadiMeasure` for shared answer/eligibility helpers and delegates the three measure expressions to that Library. Guidance logic is defined once in CQL and referenced by the authored PlanDefinition. Both guidance actions communicate information; neither orders an intervention or selects a specific treatment. Each points to its corresponding Evidence resource.
