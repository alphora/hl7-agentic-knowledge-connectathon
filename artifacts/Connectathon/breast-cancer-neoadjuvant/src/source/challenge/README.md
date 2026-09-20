# AI-Assisted Development of Clinical Reasoning Knowledge

This repository contains shared material for a proposed HL7 FHIR Connectathon
track. The track tests whether AI-assisted authoring can transform unstructured
clinical sources into valid, clinically coherent, interoperable knowledge
artifacts.

The repository is implementation-neutral. Participants may use any
AI-assisted or conventional development approach.

## Use cases

Each use case lives under `use-cases/` with its own overview, source manifest,
clinical scope, synthetic patient bundles, and expected-result contract.

| Use case | Clinical focus | Participant inputs |
| --- | --- | --- |
| [Older-adult fall risk (STEADI)](use-cases/steadi/README.md) | Three-question screening, prevention guidance, and screening completion | [Sources](use-cases/steadi/sources/manifest.yaml), [fixtures](use-cases/steadi/test-bundles/README.md), [slides](use-cases/steadi/slides/connectathon-track-overview.md) |
| [Breast cancer](use-cases/breast-cancer/README.md) | Neoadjuvant TNBC guidance for oncology review | [Sources](use-cases/breast-cancer/sources/README.md), [fixtures](use-cases/breast-cancer/test-bundles/README.md), [validation](use-cases/breast-cancer/validation/README.md) |

```text
use-cases/
├── steadi/
│   ├── README.md
│   ├── sources/
│   ├── test-bundles/
│   └── slides/
└── breast-cancer/
    ├── README.md
    ├── sources/
    ├── test-bundles/
    ├── scripts/
    └── validation/
```

Source-manifest `local_path` values are relative to the repository root.
Fixture-manifest paths are relative to the directory containing that manifest.
FHIR canonical URLs identify artifacts independently of their filesystem paths.

## Track question

Can AI-assisted development reduce authoring and review effort, support a
repeatable process across artifact types, and preserve the quality required for
clinical reasoning content?

Record process evidence and artifact evidence separately:

- **Process:** elapsed authoring time, human review time, revision cycles,
  blocking issues, and repeatability.
- **Artifacts:** source traceability, FHIR conformance, CQL translation and
  execution, clinical coherence, and cross-implementation agreement.

## Participant task

Start with a use case's source corpus and shared test bundles. Produce
source-linked evidence, structured recommendations, terminology bindings,
FHIR knowledge artifacts, CQL source, and ELM JSON as specified by that case.
Assessment and measure requirements are case-specific: STEADI includes SDC
Questionnaire extraction and a screening-completion measure; breast cancer
uses diagnostic Observations and an oncology-review applicability rule.

Record tools, versions, instructions, human decisions, and unresolved issues.
Preserve source locators and distinguish source statements from track-authored
operational choices. Record exact package dependencies for distribution.

FHIR R4 does not define `Citation`; an R4 submission should use available
provenance and related-artifact elements. Identify any R5 variant separately.

## Interoperability test

The baseline is FHIR R4 4.0.1, ELM JSON, and a conservative CQL subset suitable
for multiple CQL 1.5-era implementations. Participants:

1. validate the generated FHIR resources and package;
2. store and retrieve the knowledge artifacts from independent FHIR servers;
3. translate the same CQL and record diagnostics;
4. execute every shared patient bundle for their selected use case;
5. compare Boolean and null semantics against the assertions; and
6. record exact implementation, dependency, terminology, and artifact versions.

Baseline evidence requires agreement from at least two independent CQL
implementations and round-trip testing in at least two FHIR implementations.
Compilation or upload alone is not a passing result.

## Review boundaries

FHIR validation and CQL compilation are necessary, but they are not clinical
approval. Source rights and redistribution terms are recorded in each source
manifest and the repository [notices](NOTICE.md).

All patient data is synthetic. The material is for Connectathon testing and
education, not clinical use.
