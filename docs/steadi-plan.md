# STEADI implementation plan

Status: direct-authoring plan accepted; implementation and verification in progress.
Updated: 2026-09-19.
Upstream revision: 5034ccd6bc5971aa7e366b6b0df0b23caffe4f46.
Public repository: https://github.com/alphora/hl7-agentic-knowledge-connectathon

## Goal and boundaries

Implement the supplied STEADI challenge, with every required artifact and executable behavior traceable to its supplied inputs and acceptance contract. The operator explicitly limits implementation to the requirements. Do not crawl additional or referenced clinical documents to enlarge scope. Applicable terminology lookup is authorized. Consult technical specifications only to implement required resource/operation contracts, not to add deliverables or clinical obligations.

Sources: source manifest, the six raw snapshots, MARP overview and rendered PDF, synthetic bundles and shared Questionnaire.
Acceptance requirements: STEADI overview and fixture contract, machine-readable assertions/extraction expectations, and root participant/interoperability requirements.
A research source informs the required evidence summary; its presence does not make all interventions in that source executable requirements.

Use customer-neutral KE method 0.1.1. No IEHP/HCSC customer rules, canonical namespaces, PA outcomes, policy content, or lifecycle state belong in this project. No KELP project binding has been supplied for this new repository.

Framework: An AI-assisted clinical knowledge engineering framework that turns source guidance into executable FHIR content, with traceable reasoning, reproducible verification, and human review.

## Phase 1 - Requirements, source model and evidence design

Complete the read ledger and requirements-to-artifact/check matrix. Verify upstream blob hashes and six source-manifest SHA-256 values. Distinguish source statements from track operational choices; retain stable locators and source rights. Keep downloaded snapshots in an ignored cache rather than silently redistributing third-party material.

### Evidence and EvidenceVariable workstream

1. Extract only the evidence needed to explain the two required guidance paths: exercise and individualized consideration of multifactorial intervention. Prepare a reviewable evidence table from the supplied USPSTF recommendation, supplied evidence-update snapshot and supplied systematic review. Record population, intervention, comparator, outcome, reported benefit, harms, certainty/limitations, source date and exact locator. Preserve differing populations, comparators, outcome definitions and follow-up periods. Do not pool findings, calculate new effect estimates, infer missing information or treat statistical nonsignificance as proof of no effect. The source snapshots' boundaries matter: an abstract plus table of contents is not permission to retrieve the linked book.
2. Propose one Evidence record per distinct source-supported evidence question needed for the two guidance paths. Two guidance topics are the starting point, not an instruction to collapse incompatible studies into exactly two resources. Reuse EvidenceVariable definitions only when their meaning is identical. Each accepted record must support an actual required guidance statement; avoid an exhaustive research catalog.
3. Define EvidenceVariables for the referenced research population, intervention/exposure, relevant comparison and outcome. Separately identify the track screening population and its operational eligibility. Do not rewrite a study's eligibility as age 65+ just because that is the track's target population. The link from evidence to guideline applicability must explain the population correspondence.
4. Use FHIR R4 4.0.1 fields. Evidence.exposureBackground references the population; exposureVariant and outcome reference their variables. EvidenceVariable.characteristic requires a definition[x], not just a label. Select definitionCodeableConcept with verified applicable terminology (and faithful text) for descriptive definitions, or a supported expression when a genuinely executable definition is required. A descriptive evidence population is not proof of executable eligibility.
For each Evidence record, record the intervention/exposure and comparator roles separately in its narrative and evidence table, naming their referenced EvidenceVariable identities and the exact outcome. R4 has no dedicated comparator element: exposureVariant may reference the compared exposure definitions, but the relationship and direction must be explicit in description/note. Do not imply that array order defines roles or that an effect applies to every listed outcome. Split records where necessary to keep an estimate and its population/comparison/outcome unambiguous.
5. R4 Evidence lacks the later-release statistic structure. Preserve required reported findings, uncertainty and source locators in its narrative/description/note and relatedArtifact, with the reviewable evidence table as supporting detail. Do not put R5 fields into R4 or add a statistical resource family/custom extension merely to recreate a newer model. Do not claim narrative estimates are computable statistics.
6. Preserve USPSTF grade B exercise and grade C individualized multifactorial guidance as recommendation strength, distinct from effect sizes and evidence certainty. Link the guidance artifacts to their supporting Evidence through supported related-artifact associations. Keep research exposure definitions distinct from recommended actions; never derive an automatic order from an EvidenceVariable.
7. Ask CRL which current 6.4.0 path supports these artifacts and links. If they are outside CRL emission, use separately authored standard R4 companions only after verifying the composition boundary. Do not duplicate executable clinical logic, hand-edit generated artifacts, or assume lack of a kit search match proves lack of capability.
8. Independent evidence review checks the supplied source passages against every statement and variable, population correspondence, recommendation strength, uncertainty and reference direction. Validation checks required fields, R4-only shapes and resolvable references. Include these resources in both FHIR round-trip tests.

Technical schema references, accessed solely for the required R4 mapping:
- https://hl7.org/fhir/R4/evidence.html
- https://hl7.org/fhir/R4/evidencevariable.html

These resources describe evidence and its subjects. They do not replace the eight required CQL expressions, create patient observations, or establish screening performance statistics not supplied by the source.

### Decisions to settle before artifact generation

- Operator-approved canonical base (2026-09-19): https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir. Preserve upstream fixture identities; any allowed Questionnaire mapping must be explicit.
- Direct CQL/FHIR implementation is authorized; it remains explicitly distinguished from CRL generation.
- Fixture context omits explicit community residence/hospice data. Record the track-scoped context assumptions explicitly; an AMB encounter alone does not prove those facts for general clinical use.
- Document operational choices for age anchor, encounter/period linkage and selection among multiple responses, preserving all supplied expectations. Do not mix answers across separate response instances.

### Accepted execution contract

The operator authorized direct implementation of missing capabilities. Author the assessment and guidance directly in standard CQL/FHIR, alongside the already authorized Measure/Evidence companions. This supersedes the earlier CRL-generated-only path for this challenge. No CRL tools-repository changes or additional clinical sources are included.

Both execution implementations receive the original synthetic patient Bundle and equivalent explicit period/selection/context parameters. CQL reads one coherent selected response. Native SDC extraction is independently invoked on that same response and the unchanged Questionnaire; documented adapter metadata corrections retain raw engine evidence. The outputs are explicitly direct-authored/adapter results, not CRL emission.

## Phase 2 - Required implementation only

Author the evidence summary, recommendation decision table, assessment/measure/terminology definitions and corresponding R4 resources. Use the shared three-question Questionnaire, required linkIds/LOINC bindings and extraction semantics. Pin dependencies and expose the exact eight expression names. Use standard CQL and FHIR with explicit provenance to the supplied requirements.

| Required output | Planned acceptance evidence |
| --- | --- |
| Evidence, EvidenceVariable | Source-linked population/intervention/outcome definitions; benefits/harms/uncertainty read-back; R4 validation and resolved associations |
| Questionnaire and reusable logic | Three required Boolean questions; original linkIds/codes; completed-response gating; explicit canonical mapping if used |
| SDC extraction | Run an actual extraction path; compare normalized observed resources, copied fields and provenance with supplied expected sets |
| PlanDefinition, ActivityDefinition, Library | Exercise guidance and individualized multifactorial consideration; no diagnosis, automatic order or extra treatment selection |
| Measure and Library | Track-authored screening completion, distinct from CMS139FHIR; initial population, denominator and numerator aligned with fixtures |
| ValueSet, ImplementationGuide | Verified applicable terminology, stable identity and exact dependencies |
| CQL source and ELM JSON | Portable CQL subset, translation diagnostics and all eight named expressions |
| R4 NPM package | Reproducible package, complete artifact inventory, exact dependency versions and validation |

Completed screen means completed response status plus all three usable Boolean answers. Partial affirmative remains unknown for risk and dependent guidance. Missing/partial screen gives false completion numerator. Extraction of completed younger-patient responses remains independent of screening eligibility.

## Phase 3 - Verification, review and public delivery

Run all six immutable shared fixtures: 48 named-expression assertions, four positive extraction cases and two non-invocation cases. Do not substitute expected JSON for actual extraction output. Add narrowly relevant edge cases for missing/false answers, response changes, coherent response selection and population boundaries without changing the fixture oracle.

Validate our generated resources and execute our artifact pipeline first. Coordinate with another participant to execute the same CQL and compare Boolean/null results, and to complete the second FHIR implementation storage/readback check. The challenge requires combined evidence from two implementations, not two implementations operated by this participant. Cross-participant results remain pending until actually received and compared. Record exact versions, actual commands, diagnostics and observed results. Failed/unavailable checks remain visible; compilation, upload, a mock engine or two wrappers around one implementation do not establish interoperability.

Review the source-to-evidence-to-guidance/measure chain and the actual delivered artifacts. Record reviewer findings and lead dispositions; human clinical acceptance remains separate. Record elapsed authoring and human review time, revision cycles, blockers and repeatability. Without a comparable conventional baseline, report descriptive effort only.

After scoped code/artifact review, commit and push the authorized public project with a strict file allowlist excluding private workspace material, credentials and cached third-party snapshots. Publish reproducible instructions, verification evidence and remaining limitations. The public repository contains the initial reviewed Measure/Evidence delivery; assessment and package changes receive their own code review.

## Review and verification status

The direct-implementation plan review converged after two important findings were accepted: keep risk independent of population eligibility, and distinguish exact selected-encounter assessment from period-wide Measure membership. Controls cover both. Native execution, code review and package validation are separate gates.

The external review arm was unavailable after two timeouts. Native review is recorded separately from lead execution. Human clinical acceptance and cross-participant storage/retrieval are not inferred from tests or review.

Current results and remaining work are recorded in `task-state.json` and the verification reports. The package uses exact R4 4.0.1, SDC 4.0.0 and CPG 2.0.0 dependency declarations. These do not establish transitive profile/terminology validation by themselves.
