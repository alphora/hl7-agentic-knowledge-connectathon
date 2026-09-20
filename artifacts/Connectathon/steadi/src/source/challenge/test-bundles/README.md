# Synthetic patient test bundles

This directory contains the shared execution fixtures for the older-adult
fall-risk use case. Every case is synthetic and uses FHIR R4 4.0.1 resources.

## Common evaluation context

- Measurement period: 2026-01-01 through 2026-12-31, inclusive
- Ambulatory encounter: 2026-06-15
- Eligible-patient birth date: 1945-01-01
- Younger-patient birth date: 1965-06-16
- Shared coded Questionnaire: [questionnaire.json](questionnaire.json)
- Questionnaire canonical:
  `https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/Questionnaire/steadi-three-question-screen|0.2.0`
- Synthetic resources carry the standard `HTEST` security label from
  `http://terminology.hl7.org/CodeSystem/v3-ActReason`.

Each case directory contains:

- `bundle.json`: a FHIR R4 collection Bundle containing a Patient, an
  ambulatory Encounter, and a QuestionnaireResponse when the scenario has one;
- `extracted-bundle.json`: the normalized set of resources expected from SDC
  Observation-based extraction;
- `assertions.json`: engine-neutral expected values for the eight required
  CQL expressions and the extraction result; and
- `SUMMARY.md`: a human-readable explanation of the data and expected result.

The canonical uses a repository-owned namespace. A participant may map it to
the canonical used by its generated Questionnaire, but must preserve the three
linkIds, question codes, and asserted behavior.

## Coded Questionnaire contract

| linkId | LOINC 2.81 | Display | Answer type |
| --- | --- | --- | --- |
| `unsteady` | `100257-5` | Feel unsteady when standing or walking | Boolean |
| `worries-about-falling` | `97878-3` | Worried about falling | Boolean |
| `fallen-in-past-year` | `52552-7` | Falls in the past year | Boolean |

The codes were resolved and verified as active through ReasonHub on
2026-08-26. The track does not assign a panel code because these three items
are a deliberate subset rather than a claim to implement the complete LOINC
Stay Independent panel.

FHIR R4 `QuestionnaireResponse.item` has no `code` element. Each response
therefore retains Boolean answers and references the versioned shared
Questionnaire, where the LOINC codes are maintained. SDC extraction repeats
those codes on the resulting `Observation.code`. This preserves conformant
FHIR and straightforward Boolean logic in CQL.

A response is complete only when its status is `completed` and all three
items contain a usable Boolean answer. Increased fall risk is true when the
response is complete and at least one answer is true. It is false when the
response is complete and all answers are false. It is null when the response is
incomplete or absent.

## SDC extraction contract

The shared Questionnaire declares the SDC
[`sdc-questionnaire-extr-obsn`](https://hl7.org/fhir/uv/sdc/STU4/en/StructureDefinition-sdc-questionnaire-extr-obsn.html)
profile, enables `sdc-questionnaire-observationExtract`, and supplies the
`survey` Observation category. The four completed responses are expected to
produce three final Observations. Each Observation copies the patient,
encounter, authored time, author, coded question, and Boolean answer, and its
`derivedFrom` points to the source QuestionnaireResponse.

SDC [`QuestionnaireResponse/$extract`](https://hl7.org/fhir/uv/sdc/STU4/en/OperationDefinition-QuestionnaireResponse-extract.html)
can return a transaction Bundle. To make cross-implementation comparisons
stable, each `extracted-bundle.json` is instead a collection Bundle containing
only the normalized expected resource set. Its deterministic `fullUrl` values
identify fixture resources and are not part of the semantic assertion; the
track does not prescribe server-local URLs, request verbs, or
conditional-create behavior.

The incomplete response and absent-response cases intentionally have an empty
expected resource set and `invocationExpected=false`. The track does not invoke
the baseline extraction operation until a completed QuestionnaireResponse is
available, so a partial affirmative answer cannot leak into downstream logic
as if the assessment were complete.

## Cases

| Case | Main condition | Expected risk | Extracted Observations |
| --- | --- | --- | ---: |
| [younger-than-65](cases/younger-than-65/SUMMARY.md) | complete screen, age below threshold | false; outside population | 3 |
| [eligible-all-no](cases/eligible-all-no/SUMMARY.md) | complete screen, all answers false | false | 3 |
| [eligible-unsteady-yes](cases/eligible-unsteady-yes/SUMMARY.md) | unsteady answer true | true | 3 |
| [eligible-prior-fall-yes](cases/eligible-prior-fall-yes/SUMMARY.md) | prior-fall answer true | true | 3 |
| [eligible-incomplete-response](cases/eligible-incomplete-response/SUMMARY.md) | one required answer missing | null | 0; no invocation |
| [eligible-no-response](cases/eligible-no-response/SUMMARY.md) | no QuestionnaireResponse | null | 0; no invocation |

## Assertion format

Every assertion has an expression name and an expected typed value. Boolean
unknown is represented as JSON `null` with `"semantics": "unknown"`; it is
not interchangeable with `false`, an omitted result, or an execution error.

A test harness may add raw engine output and status fields in a separate result
file. It should not modify the shared assertions.

## Fixture validation status

On 2026-08-26, all 13 FHIR files passed the HL7 FHIR validator 6.10.2 with
FHIR R4 4.0.1 and `hl7.fhir.uv.sdc#4.0.0` with no errors. Remaining warnings
are limited to omitted generated narratives, the deliberately missing required
answer in the incomplete fixture, and LOINC validation being disabled in that
validator run. Exact ReasonHub lookups independently confirmed all three LOINC
2.81 codes and displays as active. Cross-file checks also confirmed that every
completed answer is reproduced exactly in the expected Observation and that
the original eight CQL assertions remain unchanged.
