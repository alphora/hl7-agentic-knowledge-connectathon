# Completed-negative terminal outcome repair

The saved CRL previously had only a positive Oncology Review Guidance activity. A HER2-positive case completed without a terminal communication. An identical-input comparison against the current pinned 4aee604 engine and the available older 4.7.0 binary found identical RequestGroups across all thirteen original cases; this omission existed in the authored package. CRL confirmed that its newer apply development candidate had not been adopted into our delivered runtime.

The operator authorized an explicit negative completion result. CRL now authors `Nothing Recommended` as a CPGCommunicationRequest. A false population gate or a false definitive TNBC/tumor-node assessment reaches this result. Unknown conditions retain null-propagating first-branch exclusions; the definitive-HER2 gate continues to exclude unresolved/equivocal results from completed recommendations. Clinical criteria, source documents, anchors and diagnostic fixture data were not changed.

## Native evidence

`tests/verification/native-terminal` contains fresh raw Library evaluation and PlanDefinition apply responses over all thirteen unchanged original challenge bundles. The verifier checks exact CommunicationRequest identities, RequestGroup references, errors and the scoped negative payload. All thirteen outcome checks pass: four oncology guidance, five explicit negative completions, four unresolved with no terminal communication. All nine generated CQL libraries translate to ELM. The CRL6.4.3 emit_results producer completed all thirteen CEL cases as generated Q/QR pairs; all26 manifest file hashes match. The MCP caller hit its300-second transport limit while the producer continued its final cases; the finished manifest and process exit were verified before saving, without starting a duplicate producer. The existing seven independent scalar-expression differences remain unchanged (97/104).

## Preview and provenance limits

The current CRE preview still interprets the active/confirmed diagnosis filter differently from the native engine and produces the negative population path for every CEL case (five pass, eight fail). Actual CEL-emitted Conditions contain active and confirmed status. This preview discrepancy has been reported to CRL (01M30HDHA7J2QMRTGJHJ7XJ0C3); no clinical criteria were weakened to hide it. Native engine results, not the preview, establish the outcome evidence above. The existing provenance gate retains one source-selection finding and thirteen cockpit-correspondence errors; new terminal nodes have valid source-contract attribution and no over-reach or source-text/hash errors.

## Delivery

The updated FHIR package contains 49 resources including ImplementationGuide. Model and CEL expectations were changed through authored sources; CQL/FHIR were regenerated with CRL tools. The existing manually authored Evidence/EvidenceVariable and fixture terminology companions were restored unchanged after generation. The package is `reports/package/breast-cancer-neoadjuvant-0.0.0.tgz`; its hash is in `reports/package/terminal-package-receipt.json`.

Kit consulted: schema2.13, semantic hash daf1df90d2aa8796f3cbc1de923e1c8e0f4f3d257c3dcd5c492a6ee2ba9caa4c, audit matching. Shared method0.1.1 and focused modeling/verification/provenance skills applied to the synthetic Connectathon scope. No additional customer-review panel or human clinical-acceptance claim.
