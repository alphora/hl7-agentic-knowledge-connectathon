library Steadi version '0.1.0'
using FHIR version '4.0.1'
include SteadiMeasure version '0.1.0' called Screening
parameter "Encounter Id" String default null
parameter "Questionnaire Response Id" String default null
context Patient

/* Direct-authored companion: one selected encounter and one coherent response.
   Measure populations keep their period-wide scope. */
define "Assessment Encounter":
  singleton from (
    [Encounter] E
      where Screening."References"(E.subject.reference.value, 'Patient', Patient.id.value)
        and ("Encounter Id" is null or E.id.value = "Encounter Id")
  )
define "Assessment Response":
  singleton from (
    Screening."Period Screens" R
      where Screening."References"(R.encounter.reference.value, 'Encounter', "Assessment Encounter".id.value)
        and ("Questionnaire Response Id" is null or R.id.value = "Questionnaire Response Id")
  )
define "In Screening Population":
  exists (
    Screening."Ambulatory Encounters" E
      where E.id.value = "Assessment Encounter".id.value
        and Screening."Eligible Encounter"(E)
  )
define "Completed Three Question Screen":
  Coalesce(Screening."Screen Complete"("Assessment Response"), false)
define "At Increased Fall Risk":
  if "Completed Three Question Screen" then
    Screening."Screen Answer"("Assessment Response", 'unsteady')
      or Screening."Screen Answer"("Assessment Response", 'worries-about-falling')
      or Screening."Screen Answer"("Assessment Response", 'fallen-in-past-year')
  else null
define "Exercise Intervention Applicable":
  "In Screening Population" and "At Increased Fall Risk"
define "Consider Multifactorial Intervention":
  "In Screening Population" and "At Increased Fall Risk"
define "Initial Population": Screening."Initial Population"
define "Denominator": Screening."Denominator"
define "Numerator": Screening."Numerator"


define "Exercise fall-prevention guidance Message":
  'Exercise interventions are recommended for community-dwelling adults aged 65 years or older at increased fall risk (USPSTF grade B). This guidance does not select or order a particular intervention.'
define "Individualized multifactorial consideration Message":
  'Individualize whether to offer multifactorial fall-prevention interventions for community-dwelling adults aged 65 years or older at increased fall risk, considering prior falls, comorbidities and patient preferences (USPSTF grade C). This is not a routine intervention order.'
