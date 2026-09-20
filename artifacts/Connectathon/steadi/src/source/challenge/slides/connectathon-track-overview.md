---
marp: true
theme: connectathon
size: 16:9
paginate: true
footer: HL7 FHIR Connectathon 43 · proposed track · draft 2026-08-26
title: AI-Assisted Development of Clinical Reasoning Knowledge
description: Proposed HL7 FHIR Connectathon track for evaluating AI-assisted development of valid, clinically coherent, interoperable FHIR and CQL knowledge artifacts.
author: Connectathon Track Proposal
---

<!-- _class: title -->

<div class="eyebrow">Proposed HL7 FHIR Connectathon 43 track</div>

# AI-Assisted Development of Clinical Reasoning Knowledge

<p class="lede">Testing how clinical source material can become valid, clinically coherent, interoperable FHIR and CQL knowledge artifacts.</p>

<p class="subtle">September 19–20, 2026 · Rockville, Maryland</p>

<!--
[Sources]
- https://confluence.hl7.org/spaces/FHIR/pages/468259447/2026+-+09+Connectathon+43
[/Sources]
-->
---

<div class="eyebrow">Purpose and intent</div>

## The track evaluates AI-assisted authoring of computable clinical knowledge

<div class="two-col">
<div class="rule-left">

### Hypothesis

AI-assisted methods can reduce the time and human effort needed to develop computable clinical knowledge, and can support more artifact types with a repeatable process.

</div>
<div class="rule-left">

### Required result

The resulting knowledge must remain source-traceable, structurally valid, clinically coherent, executable, and portable across independent implementations.

</div>
</div>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md
- https://confluence.hl7.org/spaces/FHIR/pages/477659466/2026+-+09+Clinical+Reasoning
[/Sources]
-->

---

<div class="eyebrow">Evaluation questions</div>

## The track records process performance and artifact quality

| Dimension | What the track records |
| --- | --- |
| **Efficiency** | elapsed authoring time, human review time, revision cycles, and blocking issues |
| **Scalability** | artifact types completed, reuse of the process, and response to source changes |
| **Validity** | FHIR validation, canonical resolution, CQL translation, and package checks |
| **Clinical coherence** | reviewer findings, corrections, internal consistency, and expected clinical behavior |
| **Interoperability** | equivalent results across CQL engines and preservation across FHIR repositories |

<p class="small subtle">Where a participant has a comparable conventional baseline, it should be reported. Otherwise, efficiency findings remain descriptive.</p>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#track-question
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#interoperability-test
[/Sources]
-->

---

<div class="eyebrow">Common test design</div>

## Participants use common inputs and acceptance criteria

<div class="pipeline">
<div>
<h3>01 · Inputs</h3>
<p>Approved clinical source corpus and shared use-case statement.</p>
</div>
<div>
<h3>02 · Method</h3>
<p>Any AI-assisted or conventional authoring approach.</p>
</div>
<div>
<h3>03 · Disclosure</h3>
<p>Record tools, versions, instructions, decisions, and human review.</p>
</div>
<div>
<h3>04 · Outputs</h3>
<p>The same required knowledge artifacts and executable behaviors.</p>
</div>
<div>
<h3>05 · Evaluation</h3>
<p>The same validation, clinical review, fixtures, and interoperability tests.</p>
</div>
</div>

<p class="small subtle">No participant implementation defines the reference result. The documented clinical intent and expected behaviors do.</p>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#participant-task
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/use-cases/steadi/test-bundles/README.md
[/Sources]
-->

---

<div class="eyebrow">Use case</div>

## Older-adult fall-risk screening and prevention

<div class="two-col">
<div>

### Patient-level questions

For a community-dwelling adult age 65 or older:

1. Is the patient in scope for screening?
2. Was the three-question screen completed?
3. Does the result indicate increased fall risk?
4. Which evidence-linked action is applicable?

</div>
<div>

### Population-level question

Across a measurement period, what proportion of eligible patients completed the screen?

### Knowledge forms exercised

Evidence · guideline · assessment · measure · terminology · CQL logic

</div>
</div>

<!--
[Sources]
- https://www.cdc.gov/steadi/media/pdfs/STEADI-Algorithm-508.pdf
- https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/falls-prevention-community-dwelling-older-adults-interventions
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#seed-use-case
[/Sources]
-->

---

<div class="eyebrow">Clinical scope</div>

## The baseline defines a narrow clinical scope

<div class="two-col">
<div class="rule-left">

### Included

- community-dwelling adults age 65 or older
- ambulatory context
- CDC STEADI three key questions
- increased risk when any completed answer is yes
- exercise and individualized multifactorial guidance
- track-authored screening-completion measure

</div>
<div class="rule-left">

### Excluded

- diagnosis or emergency triage after a fall
- automatic ordering of an intervention
- inpatient, hospice, or long-term-care populations
- equivalence claims to CMS139FHIR
- real-world quality reporting or clinical deployment

</div>
</div>

<!--
[Sources]
- https://www.cdc.gov/steadi/media/pdfs/STEADI-Algorithm-508.pdf
- https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/falls-prevention-community-dwelling-older-adults-interventions
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#seed-use-case
[/Sources]
-->

---

<div class="eyebrow">Source material</div>

## The source corpus covers evidence, recommendation, workflow, and formalization

| Source | Role in the use case |
| --- | --- |
| **CDC STEADI algorithm and pocket guide** | three-question assessment and screen–assess–intervene workflow |
| **USPSTF 2024 recommendation** | exercise recommendation and individualized multifactorial consideration |
| **USPSTF evidence update and open systematic review** | population, outcomes, benefits, harms, and evidence context |
| **LOINC and HL7 CPG / Using CQL with FHIR** | terminology and computable-artifact guidance |
| **CMS139FHIR** | comparison point only; not copied or represented as the track measure |

<p class="small subtle">Redistributable snapshots are included in the repository; standards and comparison references remain link-only. Derived statements must retain stable source locators.</p>

<!--
[Sources]
- https://www.cdc.gov/steadi/media/pdfs/STEADI-Algorithm-508.pdf
- https://www.cdc.gov/steadi/media/pdfs/steadi-pocketguide-508.pdf
- https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/falls-prevention-community-dwelling-older-adults-interventions
- https://www.ncbi.nlm.nih.gov/books/NBK604238/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11590344/
- https://loinc.org/
- https://hl7.org/fhir/uv/cpg/
- https://hl7.org/fhir/uv/cql/
- https://ecqi.healthit.gov/ecqm/fhir-ec/2026/cms0139fhir
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/use-cases/steadi/sources/manifest.yaml
[/Sources]
-->

---

<div class="eyebrow">Source-to-output mapping</div>

## Each source role has a defined computable destination

| Source role | Structured knowledge | Primary FHIR output |
| --- | --- | --- |
| Evidence review | benefits, harms, population, outcomes | `Evidence`, `EvidenceVariable` |
| Recommendation | applicability, strength, action | `PlanDefinition`, `ActivityDefinition`, `Library` |
| STEADI workflow | screening and follow-up decisions | `PlanDefinition`, `ActivityDefinition` |
| Three-question screen | questions, answers, completeness, positive result | `Questionnaire`, `Library` |
| Track measure definition | population and completion logic | `Measure`, `Library` |
| Terminology and packaging guidance | bindings, dependencies, canonical identity | `ValueSet`, `ImplementationGuide` |

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#seed-use-case
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#participant-task
[/Sources]
-->

---

<div class="eyebrow">Expected output</div>

## The submission includes reviewable knowledge and FHIR R4 artifacts

<div class="three-col">
<div class="rule-top">

### Reviewable knowledge

Evidence summary · recommendation decision table · assessment definition · measure definition · terminology definition

</div>
<div class="rule-top">

### FHIR knowledge artifacts

`Evidence` · `EvidenceVariable` · `Questionnaire` · `Library` · `PlanDefinition` · `ActivityDefinition`

</div>
<div class="rule-top accent-top">

### Measure and package

`Measure` · `ValueSet` · `ImplementationGuide` · stable canonicals · exact dependency versions

</div>
</div>

<div class="band teal">
Every clinical statement and operational choice must be distinguishable and traceable to its source or track-authored rationale.
</div>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#participant-task
- https://hl7.org/fhir/R4/
[/Sources]
-->

---

<div class="eyebrow">Expected executable behavior</div>

## CQL expresses assessment, guidance, and measure semantics

<div class="two-col">
<div class="rule-left">

### Required named behaviors

- `In Screening Population`
- `Completed Three Question Screen`
- `At Increased Fall Risk`
- `Exercise Intervention Applicable`
- `Consider Multifactorial Intervention`
- `Initial Population`, `Denominator`, `Numerator`

</div>
<div class="rule-left">

### Deliverable package

- CQL source using a portable subset
- translated ELM JSON and translation logs
- FHIR R4 NPM package
- synthetic patient Bundles
- engine-neutral expected results
- exact translator, engine, and dependency versions

</div>
</div>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#required-executable-behavior
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/use-cases/steadi/test-bundles/README.md
- https://hl7.org/fhir/uv/cql/
[/Sources]
-->

---

<div class="eyebrow">Clinical coherence</div>

## Human review verifies that the artifacts tell the same clinical story

<div class="two-col">
<div class="rule-left">

### Review questions

- Are source statements separated from track-authored choices?
- Are population, recommendation strength, and actions preserved?
- Do the assessment, guideline, measure, and CQL agree?
- Are uncertainty and incomplete data represented explicitly?

</div>
<div class="rule-left">

### Failure examples

- missing answer treated as a negative answer
- increased risk represented as a diagnosis
- exercise and multifactorial recommendations collapsed
- unsupported code, threshold, or population invented
- measure represented as CMS139FHIR

</div>
</div>

<div class="band">
FHIR validation and CQL compilation are necessary, but they are not clinical approval.
</div>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#review-boundaries
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#seed-use-case
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#required-executable-behavior
[/Sources]
-->

---

<div class="eyebrow">Shared test cases</div>

## Synthetic fixtures make the expected behavior observable

| Case | Expected result |
| --- | --- |
| Adult younger than 65 | outside screening and measure population |
| Eligible adult; all answers no | complete screen; not at increased risk |
| Eligible adult; unsteady yes | increased risk; exercise applicable |
| Eligible adult; prior fall yes | increased risk; multifactorial consideration |
| Eligible adult; incomplete response | screen incomplete; risk unknown; numerator false |
| Eligible adult; no response | screen incomplete; risk unknown; numerator false |

<div class="band">
Missing data must remain unknown. It must not silently become a negative screen.
</div>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/use-cases/steadi/test-bundles/README.md
[/Sources]
-->

---

<div class="eyebrow">Interoperability testing</div>

## Interoperability testing covers validation, translation, execution, and storage

<div class="pipeline">
<div>
<h3>01 · Validate</h3>
<p>Validate FHIR R4 resources and the package.</p>
</div>
<div>
<h3>02 · Round-trip</h3>
<p>Store and retrieve artifacts from independent FHIR repositories.</p>
</div>
<div>
<h3>03 · Translate</h3>
<p>Translate the same CQL and record diagnostics.</p>
</div>
<div>
<h3>04 · Execute</h3>
<p>Run every synthetic fixture in independent CQL engines.</p>
</div>
<div>
<h3>05 · Compare</h3>
<p>Compare values, null semantics, versions, and discrepancies.</p>
</div>
</div>

<p class="small subtle">Baseline acceptance requires agreement across at least two independent CQL implementations and round-trip testing in at least two FHIR implementations.</p>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#interoperability-test
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/use-cases/steadi/test-bundles/README.md
- https://confluence.hl7.org/spaces/FHIR/pages/477659466/2026+-+09+Clinical+Reasoning
[/Sources]
-->

---

<!-- _class: closing -->

<div class="eyebrow">Expected track result</div>

## The outcome is evidence about the process and the artifacts

<div class="two-col">
<div class="rule-top">

### Process evidence

- authoring and review effort
- revision history and human decisions
- repeatability across knowledge-artifact types
- implementation-specific limitations

</div>
<div class="rule-top">

### Knowledge evidence

- reviewed source-to-output traceability
- valid FHIR and translatable CQL
- clinically coherent fixture behavior
- cross-implementation result matrix and issue list

</div>
</div>

<p class="decision">The central question: can AI-assisted development improve efficiency and scale while preserving clinical quality and interoperability?</p>

<!--
[Sources]
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#track-question
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#participant-task
- https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/main/README.md#interoperability-test
[/Sources]
-->
