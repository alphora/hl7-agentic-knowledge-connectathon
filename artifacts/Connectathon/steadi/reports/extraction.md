# Generated QuestionnaireResponse extraction

The contract under test is the output of `$extract` from a completed response. It does not require loading the challenge's original QuestionnaireResponse as the input to our decision evaluation. CEL answer Observations are valid test setup.

## Primary result

Three in-scope generated responses (all-no, unsteady-yes and prior-fall-yes), completed by the client, each produce **three final Observations** through the native `QuestionnaireResponseProcessor.extract` operation in the pinned CQF engine. The generated Questionnaires, linkIds, definitions and original saved Q/QR files were not modified. No extracted output was repaired.

The client copies each populated generated response, sets status to completed, and supplies authored time, encounter and author from the synthetic case context. These are normal client completion/launch fields. The operation receives Patient and Encounter context, not the input answer Observations, so the retained output comes from QR extraction.

| Output check | Result for all three responses |
| --- | --- |
| Three Observations | Pass |
| Final status | Pass |
| Boolean answers | Pass, including explicit false |
| Patient subject | Pass |
| QR authored time to Observation effective time | Pass |
| Survey category | Pass |
| Specified LOINC question codes | Fail: authored local codes emitted |
| Encounter | Fail: absent |
| QR author to performer | Fail: absent |
| QR derivedFrom reference | Fail: absent |

The incomplete and absent-response cases are not submitted to extraction. This is verified harness behavior, not a claim that the extraction engine itself enforces the completion gate.

## Younger case

The fourth completed source fixture is younger than65, so our age-gated apply correctly produces no Questionnaire. It is excluded from the three generated-output checks above. A supplemental test reused the unchanged generated all-no Questionnaire for a younger client response; extraction still returns three final Observations independently of the screening gate. This is a reusable-form operation test, not an extra apply-produced response.

## Evidence and reproduction

Raw operation inputs/results and per-field comparisons are in `tests/verification/extraction/`, particularly `verification.json`. The helper `reports/tools/check-extraction.py` invokes `reports/tools/ExtractDemo.java` using the supplied Java command and CQF classpath. The SDK used here was extracted from `cqf-fhir-cr-cli-4.7-crl-4aee6041.jar`, SHA256 `9870fc867547f65518c5cd6e698ace77b60a9e98797ed38330c25d06cbf5cb2e`.

From the artifact directory, pass `--classpath` pointing to that engine's extracted `lib/*` and classes and optionally `--java` to the Java executable. Native output is retained verbatim. The report deliberately preserves failed field checks and does not claim full extraction-contract conformance.

CRL was asked which existing authoring/configuration options address external coding and the missing context fields. No new language feature or engine change is assumed necessary from this test alone.
