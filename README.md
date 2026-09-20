# Alphora HL7 Agentic Knowledge Connectathon

A source-to-execution knowledge workflow: author in CRL and CEL, generate CQL and FHIR, and manage artifacts and verification with KELP.

This repository is being rebuilt as a KELP content project for the STEADI and breast-cancer neoadjuvant challenges. The previous direct-authored assessment implementation has been removed from the active project and moved to local temporary staging. It is not the demo deliverable.

## Demo status

Rebuild in progress. Artifact intake, lifecycle saves and runnable demo verification are not yet complete. The calculation-only STEADI source currently exposes a CRL generation defect; diagnostic Observation support for the breast-cancer contract remains incomplete. The preserved Measure definition still needs its replacement generated-logic connection completed. Do not treat the current main branch as a finished demonstration.

Each use case will live under `artifacts/`, with source, CRL, CEL, generated CQL/FHIR, tests and a KELP-managed `reports/` folder. Use the KELP and CRL VS Code extensions to load and run the artifacts; exact verified commands will be added after execution.

## Companion resources

Measures are supported by our established workflow. CRL generates the supporting logic and artifacts; the agent manually authors the `Measure` resource alongside them. Because that resource is straightforward to author, direct generation has not been a priority, although it is on the backlog. This demonstration uses that established approach.

`Evidence` and `EvidenceVariable` are also authored manually alongside the other FHIR resources. Direct CRL support for those resource families is under consideration. `MeasureReport` results belong with the tests alongside `Questionnaire` and `QuestionnaireResponse`.

Generated Questionnaire identifiers are preserved. We intentionally do not patch generated identifiers to match the challenge's fixed linkIds. Exact capability differences and actual test results will be documented in the per-artifact reports.

This is a connectathon demonstration, not a claim of clinical validation or production readiness. Cross-participant storage roundtrips and human clinical review are not included in this demonstration work.
