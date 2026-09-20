"""Compare actual typed native results to unchanged shared fixture assertions."""
import argparse
import json
from pathlib import Path

DAR = "http://hl7.org/fhir/StructureDefinition/data-absent-reason"


def boolean_value(parameter):
    if isinstance(parameter.get("valueBoolean"), bool):
        return parameter["valueBoolean"]
    absent = parameter.get("_valueBoolean", {}).get("extension", [])
    if any(e.get("url") == DAR and e.get("valueCode") == "unknown" for e in absent):
        return None
    raise ValueError("No typed Boolean result or explicit unknown marker")


def resources(value):
    if isinstance(value, dict):
        if "resourceType" in value:
            yield value
        for child in value.values():
            yield from resources(child)
    elif isinstance(value, list):
        for child in value:
            yield from resources(child)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_root", type=Path)
    parser.add_argument("actual_root", type=Path)
    args = parser.parse_args()
    manifest = json.loads((args.fixture_root / "manifest.json").read_text(encoding="utf-8"))
    checks = []
    activity_checks = []
    for case in manifest["cases"]:
        oracle = json.loads((args.fixture_root / case["assertions"]).read_text(encoding="utf-8"))
        actual_path = args.actual_root / case["id"] / "evaluation.json"
        params = []
        failure = None
        try:
            actual = json.loads(actual_path.read_text(encoding="utf-8"))
            if actual.get("resourceType") != "Parameters":
                raise ValueError("Expected Parameters evaluation response")
            params = actual.get("parameter", [])
            errors = [p for p in params if p.get("resource", {}).get("resourceType") == "OperationOutcome"]
            if errors:
                raise ValueError("Evaluation contains OperationOutcome; cannot count as unknown")
        except (OSError, ValueError) as error:
            failure = str(error)
        for assertion in oracle["assertions"]:
            expected = assertion["expected"]
            row = {"case": case["id"], "expression": assertion["expression"], "expected": expected["value"]}
            try:
                if failure:
                    raise ValueError(failure)
                if expected["type"] != "Boolean":
                    raise ValueError("Unexpected oracle type")
                matches = [p for p in params if p.get("name") == assertion["expression"]]
                if len(matches) != 1:
                    raise ValueError(f"Expected one result, found {len(matches)}")
                row["actual"] = boolean_value(matches[0])
                row["pass"] = row["actual"] is expected["value"]
            except ValueError as error:
                row.update({"pass": False, "error": str(error)})
            checks.append(row)
        expected_applicability = next(a["expected"]["value"] for a in oracle["assertions"] if a["expression"] == "Neoadjuvant TNBC Guidance Applicable")
        expected_activities = ["breast-cancer-neoadjuvant-oncology-review-guidance"] if expected_applicability is True else []
        activity_row = {"case": case["id"], "expected": expected_activities}
        try:
            applied = json.loads((args.actual_root / case["id"] / "apply-raw.json").read_text(encoding="utf-8"))
            all_resources = list(resources(applied))
            errors = [issue for r in all_resources if r.get("resourceType") == "OperationOutcome" for issue in r.get("issue", []) if issue.get("severity") in {"error", "fatal"}]
            actual_activities = sorted(r.get("id") for r in all_resources if r.get("resourceType") == "CommunicationRequest")
            activity_row.update({"actual": actual_activities, "errors": errors, "pass": not errors and actual_activities == expected_activities})
        except (OSError, ValueError) as error:
            activity_row.update({"pass": False, "error": str(error)})
        activity_checks.append(activity_row)
    result = {"cases": len(manifest["cases"]), "checks": len(checks), "passed": sum(c["pass"] for c in checks), "results": checks, "activityChecks": activity_checks, "activityPassed": sum(c["pass"] for c in activity_checks)}
    (args.actual_root / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{result['passed']}/{result['checks']} typed assertions passed across {result['cases']} original fixtures")
    print(f"{result['activityPassed']}/{result['cases']} exact activity/error checks passed")
    for c in checks:
        if not c["pass"]:
            print(json.dumps(c))
    raise SystemExit(0 if all(c["pass"] for c in checks + activity_checks) else 1)


if __name__ == "__main__":
    main()
