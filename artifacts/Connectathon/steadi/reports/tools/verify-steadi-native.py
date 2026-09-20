"""Compare actual native output with unchanged supplied fixture assertions."""
import argparse
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-cases',type=Path,default=root/'src/source/challenge/test-bundles/cases')
source=parser.parse_args().source_cases
manifest=json.loads((root/'tests/data/fhir/cel-data-manifest.json').read_text())
mapping={'Younger Than 65':'younger-than-65','Eligible All No':'eligible-all-no','Eligible Unsteady Yes':'eligible-unsteady-yes','Eligible Prior Fall Yes':'eligible-prior-fall-yes','Eligible Incomplete Response':'eligible-incomplete-response','Eligible No Response':'eligible-no-response'}

def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values(): yield from walk(v)
    elif isinstance(x,list):
        for v in x: yield from walk(v)

def boolean(p):
    if type(p.get('valueBoolean')) is bool:return p['valueBoolean']
    ext=p.get('_valueBoolean',{}).get('extension',[])
    if any(e.get('url')=='http://hl7.org/fhir/StructureDefinition/data-absent-reason' and e.get('valueCode')=='unknown' for e in ext):return None
    raise AssertionError('Missing/unsupported typed Boolean carrier: '+repr(p))

checks=[]; cases=[]
for case in manifest['cases']:
    fixture=mapping[case['caseName']]
    compartment=Path(case['compartmentDir']).name
    native=root/'tests/verification/native'/compartment
    evaluation=json.loads((native/'evaluation.json').read_text())
    apply=json.loads((native/'apply-raw.json').read_text())
    errors=[i for obj in walk([evaluation,apply]) if obj.get('resourceType')=='OperationOutcome' for i in obj.get('issue',[]) if i.get('severity') in ('error','fatal')]
    assert not errors,(fixture,errors)
    actual={p['name']:boolean(p) for p in evaluation['parameter']}
    oracle=json.loads((source/fixture/'assertions.json').read_text())
    for assertion in oracle['assertions']:
        name=assertion['expression']; expected=assertion['expected']['value']
        checks.append({'case':fixture,'expression':name,'expected':expected,'actual':actual[name],'pass':actual[name] is expected})
    communications=[x for x in walk(apply) if x.get('resourceType')=='CommunicationRequest']
    expected_ids=['steadi-exercise-guidance','steadi-multifactorial-intervention-guidance'] if fixture in ('eligible-unsteady-yes','eligible-prior-fall-yes') else []
    actual_ids=sorted(x['id'] for x in communications)
    assert actual_ids==expected_ids,(fixture,actual_ids)
    report=json.loads((root/'tests/results/fhir'/case['compartmentDir']/'measurereport/steadi-screening-completion.json').read_text())
    assert report['status']=='complete',report
    populations={p['code']['coding'][0]['code']:p['count'] for p in report['group'][0]['population']}
    for code,expression in [('initial-population','Initial Population'),('denominator','Denominator'),('numerator','Numerator')]:
        assert populations[code]==int(actual[expression]),(fixture,code,populations)
    cases.append({'case':fixture,'engineErrors':errors,'guidance':actual_ids,'measurePopulations':populations,'rawDirectory':native.relative_to(root).as_posix()})
summary=json.loads((root/'tests/results/fhir/population/measurereport/steadi-screening-completion.json').read_text())
summary_counts={p['code']['coding'][0]['code']:p['count'] for p in summary['group'][0]['population']}
assert summary_counts=={'initial-population':5,'denominator':5,'numerator':3},summary_counts
assert summary['group'][0]['measureScore']['value']==0.6
record={'evidence':'native CQL evaluation, PlanDefinition apply and Measure evaluation over CEL-emitted local-answer facts','assertions':len(checks),'passed':sum(x['pass'] for x in checks),'checks':checks,'cases':cases,'measureSummary':summary_counts,'measureScore':0.6,'limits':['Not original shared QuestionnaireResponse ingestion or SDC extraction.','Current Patient age substitutes for encounter-age; supplied cases have the same threshold classification.','Measure does not enforce source QR completed status, encounter association or measurement-period inclusion.'],'crlSha256':hashlib.sha256((root/'src/crl/steadi.crl').read_bytes()).hexdigest()}
out=root/'tests/verification/native-verification.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ('assertions','passed','measureSummary','measureScore','limits')},indent=2))
assert record['passed']==record['assertions']==48
