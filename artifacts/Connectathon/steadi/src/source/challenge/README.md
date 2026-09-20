# Older-adult fall risk (STEADI)

This case supplies a traceable source corpus, synthetic FHIR R4 patient
bundles, a shared coded Questionnaire, and engine-neutral expected results.
Participants turn the source material into evidence, assessment, guidance,
and screening-completion measure artifacts.

## Clinical question

For a community-dwelling adult age 65 years or older seen in ambulatory care:

1. Is the patient in scope for fall-risk screening?
2. Was the CDC STEADI three-question screen completed?
3. Does the completed screen indicate increased fall risk?
4. Which evidence-linked action is applicable?
5. Across a measurement period, what proportion of eligible patients completed
   the screen?

The three screening questions ask whether the patient:

- feels unsteady when standing or walking;
- worries about falling; or
- has fallen in the past year.

For this track, a completed screen indicates increased fall risk when any
answer is yes. Missing or incomplete answers remain unknown and must not be
treated as a negative screen.

The track includes exercise guidance linked to the USPSTF grade B
recommendation and individualized consideration of multifactorial
interventions linked to the grade C recommendation. It does not diagnose a
fall-related condition, select a specific treatment, or order an intervention.

## Case contents

- [Source manifest](sources/manifest.yaml) and [raw source snapshots](sources/raw/)
- [MARP overview](slides/connectathon-track-overview.md) and
  [rendered PDF](slides/connectathon-track-overview.pdf)
- [Synthetic patient test bundles](test-bundles/README.md), a shared coded
  [Questionnaire](test-bundles/questionnaire.json), SDC extraction
  expectations, assertions, and a case summary for every bundle

The raw corpus contains only snapshots whose current redistribution basis is
recorded in the manifest. Standards references and CMS139FHIR remain link-only.
CMS139FHIR is a comparison point; it is not copied, and the track-authored
measure must not claim equivalence to it.

## Participant deliverables

The expected output includes:

| Knowledge role | Expected artifact |
| --- | --- |
| Evidence and population definitions | `Evidence`, `EvidenceVariable` |
| Three-question assessment | `Questionnaire`, reusable logic |
| Recommendation workflow | `PlanDefinition`, `ActivityDefinition`, `Library` |
| Screening-completion measure | `Measure`, `Library` |
| Terminology and package metadata | `ValueSet`, `ImplementationGuide` |
| Executable logic | CQL source and ELM JSON |
| Distribution | FHIR R4 NPM package with exact dependency versions |

FHIR R4 does not define `Citation`; an R4 baseline submission should use
available provenance and related-artifact elements. Any R5 variant must be
clearly separated from the R4 baseline.

## SDC extraction contract

The input fixtures exercise the SDC Observation-based extraction pattern.
Each completed QuestionnaireResponse references the same versioned,
LOINC-coded Questionnaire. Its expected extracted Observations are supplied as
a normalized resource set so participants can compare `$extract` behavior
across implementations without depending on server-specific transaction
details. Incomplete and absent responses remain explicit negative extraction
cases.

The [fixture contract](test-bundles/README.md#sdc-extraction-contract) defines
the coded questions, copied Observation fields, extraction invocation rules,
and Boolean/null semantics.

## Required executable behavior

The shared assertions use these expression names:

- `In Screening Population`
- `Completed Three Question Screen`
- `At Increased Fall Risk`
- `Exercise Intervention Applicable`
- `Consider Multifactorial Intervention`
- `Initial Population`
- `Denominator`
- `Numerator`

The first five expressions describe patient-level assessment and guidance. The
last three describe a track-authored screening-completion process measure.
Incomplete or absent screening data produces an unknown increased-risk result,
while the measure numerator remains false.

Follow the shared [participant and interoperability requirements](../../README.md),
including independent CQL execution, FHIR round-trip testing, exact versions,
source traceability, and process evidence. FHIR validation and CQL compilation
are necessary, but they are not clinical approval.

All patient data is synthetic. This material is for Connectathon testing and
education, not clinical use.
