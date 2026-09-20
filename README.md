# Alphora STEADI Connectathon implementation

An AI-assisted clinical knowledge engineering framework that turns source guidance into executable FHIR content, with traceable reasoning, reproducible verification, and human review.

This implements the supplied STEADI challenge at upstream revision `5034ccd6bc5971aa7e366b6b0df0b23caffe4f46`. All patient data are synthetic; this is not clinically approved content.

The operator authorized direct implementation for capabilities not available through the CRL authoring path. This submission therefore contains explicitly authored CQL/FHIR, with a small adapter over the pinned native runtime. These artifacts are not represented as CRL-generated.

- `Steadi.cql` exposes the eight required expressions, preserving Boolean and unknown results.
- `PlanDefinition` and two `ActivityDefinition` resources produce evidence-linked exercise and individualized multifactorial guidance through native `$apply` processing.
- `SteadiMeasure.cql` and `Measure` count screening completion, evaluated through the native measure operation.
- Two `Evidence` and seven `EvidenceVariable` resources describe the supplied research findings and population definitions.
- The shared Questionnaire is byte-identical to the supplied version. Native SDC extraction is tested with an explicit metadata adapter; raw and adapted outputs are retained.
- An `ImplementationGuide`, terminology `ValueSet`, deterministic FHIR NPM package, and PUT transaction Bundle complete the artifact inventory.

[Download the FHIR package](dist/org.alphora.steadi-0.1.0.tgz) or [knowledge transaction Bundle](dist/knowledge-transaction.json). The Bundle contains knowledge definitions, not patient test data.

See [implementation plan](docs/steadi-plan.md), [assessment and measure contract](docs/assessment-and-measure.md), [runtime adapter](docs/native-adapter.md), [evidence summary](docs/evidence-summary.md), and [task state](docs/task-state.json).

Canonical base: `https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir`.

## Reproduce

Use Node 22+, Python 3.11+, Java/Javac 23 and the pinned native engine in [toolchain.json](docs/toolchain.json). Run from this repository:

```powershell
python tools/bootstrap.py --engine-jar <path-to-pinned-jar>
npm ci --ignore-scripts
python -m pip install --target .cache/python -r requirements-dev.txt
node tools/build-measure.mjs
node tools/build-assessment.mjs
python tools/build-evidence.py
python tools/build-guidance.py
python tools/build-package.py
python tools/test-verification-guards.py
python tools/verify-measure-native.py --jar <path-to-pinned-jar>
python tools/verify-assessment-native.py --jar <path-to-pinned-jar>
python tools/validate-companions.py
```

The scripts verify original fixture hashes. Assessment runs compare all 48 supplied assertions; native runs also check extraction and guidance. Additional controls test answer/change/clear, response isolation, encounter selection, age boundaries, and malformed or mismatched input. The native `measure` command corresponds to FHIR `Measure/$evaluate-measure`.

The bootstrap retrieves only pinned supplied inputs and technical dependencies. The local Windows build is exercised; clean-cache cross-platform reproduction remains unverified. JSON-schema checks establish R4 JSON structure, not complete profile/terminology/invariant validation. Cross-participant FHIR storage/retrieval checks and human clinical review remain pending. Independent participants may supply the additional interoperability evidence; two local server installations are not a prerequisite.

The shared Questionnaire is reproduced under the upstream [MIT license](licenses/upstream-MIT.txt); its metadata remain intact. Cached third-party clinical source snapshots and private KE workspace material are not distributed in this package.
