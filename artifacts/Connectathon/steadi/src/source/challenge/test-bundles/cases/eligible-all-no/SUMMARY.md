# Eligible adult with all answers no

Fixture id: `eligible-all-no`

## Scenario

Establishes the completed negative-screen path and separates a false risk result from missing data.

## Bundle contents

- Patient birth date: `1945-01-01`
- Finished ambulatory Encounter on `2026-06-15`
- QuestionnaireResponse `completed` with `unsteady=false`, `worries-about-falling=false`, `fallen-in-past-year=false`.
- All identifiers and data are synthetic.

## Expected behavior

The patient is eligible, the screen is complete, increased risk is false, and the screening-completion numerator is true.

| Expression | Expected |
| --- | --- |
| `In Screening Population` | `true` |
| `Completed Three Question Screen` | `true` |
| `At Increased Fall Risk` | `false` |
| `Exercise Intervention Applicable` | `false` |
| `Consider Multifactorial Intervention` | `false` |
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
| `fallen-in-past-year` | `52552-7` | `false` |

## Files

- [FHIR R4 Bundle](bundle.json)
- [Shared coded Questionnaire](../../questionnaire.json)
- [Expected extracted resources](extracted-bundle.json)
- [Machine-readable assertions](assertions.json)
