"""Bounded FHIR R4 JSON-schema checks; not full profile/terminology validation."""
from pathlib import Path
import json,sys,hashlib,uuid
ROOT=Path(__file__).resolve().parents[1]
output=ROOT/'verification/fhir-json-structure.json';output.parent.mkdir(parents=True,exist_ok=True)
run_id=str(uuid.uuid4())
output.write_text(json.dumps({'status':'incomplete','runId':run_id})+'\n')
try:
 sys.path.insert(0,str(ROOT/'.cache/python'))
 import jsonschema
 schema=json.loads((ROOT/'.cache/fhir-schema/fhir.schema.json').read_bytes())
 native=json.loads((ROOT/'verification/measure-native/summary.json').read_text())
 assert native['status']=='passed' and len(native['cases'])==6,'Native report set is not a current complete pass'
 assessment=json.loads((ROOT/'verification/assessment-native/summary.json').read_text())
 assert assessment['status']=='passed' and len(assessment['cases'])==6 and len(assessment['controls'])==14,'Assessment run incomplete'
 for rel,digest in assessment['inputs'].items():
  assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,'Assessment input changed since execution: '+rel
 for row in assessment['cases']+assessment['controls']:
  assert row['passed'],'Unpassed assessment case'
  if 'guidanceCount' in row:
   applied=json.loads((ROOT/'verification/assessment-native'/row['name']/'apply.json').read_bytes())
   bundle=next(p['resource'] for p in applied['parameter'] if p['name']=='return')
   group=next(e['resource'] for e in bundle['entry'] if e['resource']['resourceType']=='RequestGroup')
   expected_actions=['exercise-guidance','multifactorial-guidance'] if row['guidanceCount']==2 else []
   assert sorted(a['id'] for a in group.get('action',[]))==expected_actions,'Missing or duplicate guidance action'
  for name,digest in row.get('outputs',{}).items():
   assert hashlib.sha256((ROOT/'verification/assessment-native'/row['name']/name).read_bytes()).hexdigest()==digest,'Changed native evidence'
 paths=list((ROOT/'input/fhir').rglob('*.json'))+list((ROOT/'generated/companions').rglob('*.json'))+list((ROOT/'verification/measure-native').glob('*.json'))
 for folder in (ROOT/'verification/assessment-native').iterdir():
  if folder.is_dir():
   paths.extend(folder/n for n in ('evaluation.json','extraction.json','apply.json') if (folder/n).exists())
 paths.append(ROOT/'dist/knowledge-transaction.json')
 rows=[]
 for path in paths:
  resource=json.loads(path.read_bytes())
  if 'resourceType' not in resource:continue
  typed={**schema,'oneOf':[{'$ref':'#/definitions/'+resource['resourceType']}]}
  errors=[]
  def leaves(e):
   if e.context:
    for child in e.context:leaves(child)
   else:errors.append({'path':list(e.path),'message':e.message})
  for err in jsonschema.Draft6Validator(typed).iter_errors(resource):leaves(err)
  rows.append({'path':path.relative_to(ROOT).as_posix(),'resourceType':resource['resourceType'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'errors':errors})
 assert rows,'No resources validated'
 report={'runId':run_id,'status':'passed' if all(not r['errors'] for r in rows) else 'failed','validator':'jsonschema4.25.1/Draft6','schema':json.loads((ROOT/'.cache/fhir-schema/origin.json').read_text()),'scope':'FHIR4.0.1 JSON structure only; not terminology/profile/invariant validation or source fidelity','resources':rows}
 (ROOT/'verification/fhir-json-structure.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'resourceCount':len(rows),'failed':[r for r in rows if r['errors']]}))
 assert report['status']=='passed'
except BaseException as error:
 output.write_text(json.dumps({'status':'failed','runId':run_id,'error':str(error)},indent=2)+'\n');raise
