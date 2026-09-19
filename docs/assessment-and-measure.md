# STEADI assessment and measure contract

All rules below come from the supplied track at revision 5034ccd6bc5971aa7e366b6b0df0b23caffe4f46. No IEHP/HCSC customer guidance applies.

| Determination | Faithful interpretation | Implementation status |
| --- | --- | --- |
| In Screening Population | Age at least 65, ambulatory encounter, community-dwelling context, excluding inpatient/hospice/LTC | Assessment integration pending; period/encounter eligibility implemented in measure |
| Completed Three Question Screen | One completed QuestionnaireResponse with all three usable Boolean answers | Implemented in measure helper; CRL shared-response integration pending |
| At Increased Fall Risk | Completed and any Yes -> true; completed all No -> false; incomplete/absent -> null | Local-answer CRL core demonstrated; not shared-fixture acceptance |
| Exercise Intervention Applicable | In population and increased risk | CRL communication action demonstrated; final input integration pending |
| Consider Multifactorial Intervention | Same applicability, distinct individualized grade C guidance | Separate CRL communication action demonstrated |
| Initial Population | Patient has an eligible ambulatory encounter within the period | Authored Measure library |
| Denominator | Initial Population | Authored Measure library |
| Numerator | Denominator and a completed screen in the period linked to an eligible encounter | Authored Measure library |

The Questionnaire is reused unchanged, including its versioned canonical, required Boolean items, LOINC 2.81 codes and three linkIds. Its upstream copyright and metadata remain intact. The three items are a deliberate subset, not a claim to implement a complete LOINC panel.

The measure is a patient-based proportion and a process measure. It does not measure intervention adherence, fall reduction, quality of treatment, or CMS139FHIR equivalence. An all-No response is a completed screen and counts in the numerator. A partial Yes response does not.

Track operational choices in the measure:
- Calculate age at the linked encounter start.
- Both encounter start and response authored time must lie in the supplied inclusive measurement period.
- Require matching patient and encounter references.
- Count a patient once if any qualifying encounter has a complete response; do not merge answers across responses.
- Community residence and non-hospice/non-LTC context are an explicit track parameter, not inferred from an AMB code. The supplied fixtures establish that context; broader deployment must establish it separately.
- Duplicate instances of a required item or multiple answers cause an evaluation error rather than selecting an arbitrary answer. This is malformed-input handling, not a negative screen.

The Measure is authored independently because the operator confirmed CRL has no Measure authoring construct. Its population expressions are in SteadiMeasure.cql. Assessment and guidance remain on the CRL -> generated CQL/FHIR -> native $apply path. Measure evaluation uses the native measure command corresponding to Measure/$evaluate-measure.

The native CRL probe is isolated under the ignored .cache/preflight/crl-core directory. Its local answer codes and generated linkIds are not the supplied LOINC/Questionnaire contract. Successful generation there proves the native mechanism, not completion of the challenge.
