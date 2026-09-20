library BreastCancerNeoadjuvantLocalConcepts

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon

codesystem "Breast Cancer Neoadjuvant Local Codes": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-neoadjuvant-local'
code "Estrogen Receptor Result": 'estrogen-receptor-result' from "Breast Cancer Neoadjuvant Local Codes"
code "Progesterone Receptor Result": 'progesterone-receptor-result' from "Breast Cancer Neoadjuvant Local Codes"
code "HER2 Result": 'her2-result' from "Breast Cancer Neoadjuvant Local Codes"
code "Clinical M Result": 'clinical-m-result' from "Breast Cancer Neoadjuvant Local Codes"
code "Clinical N Result": 'clinical-n-result' from "Breast Cancer Neoadjuvant Local Codes"
code "Clinical T Result": 'clinical-t-result' from "Breast Cancer Neoadjuvant Local Codes"

context Patient
