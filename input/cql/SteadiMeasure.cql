library SteadiMeasure version '0.1.0'

using FHIR version '4.0.1'

parameter "Measurement Period" Interval<DateTime>
  default Interval[@2026-01-01T00:00:00.000Z, @2026-12-31T23:59:59.000Z]

/*
  The supplied track fixes the community-dwelling, non-hospice, non-LTC context.
  Its fixtures do not encode residence or hospice status. This is an explicit
  track-context parameter, not an inference from an AMB encounter.
*/
parameter "Track Context Confirmed" Boolean default true

context Patient

define function "References"(reference String, resourceType String, resourceId String):
  reference = resourceType + '/' + resourceId
    or EndsWith(reference, '/' + resourceType + '/' + resourceId)

define "Ambulatory Encounters":
  [Encounter] E
    where E.class.system.value = 'http://terminology.hl7.org/CodeSystem/v3-ActCode'
      and E.class.code.value = 'AMB'
      and "References"(E.subject.reference.value, 'Patient', Patient.id.value)
      and E.period.start.value during "Measurement Period"

define function "Eligible Encounter"(E FHIR.Encounter):
  "Track Context Confirmed"
    and CalculateAgeInYearsAt(Patient.birthDate.value, date from E.period.start.value) >= 65

define "Recognized Questionnaires":
  {
    'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/Questionnaire/steadi-three-question-screen|0.2.0'
  }

define "Period Screens":
  [QuestionnaireResponse] R
    where R.questionnaire.value in "Recognized Questionnaires"
      and "References"(R.subject.reference.value, 'Patient', Patient.id.value)
      and R.authored.value during "Measurement Period"
      and R.status.value in { 'completed', 'amended', 'in-progress' }

define function "Screen Answer"(R FHIR.QuestionnaireResponse, linkId String):
  (
    singleton from (
      R.item I
        where I.linkId.value = linkId
        return (singleton from I.answer).value as FHIR.boolean
    )
  ).value

define function "Screen Complete"(R FHIR.QuestionnaireResponse):
  Coalesce(R.status.value = 'completed', false)
    and "Screen Answer"(R, 'unsteady') is not null
    and "Screen Answer"(R, 'worries-about-falling') is not null
    and "Screen Answer"(R, 'fallen-in-past-year') is not null

define "Initial Population":
  exists ("Ambulatory Encounters" E where "Eligible Encounter"(E))

define "Denominator":
  "Initial Population"

define "Numerator":
  "Denominator"
    and exists (
      "Period Screens" R
        where "Screen Complete"(R)
          and exists (
            "Ambulatory Encounters" E
              where "Eligible Encounter"(E)
                and "References"(R.encounter.reference.value, 'Encounter', E.id.value)
          )
    )
