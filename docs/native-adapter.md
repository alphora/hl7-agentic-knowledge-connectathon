# Native operation adapter

`tools/java/SteadiNative.java` invokes the pinned runtime's `LibraryProcessor.evaluate`, `QuestionnaireResponseProcessor.extract`, and `PlanDefinitionProcessor.applyR5`. Despite the SDK method name, this adapter uses the R4 context and produces R4 resources. It creates a fresh definition-only repository and passes the current patient data explicitly with `useServerData=false` for every invocation.

CLI wrapper:

```text
python tools/native-runtime.py --jar PATH knowledge.json patient-data.json parameters.json Patient/id Encounter/id NEW_OUTPUT_DIRECTORY
```

`knowledge.json` is a collection Bundle of the supplied Questionnaire and authored knowledge definitions. `patient-data.json` is the original fixture Bundle. Parameters include `Encounter Id` (String), `Track Context Confirmed` (Boolean), and `Measurement Period` (Period with start/end); optional `Questionnaire Response Id` selects among multiple responses. `Encounter Id` must match the encounter argument. Output directories must be new, preventing stale output from masquerading as the current invocation.

The wrapper verifies the entire runtime JAR's SHA-256, extracts only its library members, and builds an explicit classpath from those verified members. Extra files in the cache do not join the classpath. It compiles the current adapter with Javac before execution.

## Explicit output adaptation

The adapter saves raw operation results before transformation. Native extraction supplies the Observation values, codes, status, patient, encounter, timestamps and performer. It does not read expected fixture output.

The pinned SDK's extraction metadata requires these explicit corrections for this contract:

1. Use the supplied Questionnaire's explicit observation-extraction category, including its terminology system URI.
2. Copy the selected response's security labels to extracted Observations and the extraction Bundle.
3. Set `derivedFrom` to the actual original response's relative reference.
4. Add valid PUT request URLs for native-generated Observation IDs.

For `$apply`, raw action references contain only generated IDs. The adapter resolves those against actual returned resources to produce `ResourceType/id` references. It does not create missing guidance or modify clinical applicability or message text. It re-parses serialized native output before reference adaptation because the SDK's in-memory no-action result contains null list entries that cannot be copied safely.

`extraction-raw.json` and `apply-raw.json` retain engine output; `extraction.json` and `apply.json` are the adapter deliverables. This is adapter conformance evidence, not proof that an unmodified SDK produces the fixture contract. The Java code rejects nested error/fatal OperationOutcomes. A typed Boolean with `data-absent-reason=unknown` is accepted as unknown; absent results or errors are not silently converted to null.

## Verification boundaries

The native harness checks all eight values, extraction invocation/count/copied fields, exact two distinct guidance messages, correct patient/encounter, and resolvable action references. It retains raw output and input/tool hashes. Both the JavaScript CQL implementation and native JVM implementation execute the six original fixtures. Additional controls have separate identities and do not replace the supplied oracle.

This is a local SDK adapter, not an HTTP FHIR server or general interview platform. Server round trips, full profile/terminology validation and human clinical review require separate evidence.
