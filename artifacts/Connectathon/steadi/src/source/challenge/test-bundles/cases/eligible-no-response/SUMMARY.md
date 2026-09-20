# Eligible adult with no response

Fixture id: `eligible-no-response`

## Scenario

Tests absence of the assessment as distinct from a completed negative screen.

## Bundle contents

- Patient birth date: `1945-01-01`
- Finished ambulatory Encounter on `2026-06-15`
- No QuestionnaireResponse is present.
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

There is no QuestionnaireResponse on which to invoke
`QuestionnaireResponse/$extract`. The normalized expected resource set is
therefore empty.

## Files

- [FHIR R4 Bundle](bundle.json)
- [Shared coded Questionnaire](../../questionnaire.json)
- [Expected extracted resources](extracted-bundle.json)
- [Machine-readable assertions](assertions.json)
