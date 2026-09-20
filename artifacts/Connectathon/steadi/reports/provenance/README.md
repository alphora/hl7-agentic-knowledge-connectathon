# STEADI source attribution — demo evidence

The installed provenance carrier is `src/provenance/steadi.json` (relative to the artifact root). This reports directory contains the validation evidence, not additional provenance carriers.

## Result

30 source items acknowledge the full canonical source without ignored ranges. All 14 distinct policy-owned CRL leaves/decision rows from the tool scaffold have source attribution. The completed positive-screen path has its own five-row cluster linked to frozen CEL cases `steadi-03` and `steadi-04`; FINAL validation confirms no correspondence finding for those cases. No clinical outcomes were invented for the four no-guidance cases.

The canonical anchor hash remains `sha256:e8fed4e11d4832007937d6ffb78766d8d7bd42c9c4558dde512d12836e21e1d5`. Supported `normalize_provenance` with the canonical anchor established the carrier-relative anchor-self pointer to `../anchor-source/steadi.txt` and returned `fullyNormalized: true`, empty worklist. The existing DOCX-derived sidecar remains the upstream source trail; this task did not rewrite it.

Actual FINAL validation: **pass false; 9 errors, 20 manual-review findings, 5 warnings**. There are no uncovered-span, overreach, referential, text/hash-drift or derivedFrom errors.

## Open source-contract findings

Five missed-decision items represent four distinct boundaries:

1. General community-dwelling/ambulatory and excluded-population filtering is not implemented; supplied synthetic fixture context supplies those conditions. The slide repetition is an additional source item, not another distinct gap.
2. The implementation uses age today rather than encounter-relative age. Supplied fixture agreement does not prove arbitrary retrospective eligibility. The measurement-period statement also belongs to the separate Measure context, whose execution evidence the lead owns.
3. The original source-model record conflated input ingestion with client completion. This interpretation is corrected: CEL inputs are valid setup; the client completes the generated response before extraction. The extraction test records completion explicitly.
4. Extraction invocation is a client workflow responsibility. The new test invokes it for complete responses and does not invoke it for incomplete/absent responses; this is not a requirement for another decision branch.

Additional technical contract limits are explicitly recorded in the definition-item rationales: exact shared linkIds, external question-code bindings, the specific extracted-field differences listed in ../extraction.md. They are not declared implemented by clinical decision links. Manual Measure/Evidence companions, packaging and participant interoperability checks require their own evidence.

## CRE/cockpit evidence is separate

FINAL reports `run-error`/unchecked cockpit correspondence for `steadi-01`, `steadi-02`, `steadi-05` and `steadi-06`. These are the cases deliberately lacking invented action or pause assertions. This result is a CRE/cockpit checking limitation in this invocation, **not proof that native CQL or $apply failed**. Separate retained evidence verifies successful native 48/48 named-expression expectations, exact guidance sets, regenerated Q/QR and Measure results; those independently maintained results are not contradicted or replaced by this tool finding.

The disposition-path scaffold was retried after the lead corrected reserved `k1`–`k6` IDs to legal `steadi-01`–`steadi-06`. The retry still produced a deferred diagnostic and coverage-only scaffold. Final validation nevertheless grounded both positive cases; their actual five-row paths were linked explicitly and revalidated. Prior invalid-ID output is not the basis of the final findings.

## Manual-review dispositions

The 20 routine `waiver-disposition-class` findings are source inventory classifications, not claims that requirements can be ignored. Each item has a concrete rationale in the carrier. The author's disposition is **accept the role with the stated evidence boundary**:

- Source identity, fixture introduction/history, presentation/process instructions, review boundaries and interoperability reporting are administrative obligations, not patient decision branches.
- Named outputs, artifact/terminology/packaging definitions, case oracles and extraction transport are definitions/contracts, with implementation or execution evidence owned separately.
- Guidance-scope wording restricts claims to guidance rather than diagnosis/orders; the same full recommendation paragraph is directly linked to both actual activity rows.
- QR identities, codes and extraction definitions stay explicitly open where unsupported. Their classification does not waive them, and no generic authored-support escape or ignored range was added.

The five soft keyword warnings arise from eligibility/criteria words in case tables, use-case questions and process/artifact descriptions. Their underlying clinical requirements remain in explicit criterion items. This is author assessment, not independent review or human acceptance.

## Installed validation

The carrier was normalized and FINAL-validated against the actual artifact paths after installation. Normalization returned `fullyNormalized: true` with no changes or worklist. FINAL findings remain the explicit findings above; saving through KELP does not turn them into a passing validation.

This is demo provenance with explicit gaps, not a full-fidelity or production acceptance claim. Source acknowledgement alone is not complete implementation.

## Interpretation correction after the recorded FINAL run

The saved validator output is historical execution evidence, not a current independent adjudication of the source interpretation above. The original-QR input-ingestion caveat is withdrawn. The source and provenance carrier were not rewritten by this focused output test; the former source-gap classifications for completion/extraction must be read with this correction.
