# Eligible adult with an incomplete response

Fixture id: `eligible-incomplete-response`

## Scenario

Tests that a present yes answer does not bypass the explicit completeness requirement when another required answer is missing.

## Bundle contents

- Patient birth date: `1945-01-01`
- Finished ambulatory Encounter on `2026-06-15`
- QuestionnaireResponse `in-progress` with `unsteady=true`, `worries-about-falling=false`.
- All identifiers and data are synthetic.

## Expected behavior

The patient remains eligible, but risk and dependent guidance are unknown. The screening-completion numerator is false.

| Expression | Expected |
| --- | --- |
| `In Screening Population` | `true` |
| `Completed Three Question Screen` | `false` |
| `At Increased Fall Risk` | null (unknown) |
| `Exercise Intervention Applicable` | null (unknown) |
| `Consider Multifactorial Intervention` | null (unknown) |
| `Initial Population` | `true` |
| `Denominator` | `true` |
| `Numerator` | `false` |

## Expected SDC extraction

`QuestionnaireResponse/$extract` is not invoked because the response status is
`in-progress`. The normalized expected resource set is empty. In particular,
the available `unsteady=true` answer is not emitted as a final Observation
before the required assessment is complete.

## Files

- [FHIR R4 Bundle](bundle.json)
- [Shared coded Questionnaire](../../questionnaire.json)
- [Expected extracted resources](extracted-bundle.json)
- [Machine-readable assertions](assertions.json)
