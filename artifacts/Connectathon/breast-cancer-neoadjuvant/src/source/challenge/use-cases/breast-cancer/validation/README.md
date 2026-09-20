# Validation evidence

Checked on 2026-09-19. These results concern the shared input corpus and
fixtures; participant-generated clinical knowledge is a separate deliverable.

## Fixture integrity

`python3 use-cases/breast-cancer/scripts/validate_fixtures.py` passed for
13 synthetic patient cases and 104 typed assertions. The check covers internal
references, patient/tumor linkage, dates, declared coding, Boolean/null behavior,
the 10 mm boundary, and the 15 mm/1.5 cm pair. It checks the published contract;
it does not execute CQL or independently validate the clinical rule.

## FHIR validation

The official HL7 FHIR Validator **6.10.2**, Java **25.0.2**, validated all
13 patient bundles and the local CodeSystem against FHIR R4 **4.0.1**:
**0 errors, 0 fatal issues, 215 warnings**.

| Warning | Count | Interpretation |
| --- | ---: | --- |
| Missing generated narrative (`dom-6`) | 114 | Fixtures supply structured content and per-case Markdown summaries; generated resource narratives are absent |
| Missing Observation performer | 88 | Synthetic Observations do not identify an observing practitioner |
| UCUM validation unavailable | 13 | `-tx n/a` disables terminology services; `mm`/`cm` were not validated by that service |

The [machine-readable summary](fhir-validator-summary.json) records exact
package versions, all unique diagnostics, per-file counts and SHA-256 hashes,
and the original report's SHA-256. Each file was checked to be unchanged since
the run before its checksum was captured. The summary omits the full report's
repeated generated HTML narratives.

Reproduce from the repository root with a locally installed validator JAR:

```sh
java -jar /path/to/validator_cli-6.10.2.jar \
  use-cases/breast-cancer/test-bundles/cases/*/bundle.json \
  use-cases/breast-cancer/test-bundles/code-system.json \
  -version 4.0.1 -tx n/a -output /tmp/breast-cancer-validator-results.json
```

This is base R4 validation, with no mCODE or CPG profile claim. The disabled
terminology server limits code validation. The separate
[terminology lookup record](terminology-lookups.json) confirms five active
LOINC 2.81 observation codes and their displays. It records the unavailable
answer-code lookups and the public LOINC answer-list reference; it is not a
ValueSet membership or complete terminology-validation result.

## Sources and remaining participant checks

All four source-text byte counts and SHA-256 hashes match the
[source manifest](../sources/manifest.yaml). Attribution, selected sections,
displayed dates, retrieval times, and excluded content are recorded there.
ASCO publications are link-only, with the access limits documented in the
[source guide](../sources/README.md).

CQL translation, CQL execution, `$apply`, FHIR server round trips, and independent
clinical review have not been performed. Participants must supply those results
for their authored knowledge artifacts. Existing STEADI inputs are unchanged.
