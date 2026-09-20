# Breast Cancer provenance: demo evidence

The carrier is `src/provenance/breast-cancer-neoadjuvant.json`. It contains 20 source-first items: complete acknowledgment of the supplied nine-file canonical source packet, plus focused source statements for the review trigger, explicit operational population, indexed diagnosis, Observation selection, receptor interpretation, stage vocabulary, eight typed expressions and three-valued logic. No extra documents or clinical criteria were added. Every item's quoted text was independently checked against its exact UTF-8 byte range.

The anchor hash is `sha256:cb6fc891d28bdc01cb96b5533d0f74f77b0256681b93660d57b7df4b5af84eed`. Supported `normalize_provenance` established the carrier-relative anchor-self path, returned fullyNormalized true and an empty worklist. The source/anchor and upstream sidecar were not edited.

## Source distinctions

The ASCO 2021 TNBC node-positive or T1c-or-higher review criterion is represented through the supplied challenge description and locators; its unprovided full text was not newly imported. Explicit active/confirmed invasive cancer, cM0, indexed-tumor linkage, dates/status and unknown behavior are **track-authored operational choices**, identified as such in their source items. They are not mislabeled as verbatim ASCO recommendations.

The 2022 immunotherapy update concerns a distinct population. NCI professional trial material supplies evidence context with its stated limitations; NCI staging and patient education do not create regimen eligibility, chemotherapy fitness or orders. Pathological N is not used to infer clinical N. Explicit clinical T is used instead of deriving stage from tumor diameter. The manually authored Evidence companions retain separate artifact verification responsibility.

All 19 indexed current references have source attribution, including diagnosis inference and the single guidance branch/action. A link establishes the intended source relationship, not proof that filtering, unknown values or native execution are correct. Criterion exports are not separate indexed leaves.

## Current FINAL findings

`validation-final.json` retains the complete actual result; `validation-receipt.json` binds its model, CEL, source and carrier hashes. **Pass false: 14 errors, 22 manual-review findings, 0 warnings.** There are no unresolved references, overreach, uncovered-span, text/hash drift or derivedFrom errors.

- One missed-decision finding remains for `indexed-observation-selection`. Its required subject/focus linkage, final status, effective/issued cutoff and absent-indexed-diagnosis behavior are intentionally not certified by a bare code-based retrieve. This item is not waived or relabeled to hide the gap. Resolve it against the actual author changes and native fixture evidence.
- All 13 frozen CEL cases remain unchecked in CRE/cockpit correspondence with run-error. No unsupported run was represented as a grounded path and no case was dropped. These findings are not proof of a native CQL/$apply failure; the actual engine/104-expression results belong to the separate verification evidence.
- Ten manual-review keyword findings and twelve disposition-class waivers reflect broad source inventory, evidence and artifact-contract descriptions. They are not independent review approval. The complete inventory is deliberately distinguished from the smaller executable review rule.

## Manual-review dispositions

The author's disposition is to retain the administrative/definition role **with an explicit scope limit**, not to erase requirements. Source file 2 (use-case overview), source file 3 (source guide), source file 4 (manifest) and source file 5 (fixture contract) contain clinical language, so their operative population, receptor/stage, unknown and selection requirements also appear in specific linked or openly unlinked items. The broad inventory entries do not certify complete implementation.

Source file 6 through source file 9 contain the supplied professional/staging/patient-education excerpts. Their evidence role and restrictions are explicit in the supplied source guide: these are not additional treatment-selection algorithms for this baseline. The TNBC receptor definition is separately linked. The update-population and stage-domain definitions preserve distinctions; neither is permission to expand the review trigger. Packet identity and the general participant README remain source/process obligations, not patient conditions.

No ignored ranges or authored support waivers were introduced. The open input-selection item and unverified cases remain visible. This is proportional connectathon traceability, not clinical production approval or a claim that every source requirement is fulfilled. If the model/CEL changes after the recorded hashes, this snapshot must be revalidated before a current claim.

## Final stable-model refresh

The final provenance validation was rerun against CRL SHA-256 `687e613f717d6a11c80b92158b36498d4d7ac5507741471b754aa4a6959a5464` and CEL SHA-256 `988100c4727c48e4c0ebd976cf54437eccb8f4f1543ae14c8c3be8721ca80e38`. The complete current result and refreshed carrier/source hashes are in the linked receipts. Findings remain 14 errors, 22 manual reviews and 0 warnings; this is not a provenance pass.

The current native evidence reports **91/104 typed expression assertions and 12/13 activity/error checks**. Eleven cases pass every named-expression assertion. The other two expose real unmet requirements: HER2-equivocal raises an uninterpretable finite-domain error for all eight named exports, and diagnosis-absent returns five tumor-specific values instead of null because source retrieval is not constrained to an indexed cancer. The receptor source item's links identify the implementation location but do not mark the equivocal requirement fulfilled; its rationale explicitly records that failure. The indexed-selection requirement remains visibly unlinked. Do not confuse these native failures with the separate CRE/cockpit errors.

CEL external coded Observation facts currently emit their coded answers as valueString, an installed emitter limitation recorded by the author. Original supplied diagnostic bundles remain the authoritative native test inputs; their values and oracles were not changed to make the model pass. See `../../tests/verification/native-current/verification.json` and the implementation-gap evidence. Packaging success does not resolve these findings.
