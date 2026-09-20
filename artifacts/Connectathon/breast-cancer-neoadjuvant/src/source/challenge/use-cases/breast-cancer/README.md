# Breast cancer: neoadjuvant TNBC review

This case extends the Connectathon's STEADI pattern with a breast cancer
example: a traceable source corpus, synthetic FHIR R4 patient bundles, and
engine-neutral expected results. Participants turn the source material into
reviewable evidence, structured recommendations, and executable knowledge.

The case focuses on triple-negative breast cancer (TNBC) neoadjuvant guidance.
This package supplies participant inputs. Generated CQL, ELM, and treatment
pathways are participant deliverables.

## Clinical question

For an adult undergoing pretreatment review of an active, confirmed invasive
breast cancer, does the documented nonmetastatic disease, receptor status, and
clinical tumor/node category match the TNBC neoadjuvant guidance under review?

The baseline tests the population described by ASCO's 2021 recommendations
3.1 and 3.2: TNBC with clinically positive nodes or a clinical tumor category
of T1c or higher, with small node-negative tumors as negative controls.
The asserted result is **applicability of guidance for oncology review**.
It does not determine a patient's fitness for chemotherapy or authorize a
medication order. A false result means this particular rule does not apply;
it does not mean that no cancer treatment is indicated.

## Start here

1. Read the [source guide](sources/README.md) and
   [manifest](sources/manifest.yaml). Distinguish guideline recommendations,
   professional evidence summaries, and patient education.
2. Review the [patient fixture contract](test-bundles/README.md), including
   clinical staging, tumor linkage, and Boolean/null semantics.
3. Generate structured evidence and recommendation artifacts with source IDs,
   versions, and section locators.
4. Formalize the agreed rule in FHIR R4 and CQL, then compare execution with
   every shared assertion.

The corpus includes NCI source text extracted from online material, with
retrieval dates and checksums. Extraction and exclusions are documented;
these files are not untouched HTML snapshots or maintained NCI publications.
ASCO publications remain linked references under their original rights.

## Guidance and evidence

| Source | Role in this exercise |
| --- | --- |
| [ASCO neoadjuvant guideline, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8274745/) | Baseline population and TNBC recommendation; use recommendations 1.2, 3.1, and 3.2 as stable locators |
| [ASCO rapid recommendation update, 2022](https://pubmed.ncbi.nlm.nih.gov/35417251/) | Required update review for immunotherapy; prevents carrying forward the 2021 statement on insufficient evidence as current guidance |
| [NCI professional breast cancer treatment summary](https://www.cancer.gov/types/breast/hp/breast-treatment-pdq) | Evidence context, including neoadjuvant therapy and KEYNOTE-522; this is an evidence summary, not an ASCO guideline |
| [NCI TNM staging explanation](https://www.cancer.gov/types/breast/stages/tnm-staging-system) | Tumor-size boundaries and staging context; its node section describes pathological staging and must not be used to derive clinical node categories |
| [NCI chemotherapy](https://www.cancer.gov/types/breast/treatment/chemotherapy) and [immunotherapy](https://www.cancer.gov/types/breast/treatment/immunotherapy) | Patient-facing explanation of treatment timing and discussion topics |

The 2022 update supports pembrolizumab with neoadjuvant chemotherapy followed
by adjuvant pembrolizumab in a specified high-risk early-stage TNBC population.
That population is not identical to everyone matching the baseline chemotherapy
review rule. Immunotherapy eligibility, contraindications, dosing, sequencing,
and treatment orders are outside the shared execution contract. Participants
must record how the update affects any broader pathway they choose to author.
This is a dated source set, not an exhaustive review of all guidance available
in 2026.

## Source statements and track choices

The source supports using tumor features and receptors to guide neoadjuvant
decisions. The following are track-authored operational choices:

- Require an explicit active, confirmed invasive breast cancer and a documented
  nonmetastatic assessment. Absence of metastatic disease in a record is not
  evidence of cM0.
- Use explicit clinical T and N categories. Keep a tumor size measurement for
  consistency checks; a size alone does not establish stage. A 10 mm tumor is
  at the T1b upper boundary, not T1c.
- Evaluate receptor and staging Observations for the same tumor and evaluation
  context. Receptors from an unrelated tumor must not determine this subtype.
- Treat unresolved or absent receptor/staging data as unknown. Use three-valued
  logic so a known positive route can resolve an OR, while missing information
  cannot silently become a negative result.
- Use a small, explicit local staging vocabulary for the fixture exchange
  contract. It is not an AJCC terminology distribution or a claim of mCODE
  profile conformance.

All baseline patients are adults in a pretreatment context. Age eligibility,
prior systemic therapy, multiple simultaneous tumors, and longitudinal result
reconciliation require additional cases before expanding the contract.

## Required expressions

Every implementation must return the typed values specified in the case files
for these expressions:

- `Has Active Confirmed Invasive Breast Cancer`
- `Has Nonmetastatic Disease`
- `In Neoadjuvant Review Population`
- `Is Triple Negative`
- `Has Clinically Positive Nodes`
- `Has Clinical T1c Or Higher`
- `Meets Tumor Or Node Criterion`
- `Neoadjuvant TNBC Guidance Applicable`

JSON `null` means an unknown Boolean. It is distinct from `false`, an omitted
expression, or an engine failure. The detailed data-selection rules and case
matrix are in the [fixture README](test-bundles/README.md).

## Participant deliverables

| Stage | Expected output |
| --- | --- |
| Evidence | Source-linked evidence summary; FHIR `Evidence`/`EvidenceVariable` where appropriate, preserving population, intervention, comparator, outcome, and limitations |
| Structured recommendation | Decision table and care pathway separating sourced recommendations from operational choices and the 2022 update |
| Assessment | Explicit receptor/staging data requirements and missing-data handling; a Questionnaire may be an additional reviewed artifact, but diagnostic inputs are not survey answers |
| Computable guidance | `PlanDefinition`, review-oriented `ActivityDefinition`, `Library`, CQL source, and ELM JSON |
| Terminology and distribution | Versioned `ValueSet`/`CodeSystem` bindings and a FHIR R4 package with exact dependencies |
| Verification | FHIR validation, CQL translation/execution results, source traceability, and a clinical review record |

A track-authored process measure of assessment completeness is an optional
extension. It needs its own population, period, numerator, denominator, and
fixtures; there is no asserted measure or claim of equivalence to an oncology
quality measure in this baseline. FHIR R4 has no `Citation` resource; use R4
provenance and related-artifact elements, or identify an R5 variant separately.

As in STEADI, interoperability evidence requires agreement from at least two
independent CQL implementations and round-trip testing in two FHIR
implementations. Record exact tool, terminology, dependency, and artifact
versions, along with authoring time, review effort, and revisions. A fixture
integrity check or successful FHIR validation alone does not demonstrate CQL
execution or clinical approval.

All patients are synthetic. This material is for Connectathon testing and
education; derived clinical content requires independent clinical review.
