library SteadiLocalElements

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon
include SteadiLocalConcepts

context Patient

define "Unsteady Records":
  [Observation: SteadiLocalConcepts."Unsteady"]

define "Worries About Falling Records":
  [Observation: SteadiLocalConcepts."Worries About Falling"]

define "Fallen In Past Year Records":
  [Observation: SteadiLocalConcepts."Fallen In Past Year"]
