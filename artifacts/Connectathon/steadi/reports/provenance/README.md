# STEADI provenance: current demo evidence

Updated 2026-09-20 for the final decision: age eligibility, Completed Three Question Screen, direct OR of the three answers, then both positive guidance activities or the completed-negative Nothing Recommended marker.

The authoritative carrier is `src/provenance/steadi.json`. All 30 original source items, their exact text and byte ranges, the anchor identity and existing source-gap classifications were preserved. Stale sequential-presence decision addresses were remapped to the current tree. All 17 distinct current policy-owned leaves/decision rows have explicit links. No source documents, CRL, CEL or tests were changed by this provenance update.

The positive five-row path is linked to `steadi-03` and `steadi-04`. The completed-negative path is linked to `steadi-02`. FINAL validation reports no correspondence findings for those three cases.

The one added authored item records the operator-approved Nothing Recommended display marker. Its support scope contains only that activity, its otherwise branch and its action row. It communicates absence of the positive-screen recommendations after a completed all-No screen; it is not a new clinical recommendation, a missing-input result or a claim that the source explicitly requires that label. Its author disposition is accept as scoped implementation wording. It does not change the Boolean assessment or Measure oracle.

## Current validation

`validation-final.json` is the complete current MCP result. `current-validation-receipt.json` binds the actual arguments and source/model/CEL/carrier hashes. `scaffold-current-receipt.json` is the fresh comparison scaffold receipt, not another provenance carrier; its inline anchor pointer was never installed.

**FINAL pass: false. 8 errors, 20 manual-review findings, 5 warnings.** There are no referential, anchor/text/hash drift, derivedFrom, overreach or uncovered-span errors.

The eight errors are five retained source items without decision links and three unchecked CRE/cockpit cases. No findings were removed by changing their severity or adding ignored ranges.

## Retained source findings and interpretation limits

- `scope-exclusions-not-general-filter` and its duplicate `slide-clinical-scope`: general community-dwelling/ambulatory and excluded-population filters are not encoded; the supplied synthetic context provides these conditions.
- `measurement-and-encounter-time`: the old carrier classified this as a missing decision link. The operator subsequently rejected age-today versus encounter-age as a demonstrated challenge difference. This narrow node-remapping update retains the source item and finding, rather than presenting that historical interpretation as a newly established requirement.
- `completed-qr-status` and `no-incomplete-extraction`: the old carrier treated input QR status/ingestion as missing decision behavior. That interpretation was corrected: input CEL observations are legitimate setup; completion and extraction concern the generated output QR/client workflow. The extraction test completes responses and does not invoke extraction on incomplete/absent responses. These retained validator classifications are not proof of a current clinical decision defect, nor a reason to add clinical branches.

The externally specified question/linkId and extracted-field differences remain separate, measured contract issues. See `../extraction.md` and the current main report. Source acknowledgement and a clinical decision link do not establish those producer capabilities. Nothing here reinstates the withdrawn original-QR input requirement or a requirement to operate two FHIR servers.

## Cases and manual review

Correspondence remains unchecked with run-error for `steadi-01` (younger), `steadi-05` (incomplete) and `steadi-06` (no response). They deliberately have no invented activity or pause oracle. The completed-negative case now has its approved marker and a matching path, reducing the prior four unchecked cases to three. CRE/cockpit findings do not establish a native CQL/$apply failure. Native behavior, named-expression expectations, extraction and Measure results remain separate evidence owned by their actual verification records.

The 20 routine disposition-class manual reviews retain their prior author assessment: administrative source/process material and artifact/transport definitions are acknowledged without turning them into patient decision branches. Their precise rationale remains in each carrier item; routine priority is not an independent-review pass. The five soft keyword warnings likewise remain visible. No additional independent panel or human medical acceptance is claimed.

The anchor hash remains `sha256:e8fed4e11d4832007937d6ffb78766d8d7bd42c9c4558dde512d12836e21e1d5`, with the previously normalized carrier-relative anchor-self pointer `../anchor-source/steadi.txt`. Neither that pointer nor its DOCX-derived sidecar was changed. This is demo provenance with explicit limitations, not full clinical or production acceptance.
