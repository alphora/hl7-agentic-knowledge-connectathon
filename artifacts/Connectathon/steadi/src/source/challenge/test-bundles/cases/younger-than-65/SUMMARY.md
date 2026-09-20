# Adult younger than 65

Fixture id: `younger-than-65`

## Scenario

Confirms that the age and ambulatory-context population gate is applied even when a complete screening response exists.

## Bundle contents

- Patient birth date: `1965-06-16`
- Finished ambulatory Encounter on `2026-06-15`
- QuestionnaireResponse `completed` with `unsteady=false`, `worries-about-falling=false`, `fallen-in-past-year=false`.
- All identifiers and data are synthetic.

## Expected behavior

The screen is complete, but the patient is outside the screening and measure populations. Guidance and measure membership are false.

| Expression | Expected |
| --- | --- |
| `In Screening Population` | `false` |
| `Completed Three Question Screen` | `true` |
| `At Increased Fall Risk` | `false` |
| `Exercise Intervention Applicable` | `false` |
| `Consider Multifactorial Intervention` | `false` |
| `Initial Population` | `false` |
| `Denominator` | `false` |
| `Numerator` | `false` |

## Expected SDC extraction

Extraction is independent of the age-based clinical population gate. The
completed response is therefore extracted into three final, survey-category
Observations even though the patient is outside the screening population.

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
