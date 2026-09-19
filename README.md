# Alphora STEADI Connectathon implementation

An AI-assisted clinical knowledge engineering framework that turns source guidance into executable FHIR content, with traceable reasoning, reproducible verification, and human review.

**Work in progress.** This implements the supplied STEADI challenge at pinned upstream revision `5034ccd6bc5971aa7e366b6b0df0b23caffe4f46`. All patient data are synthetic; this is not clinically approved content.

- Assessment/guidance will use CRL-generated CQL and FHIR with native `$apply` Questionnaire/QuestionnaireResponse output. A bounded local-answer probe works; shared-fixture integration is pending.
- A separately authored FHIR Measure and CQL library implement screening completion. CRL does not currently author Measures.
- FHIR R4 Evidence/EvidenceVariable companions preserve source-specific populations, comparisons, outcomes and limitations.
- The shared Questionnaire is preserved unchanged.
- Independent implementations may be provided by collaborating participants; cross-participant evidence remains pending.

The CRL core compatibility probe produces populated Q/QR pairs. Integration with the supplied fixed linkIds/LOINC-coded responses remains unresolved with the CRL team. Do not interpret the probe or the earlier direct-CQL prototype as full challenge acceptance.

See [plan](docs/steadi-plan.md), [assessment and measure](docs/assessment-and-measure.md), [evidence summary](docs/evidence-summary.md), and [task state](docs/task-state.json).

Canonical base: `https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir`.

Build the Measure and evidence companions with Node 22+, Python 3.11+ and the pinned native engine identified in `docs/toolchain.json`:

```powershell
python tools/bootstrap.py --engine-jar <path-to-pinned-jar>
npm ci --ignore-scripts
python -m pip install --target .cache/python -r requirements-dev.txt
node tools/build-measure.mjs
python tools/build-evidence.py
python tools/test-verification-guards.py
python tools/verify-measure-native.py --jar <path-to-pinned-jar>
python tools/validate-companions.py
```

The bootstrap retrieves only the pinned supplied inputs and technical dependencies, verifies their hashes, and extracts model files from the verified engine. It has passed with the existing local cache; a clean-cache cross-platform run has not been verified. The native `measure` command evaluates the Measure and emits MeasureReports; its corresponding FHIR operation is `$evaluate-measure`.

JSON-schema checks establish R4 JSON structure only, not profile, terminology, clinical or full challenge acceptance. The final distribution package remains pending. Cached third-party source snapshots and private KE workspace material will not be published as project artifacts.

The shared Questionnaire is reproduced from the pinned upstream challenge under its [MIT license](licenses/upstream-MIT.txt); its original metadata and copyright are retained. Clinical source snapshots are fetched for local inspection and are not redistributed here.
