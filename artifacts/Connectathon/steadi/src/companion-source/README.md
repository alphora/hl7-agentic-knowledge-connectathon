# STEADI manual companion inputs

This entity contains 1 Measure, 2 Evidence and 7 EvidenceVariable resources. They are authorized manual companions to the CRL-generated CQL/FHIR, not an alternative clinical implementation.

The Measure wrapper references the generated `Library/SteadiInterface|0.0.0` and its authored `Initial Population`, `Denominator` and `Numerator` expressions. CRL supports the supporting logic and artifacts; authoring this simple wrapper manually is our established approach. Direct Measure generation is backlog work. Evidence and EvidenceVariable are also manually authored because CRL does not currently generate those resource families.

The Evidence resources retain their supplied-source findings and citations. Their documentation links point to the corresponding generated exercise and multifactorial guidance ActivityDefinitions at version0.0.0. Those links are not evidence citations or new clinical requirements. EvidenceVariable inputs are byte-identical to the previously prepared manual inputs. Manual resource versions remain0.1.0; their generated dependencies explicitly use0.0.0.

Copy only `fhir/<ResourceType>/*.json` into matching final generated FHIR folders after the CRL producer finishes. The lead owns that assembly. Do not copy prior handwritten CQL/Library artifacts. Do not treat earlier MeasureReports as verification of this changed generated support; the lead runs the current native operation.

Reproduction and audit are maintained in the tooling workspace at `tmp/connectathon-steadi-support-641/assemble-final-companions.py` and `final-companion-evidence/final-companion-audit.json`. The audit checked10resource identities/canonicals,11internal/versioned references and unchanged generated resources. It is not full FHIR-profile validation or native execution.

The Measure description/guidance records remaining shared-input limitations: original QuestionnaireResponse completion/status and association, encounter/period filtering, and local versus shared LOINC-coded answers. The named Boolean-expression verification does not establish those input contracts.
