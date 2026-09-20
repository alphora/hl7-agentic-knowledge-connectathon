#!/usr/bin/env python3
"""Validate fixture structure and the published contract, not CQL or FHIR profiles."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'test-bundles'
BASE = 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir'
CS = BASE + '/CodeSystem/breast-cancer-fixture'
LOINC = 'http://loinc.org'
EXPRESSIONS = [
    'Has Active Confirmed Invasive Breast Cancer', 'Has Nonmetastatic Disease',
    'In Neoadjuvant Review Population', 'Is Triple Negative',
    'Has Clinically Positive Nodes', 'Has Clinical T1c Or Higher',
    'Meets Tumor Or Node Criterion', 'Neoadjuvant TNBC Guidance Applicable',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def codes(concept, system):
    return [c['code'] for c in concept.get('coding', []) if c.get('system') == system]


def conjunction(*values):
    return False if False in values else None if None in values else True


def disjunction(*values):
    return True if True in values else None if None in values else False


def references(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == 'reference':
                yield item
            else:
                yield from references(item)
    elif isinstance(value, list):
        for item in value:
            yield from references(item)


def date(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def validate():
    manifest = read(ROOT / 'manifest.json')
    local_cs = read(ROOT / manifest['codeSystem'])
    local_codes = {c['code'] for c in local_cs['concept']}
    require(local_cs['url'] == CS, 'Local CodeSystem canonical mismatch')
    require(local_cs['count'] == len(local_codes), 'Local CodeSystem count/duplicates')
    require(manifest['expressions'] == EXPRESSIONS, 'Manifest expression contract drift')
    require(manifest['fhirVersion'] == '4.0.1', 'FHIR version mismatch')
    require(len({c['id'] for c in manifest['cases']}) == len(manifest['cases']), 'Duplicate case ids')
    require({c['id'] for c in manifest['cases']} == {p.name for p in (ROOT / 'cases').iterdir() if p.is_dir()}, 'Manifest does not cover case directories')
    outcomes = set()
    sizes = {}
    for case in manifest['cases']:
        ident = case['id']
        bundle = read(ROOT / case['bundle'])
        assertions = read(ROOT / case['assertions'])
        require((ROOT / case['summary']).is_file(), ident + ': missing summary')
        require(bundle['resourceType'] == 'Bundle' and bundle['type'] == 'collection', ident + ': bundle type')
        require(assertions['fixtureId'] == ident, ident + ': assertion fixture id')
        require(assertions['bundle'] == 'bundle.json', ident + ': assertion bundle path')
        require(assertions['fhirVersion'] == manifest['fhirVersion'], ident + ': assertion FHIR version')
        resources = [e['resource'] for e in bundle['entry']]
        by_ref = {r['resourceType'] + '/' + r['id']: r for r in resources}
        require(len(by_ref) == len(resources), ident + ': duplicate resource ids')
        require(len({e['fullUrl'] for e in bundle['entry']}) == len(resources), ident + ': duplicate fullUrls')
        evaluation = date(assertions['evaluationContext']['evaluationDateTime'])
        require(evaluation == date(manifest['evaluationDateTime']), ident + ': evaluation time drift')
        patients = [r for r in resources if r['resourceType'] == 'Patient']
        require(len(patients) == 1, ident + ': requires exactly one Patient')
        patient_ref = 'Patient/' + patients[0]['id']
        require(patients[0]['id'] == assertions['evaluationContext']['patientId'], ident + ': patient context mismatch')
        for entry in bundle['entry']:
            r = entry['resource']
            require(entry['fullUrl'] == BASE + '/' + r['resourceType'] + '/' + r['id'], ident + ': fullUrl mismatch')
            require(len(r['id']) <= 64, ident + ': FHIR id length')
            require(any(c.get('system') == 'http://terminology.hl7.org/CodeSystem/v3-ActReason' and c.get('code') == 'HTEST' for c in r['meta']['security']), ident + ': missing synthetic label')
            for ref in references(r):
                require(ref in by_ref, ident + ': unresolved reference ' + ref)
            if r['resourceType'] in ('Condition', 'Observation'):
                require(r['subject']['reference'] == patient_ref, ident + ': wrong patient')
            for concept in [r.get('code', {}), r.get('valueCodeableConcept', {})]:
                require(all(c in local_codes for c in codes(concept, CS)), ident + ': undeclared local code')
            for coding in r.get('code', {}).get('coding', []):
                if coding['system'] == LOINC:
                    require(coding.get('version') == '2.81', ident + ': LOINC version missing')
        conditions = [r for r in resources if r['resourceType'] == 'Condition']
        require(len(conditions) <= 1, ident + ': fixture contract permits at most one indexed Condition')
        diagnosis = any('invasive-breast-carcinoma' in codes(c['code'], CS) and 'active' in codes(c['clinicalStatus'], 'http://terminology.hl7.org/CodeSystem/condition-clinical') and 'confirmed' in codes(c['verificationStatus'], 'http://terminology.hl7.org/CodeSystem/condition-ver-status') for c in conditions)
        observations = [r for r in resources if r['resourceType'] == 'Observation']
        for observation in observations:
            require(observation['status'] == 'final', ident + ': fixture observation must be final')
            require(date(observation['effectiveDateTime']) <= date(observation['issued']) <= evaluation, ident + ': invalid chronology')
            if diagnosis:
                require(observation.get('focus') == [{'reference': 'Condition/' + conditions[0]['id']}], ident + ': missing same-cancer linkage')
        def result(code, system=CS, require_anchor=True):
            if require_anchor and not diagnosis:
                return None
            matches = [o for o in observations if code in codes(o['code'], system)]
            require(len(matches) <= 1, ident + ': ambiguous duplicate input')
            return matches[0] if matches else None
        def stage(code, positives, negatives):
            observation = result(code)
            if observation is None:
                return None
            values = codes(observation['valueCodeableConcept'], CS)
            require(len(values) == 1, ident + ': ambiguous staging value')
            require(values[0] in positives | negatives, ident + ': unsupported staging value')
            return values[0] in positives
        def negative_receptor(code):
            observation = result(code, LOINC)
            if observation is None:
                return None
            values = codes(observation['valueCodeableConcept'], LOINC)
            if 'LA6577-6' in values:
                return True
            if 'LA6576-8' in values:
                return False
            require(codes(observation['valueCodeableConcept'], CS) == ['equivocal'], ident + ': unexpected receptor answer')
            return None
        m0 = stage('clinical-m', {'cM0'}, {'cM1'})
        nodes = stage('clinical-n', {'cN1', 'cN2', 'cN3'}, {'cN0'})
        tumor = stage('clinical-t', {'cT1c', 'cT2', 'cT3', 'cT4'}, {'cT1mi', 'cT1a', 'cT1b'})
        tnbc = conjunction(*(negative_receptor(c) for c in ('85337-4', '85339-0', '48676-1')))
        population = conjunction(diagnosis, m0)
        criterion = disjunction(nodes, tumor)
        expected = [diagnosis, m0, population, tnbc, nodes, tumor, criterion, conjunction(population, tnbc, criterion)]
        require([a['expression'] for a in assertions['assertions']] == EXPRESSIONS, ident + ': expression contract mismatch')
        for assertion, actual in zip(assertions['assertions'], expected):
            exp = assertion['expected']
            require(exp['type'] == 'Boolean', ident + ': unexpected assertion type')
            require(exp['value'] is actual, ident + ': wrong expectation for ' + assertion['expression'])
            require((exp.get('semantics') == 'unknown') == (actual is None), ident + ': null semantic annotation mismatch')
        outcomes.add(expected[-1])
        size = result('21889-1', LOINC, require_anchor=False)['component'][0]
        require(codes(size['code'], LOINC) == ['33728-7'], ident + ': wrong dimension code')
        q = size['valueQuantity']
        require(q['system'] == 'http://unitsofmeasure.org' and q['code'] in ('mm', 'cm'), ident + ': unsupported quantity')
        mm = q['value'] * (10 if q['code'] == 'cm' else 1)
        sizes[ident] = mm
        t_code = codes(result('clinical-t', require_anchor=False)['valueCodeableConcept'], CS)[0]
        require((t_code != 'cT1b' or 5 < mm <= 10) and (t_code != 'cT1c' or 10 < mm <= 20) and (t_code != 'cT2' or 20 < mm <= 50), ident + ': size/stage inconsistency')
    require(outcomes == {True, False, None}, 'Missing positive, negative, or unknown outcome')
    require(sizes['tnbc-t1c-n0'] == sizes['tnbc-t1c-n0-cm'], 'Unit equivalence fixtures differ')
    require(sizes['tnbc-t1b-n0-10mm'] == 10, 'Boundary case no longer exactly 10 mm')
    print(f"PASS: {len(manifest['cases'])} fixtures; references, coding, dates, boundaries, unit equivalence, and {len(EXPRESSIONS) * len(manifest['cases'])} typed assertions checked.")
    print('This is a fixture-contract check, not HL7 FHIR validation, terminology validation, CQL translation, or CQL execution.')


if __name__ == '__main__':
    validate()
