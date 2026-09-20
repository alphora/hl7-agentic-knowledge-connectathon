library BreastCancerNeoadjuvantExternalElements

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon
include BreastCancerNeoadjuvantExternalConcepts

context Patient

define "Diagnosis Records":
  [Condition: BreastCancerNeoadjuvantExternalConcepts."Invasive Breast Carcinoma"]

define "Estrogen Receptor Result Source 1":
  [Observation: { System.Code { system: 'http://loinc.org', code: '85337-4' } }]

define "Progesterone Receptor Result Source 1":
  [Observation: { System.Code { system: 'http://loinc.org', code: '85339-0' } }]

define "HER2 Result Source 1":
  [Observation: { System.Code { system: 'http://loinc.org', code: '48676-1' } }]

define "Clinical M Result Source 1":
  [Observation: { System.Code { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'clinical-m' } }]

define "Clinical N Result Source 1":
  [Observation: { System.Code { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'clinical-n' } }]

define "Clinical T Result Source 1":
  [Observation: { System.Code { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'clinical-t' } }]
