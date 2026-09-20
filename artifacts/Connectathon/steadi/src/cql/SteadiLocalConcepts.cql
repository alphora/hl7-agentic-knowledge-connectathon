library SteadiLocalConcepts

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon

codesystem "Steadi Local Codes": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/steadi-local'
code "Unsteady": 'unsteady' from "Steadi Local Codes"
code "Worries About Falling": 'worries-about-falling' from "Steadi Local Codes"
code "Fallen In Past Year": 'fallen-in-past-year' from "Steadi Local Codes"

context Patient
