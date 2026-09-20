# STEADI Connectathon demonstration

Clinical concepts, assessment conditions and guidance are authored in `src/crl/steadi.crl`. The six synthetic examples are authored in `src/cel/mv/steadi.cel`. CRL 6.4.1 generates the CQL, FHIR definitions, CEL case data and native Questionnaire/QuestionnaireResponse results.

## Open the demo

The working project is `E:/src/hl7-agentic-knowledge-connectathon`, on KELP branch `artifact/steadi`. The artifact is `artifacts/Connectathon/steadi`; all paths below are relative to that artifact. These are the actual working files.

1. Open `src/cel/mv/steadi.cel` in the CRL-enabled VS Code window.
2. Run **CRL: Show Medical Validation** from the command palette. Start with **Eligible Unsteady Yes**, then **Eligible Prior Fall Yes**. The installed scenario projection was checked for the first case: both Exercise Guidance and Multifactorial Intervention Guidance are produced, with no diagnostic errors. This check verifies the view-model, not a visual browser inspection.
3. Use the generated FHIR Questionnaire/QuestionnaireResponse files under `tests/results/fhir/patient/` for the native output. `tests/results/questionnaire-manifest-mv.json` maps every case to its files and terminal state. The four no-guidance cases are verified by native evidence; their absent CEL action assertions cause the separate CRE/cockpit correspondence check to remain unchecked.
4. Inspect each patient's `measurereport/steadi-screening-completion.json`, and the summary at `tests/results/fhir/population/measurereport/steadi-screening-completion.json`.

Recheck all 48 retained native expectations from an artifact terminal:

```powershell
python reports/tools/verify-steadi-native.py
```

This checks recorded actual engine output; it does not rerun the engine. Expected output: 48 assertions passed, denominator 5, numerator 3, score 0.6.

## Working-directory handoff

The CRL/CEL model, generated CQL/FHIR, manual companions, anchors and provenance have been saved and released through KELP. QA was saved at `cc2a114a6c442e94aa50d9d03ba2e7c7cecd539c` and released clean. The fresh native Q/QR manifest was generated on 2026-09-20; all ten resource hashes were checked. Earlier native expression/Measure evidence was retained only after comparing the installed CRL, CEL, CQL, FHIR and all 20 patient-data files with its verified inputs: their bytes match (excluding empty KELP scaffolding files).

## Recorded execution

- 48/48 supplied named-expression expectations agree with native CQL evaluation over the six CEL-emitted cases.
- The unsteady-positive and prior-fall-positive cases each produce exactly Exercise Guidance and Multifactorial Intervention Guidance. The other four cases produce neither.
- Native results contain five Questionnaire/QuestionnaireResponse pairs. The younger patient produces no questionnaire.
- The manual Measure references the generated `SteadiInterface|0.0.0` and its Initial Population, Denominator and Numerator expressions. Native evaluation produces six individual MeasureReports and a summary: population 5, denominator 5, numerator 3, score 0.6.
- Canonical source generation preserved the supplied refined Markdown in a literal DOCX carrier and reported no warnings. Human visual pagination was not verified.

These results demonstrate the generated logic and native operations using CEL-supplied input. The challenge extraction check concerns completed responses, not how answers were initially populated. Full conformance still has the specific differences listed below; no clinical-validation claim is made.

## Established companion authoring

Measures are supported through our established workflow: CRL generates the supporting logic and artifacts; the agent authors the small Measure resource manually alongside them. Direct Measure resource generation is on the backlog and has not been a priority because this wrapper is straightforward to author. This demonstration uses that established approach.

CRL does not currently generate Evidence and EvidenceVariable resources. The two Evidence resources and seven EvidenceVariables were authored manually; direct language support will be considered. Their supplied findings and citations are retained, and Evidence documentation links point to the generated guidance activities.

Authored companion inputs live in `src/companion-source/fhir`. They are assembled alongside generated resources only after CRL emission, because re-emission replaces the generated FHIR directory.

## Explicit differences and unfinished checks

- CEL supplies the initial answers as Observations. That is not itself a deviation from the extraction contract. Native `$extract` on the three in-scope completed client responses returns three final Observations each. See the [extraction results](extraction.md).
- Actual extracted Observations use the authored local codes rather than the specified LOINC codes; encounter, author/performer and QR `derivedFrom` are also missing. Status, survey category, Boolean values, subject and authored-to-effective time pass. These are observed output differences, not an asserted inability of CRL; supported authoring/configuration options have been queried with CRL.
- The age source evaluates age today, rather than at the encounter. The supplied six birthdates have the same threshold classification for this demonstration.
- The demonstration Measure checks age and answer presence. It does not enforce completed QuestionnaireResponse status, same-response/encounter association or measurement-period inclusion.
- Generated identifiers and linkIds are preserved. We could manually remap them to the challenge identifiers, but deliberately did not: the demonstration uses our tooling's capabilities. The reason exact linkId equality is necessary remains a question for the challenge organizers.
- Independent participant execution and FHIR-server round trips were not performed, as scoped by the operator.
- FHIR npm packaging awaits delivery of CRL's implemented packager, which was omitted from the installed 6.4.1 build. KELP artifact packing is not a substitute.
- One bounded native demo review completed: no critical findings; the verification helper's temporary paths were corrected and rechecked. No human medical-validation claim is made.
- Provenance FINAL validation remains `pass:false`: five source-gap findings and four unchecked no-action CRE/cockpit cases. All 14 model references have source attribution; this does not imply complete implementation. See [provenance findings](provenance/README.md) and [full validation output](provenance/validation-final.json).

KELP manages the source, authored inputs, generated outputs, tests, provenance and this report. The crash-interrupted lock was repaired under operator authorization with HEAD unchanged. Lifecycle saving is tracked separately from execution results.

To recheck the retained native evidence after loading this artifact, run `python reports/tools/verify-steadi-native.py` from the artifact directory. This reads the unchanged supplied assertions and actual engine outputs; it does not rerun the engine. The Java files beside it are diagnostic adapters requiring the recorded CQF engine dependency set and explicit artifact/output paths.
