library BreastCancerNeoadjuvantLocalElements

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon
include BreastCancerNeoadjuvantLocalConcepts

context Patient

define "Estrogen Receptor Result Records":
  [Observation: BreastCancerNeoadjuvantLocalConcepts."Estrogen Receptor Result"]

define "Progesterone Receptor Result Records":
  [Observation: BreastCancerNeoadjuvantLocalConcepts."Progesterone Receptor Result"]

define "HER2 Result Records":
  [Observation: BreastCancerNeoadjuvantLocalConcepts."HER2 Result"]

define "Clinical M Result Records":
  [Observation: BreastCancerNeoadjuvantLocalConcepts."Clinical M Result"]

define "Clinical N Result Records":
  [Observation: BreastCancerNeoadjuvantLocalConcepts."Clinical N Result"]

define "Clinical T Result Records":
  [Observation: BreastCancerNeoadjuvantLocalConcepts."Clinical T Result"]
