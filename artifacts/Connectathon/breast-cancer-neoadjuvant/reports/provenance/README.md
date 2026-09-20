# Breast Cancer provenance: demo evidence

The carrier is `src/provenance/breast-cancer-neoadjuvant.json`. It contains 20 source-first items: complete acknowledgment of the supplied nine-file canonical source packet, plus focused source statements for the review trigger, explicit operational population, indexed diagnosis, Observation selection, receptor interpretation, stage vocabulary, eight typed expressions and three-valued logic. No extra documents or clinical criteria were added. Every item's quoted text was independently checked against its exact UTF-8 byte range.

The anchor hash is `sha256:cb6fc891d28bdc01cb96b5533d0f74f77b0256681b93660d57b7df4b5af84eed`. Supported `normalize_provenance` established the carrier-relative anchor-self path, returned fullyNormalized true and an empty worklist. The source/anchor and upstream sidecar were not edited.

## Source distinctions

The ASCO 2021 TNBC node-positive or T1c-or-higher review criterion is represented through the supplied challenge description and locators; its unprovided full text was not newly imported. Explicit active/confirmed invasive cancer, cM0, indexed-tumor linkage, dates/status and unknown behavior are **track-authored operational choices**, identified as such in their source items. They are not mislabeled as verbatim ASCO recommendations.

The 2022 immunotherapy update concerns a distinct population. NCI professional trial material supplies evidence context with its stated limitations; NCI staging and patient education do not create regimen eligibility, chemotherapy fitness or orders. Pathological N is not used to infer clinical N. Explicit clinical T is used instead of deriving stage from tumor diameter. The manually authored Evidence companions retain separate artifact verification responsibility.

All 22 indexed current references have source attribution, including diagnosis inference, the population gate, the definitive-HER2 gate, the subtype/tumor-node guard and its guidance action. A link establishes the intended source relationship, not proof that filtering, unknown values or native execution are correct. Criterion exports are not separate indexed leaves.

## Current FINAL findings

`validation-final.json` retains the complete actual result; `validation-receipt.json` binds its model, CEL, source and carrier hashes. **Pass false: 14 errors, 22 manual-review findings, 0 warnings.** There are no unresolved references, overreach, uncovered-span, text/hash drift or derivedFrom errors.

- One missed-decision finding remains for `indexed-observation-selection`. Its required subject/focus linkage, final status, effective/issued cutoff and absent-indexed-diagnosis behavior are intentionally not certified by a bare code-based retrieve. This item is not waived or relabeled to hide the gap. Resolve it against the actual author changes and native fixture evidence.
- All 13 frozen CEL cases remain unchecked in CRE/cockpit correspondence: eight no-produced-action findings and five run-error findings. No unsupported run was represented as a grounded path and no case was dropped. These findings are not proof of a native CQL/$apply failure; the actual engine/104-expression results belong to the separate verification evidence.
- Ten manual-review keyword findings and twelve disposition-class waivers reflect broad source inventory, evidence and artifact-contract descriptions. They are not independent review approval. The complete inventory is deliberately distinguished from the smaller executable review rule.

## Manual-review dispositions

The author's disposition is to retain the administrative/definition role **with an explicit scope limit**, not to erase requirements. Source file 2 (use-case overview), source file 3 (source guide), source file 4 (manifest) and source file 5 (fixture contract) contain clinical language, so their operative population, receptor/stage, unknown and selection requirements also appear in specific linked or openly unlinked items. The broad inventory entries do not certify complete implementation.

Source file 6 through source file 9 contain the supplied professional/staging/patient-education excerpts. Their evidence role and restrictions are explicit in the supplied source guide: these are not additional treatment-selection algorithms for this baseline. The TNBC receptor definition is separately linked. The update-population and stage-domain definitions preserve distinctions; neither is permission to expand the review trigger. Packet identity and the general participant README remain source/process obligations, not patient conditions.

No ignored ranges or authored support waivers were introduced. The open input-selection item and unverified cases remain visible. This is proportional connectathon traceability, not clinical production approval or a claim that every source requirement is fulfilled. If the model/CEL changes after the recorded hashes, this snapshot must be revalidated before a current claim.

## Corrected decision and current evidence boundary

Equivocal is now an explicitly recognized receptor-domain value. After the review-population gate, HER2 Result Is Definitive controls entry to the triple-negative and tumor/node condition. An unresolved result does not produce the oncology recommendation. This is ordinary authored decision behavior, not a language gap or a requirement to generate a separate null artifact.

The six diagnostic selected CodeableConcept inputs now retain their external source representations and also provide supported local answers with actual question text. Correctly typed CEL emits 75 of 75 selected answers as CodeableConcept. The prior valueString result came from the earlier authoring form and is not a remaining blanket emitter limitation.

The current original-diagnostic-fixture native rerun is recorded separately under `tests/verification/native-corrected`. At this provenance refresh its acceptance summary was still pending; no new runtime pass is claimed here. Historical `native-current` counts and errors do not certify or describe the corrected model. Standalone named-scalar mismatches remain diagnostic evidence against their specific expression contracts; they do not by themselves show that the population-gated decision returns an inappropriate recommendation.

The source-selection requirement remains visible rather than waived: subject/indexed-tumor focus, final status and date filtering must not be inferred from successful one-record fixtures. The gated decision and independent scalar/source contracts are evaluated separately. Normalization is fully complete with no carrier changes or worklist. The current validator still reports pass false with 14 errors, 22 manual reviews and 0 warnings; none are unresolved-reference, overreach, source/hash-drift or derivedFrom errors.
