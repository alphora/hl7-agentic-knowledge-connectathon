# STEADI implementation plan

Status: native plan review completed with 2 important findings accepted; refinements and preflight qualification in progress. No implementation acceptance claimed.
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
- Exact supported CRL/CQL/companion boundary: question sent to CRL, answer pending.
- Fixture context omits explicit community residence/hospice data. Record the track-scoped context assumptions explicitly; an AMB encounter alone does not prove those facts for general clinical use.
- Document operational choices for age anchor, encounter/period linkage and selection among multiple responses, preserving all supplied expectations. Do not mix answers across separate response instances.

### Execution contract and bounded preflight

The proposed CQL input is the original synthetic patient Bundle, including QuestionnaireResponses, together with the explicit measurement period and evaluation date. Both independent engines receive equivalent input and parameter values. CQL completeness/risk reads one coherent response instance; it does not combine answers across responses. Extraction is a separate required tested operation against the same QuestionnaireResponse and supplied Questionnaire. Actual extraction output is compared with the expected resources; it is not required as a substitute CQL input merely because extraction is part of the challenge.

Use CRL-generated CQL/ELM and FHIR definitions with our verified native $apply runtime as the implementation path. Qualify the needed translator/model/helper and extraction interfaces against the supplied contract. Do not replace this path with hand-authored clinical CQL merely to satisfy fixtures. Independent CQL and FHIR implementations may be supplied by collaborating participants; operating a second local stack is not an implementation prerequisite. Exchange the same artifacts, original fixtures, parameters and typed expected results, then retain observed versions and results. Resolve concrete fixture-integration gaps without silently changing inputs or generated outputs.

## Phase 2 - Required implementation only

Author the evidence summary, recommendation decision table, assessment/measure/terminology definitions and corresponding R4 resources. Use the shared three-question Questionnaire, required linkIds/LOINC bindings and extraction semantics. Pin dependencies and expose the exact eight expression names. Use current supported CRL forms where applicable; resolve the expression/export boundary before encoding.

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

After scoped code/artifact review, commit and push the authorized public project with a strict file allowlist excluding private workspace material, credentials and cached third-party snapshots. Publish reproducible instructions, verification evidence and remaining limitations. The public repository already exists; no implementation has yet been committed.

## Review and capability status

Native impl plan review: 0 critical, 2 important, 1 nit; all accepted. Comparator representation and preflight/input contract added; hash status reconciled. Candidate preflight remains to be executed. Review was against a byte-identical bounded packet, not raw clinical sources or execution. No clinical fidelity approval inferred.
External panel arm: unavailable in this session after two earlier timeouts; do not imply a completed external review.
CRL capability question: 01M2XKZB50EX9GYFKCFMG4EYXQ, pending.
Evidence-specific follow-up: 01M2XMJSEENDFE9GTBF54617DT, accepted but CRL not armed at send time; answer pending.

## Operator clarifications (2026-09-19)

Prioritize CRL-generated CQL/ELM and FHIR artifacts and their native $apply behavior. Cross-implementation checks can be coordinated among participants. The direct CQL prototype passed 48 supplied assertions on cql-execution, but is not the selected deliverable or proof of CRL behavior. A Boolean Observation coded-source compatibility probe failed in CRL6.4.0; the exact diagnostic and shared-Questionnaire integration question were sent to CRL in exchange 01M2XPMRBDZ2CWHQNGHRMHCXW8. Local selected-answer experiments must be labeled separately from shared-fixture acceptance.

Measure boundary confirmed by operator: author standard FHIR Measure separately, with its population CQL Library, and use Measure/$evaluate-measure or the runtime measure command. Assessment and guidance remain CRL-generated and use $apply. The measure companion contains period/encounter/completion counting, not a replacement guidance implementation.
