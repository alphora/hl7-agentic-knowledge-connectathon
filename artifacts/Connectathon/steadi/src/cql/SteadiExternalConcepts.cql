library SteadiExternalConcepts

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon

valueset "STEADI Question Codes": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/steadi-steadi-question-codes'

context Patient
