# Eligible adult with a prior fall

Fixture id: `eligible-prior-fall-yes`

## Scenario

Exercises a positive screen driven by the prior-fall item and confirms that the three trigger questions have equivalent positive-screen semantics.

## Bundle contents

- Patient birth date: `1945-01-01`
- Finished ambulatory Encounter on `2026-06-15`
- QuestionnaireResponse `completed` with `unsteady=false`, `worries-about-falling=false`, `fallen-in-past-year=true`.
- All identifiers and data are synthetic.

## Expected behavior

The completed screen indicates increased risk. Exercise guidance applies and multifactorial intervention is considered individually.

| Expression | Expected |
| --- | --- |
| `In Screening Population` | `true` |
| `Completed Three Question Screen` | `true` |
| `At Increased Fall Risk` | `true` |
| `Exercise Intervention Applicable` | `true` |
| `Consider Multifactorial Intervention` | `true` |
| `Initial Population` | `true` |
| `Denominator` | `true` |
| `Numerator` | `true` |

## Expected SDC extraction

The completed response is extracted into three final, survey-category
Observations. Each Observation refers back to the QuestionnaireResponse through
`derivedFrom`.

| linkId | LOINC 2.81 | `valueBoolean` |
| --- | --- | --- |
| `unsteady` | `100257-5` | `false` |
| `worries-about-falling` | `97878-3` | `false` |
| `fallen-in-past-year` | `52552-7` | `true` |

## Files

- [FHIR R4 Bundle](bundle.json)
- [Shared coded Questionnaire](../../questionnaire.json)
- [Expected extracted resources](extracted-bundle.json)
- [Machine-readable assertions](assertions.json)
