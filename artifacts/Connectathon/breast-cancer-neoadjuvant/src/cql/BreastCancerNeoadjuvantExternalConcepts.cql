library BreastCancerNeoadjuvantExternalConcepts

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon

valueset "Invasive Breast Carcinoma": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-invasive-breast-carcinoma'
valueset "Receptor Results": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-receptor-results'
valueset "Definitive Receptor Results": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-definitive-receptor-results'
valueset "Negative Receptor Result": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-negative-receptor-result'
valueset "Estrogen Receptor Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-estrogen-receptor-test'
valueset "Progesterone Receptor Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-progesterone-receptor-test'
valueset "HER2 Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-her2-test'
valueset "Clinical M Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-m-test'
valueset "Clinical M Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-m-categories'
valueset "Clinical M Qualifying Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-m-qualifying-categories'
valueset "Clinical N Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-n-test'
valueset "Clinical N Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-n-categories'
valueset "Clinical N Qualifying Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-n-qualifying-categories'
valueset "Clinical T Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-t-test'
valueset "Clinical T Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-t-categories'
valueset "Clinical T Qualifying Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-t-qualifying-categories'

context Patient
