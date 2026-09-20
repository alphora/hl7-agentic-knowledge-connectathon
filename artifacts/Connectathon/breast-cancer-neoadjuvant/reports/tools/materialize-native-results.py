"""Place unchanged original-fixture engine outputs in the KELP results entity."""
from pathlib import Path
import json,hashlib,shutil
root=Path(__file__).resolve().parents[2]
fixtures=root/'src/source/challenge/use-cases/breast-cancer/test-bundles'
raw=root/'tests/verification/native-current'
manifest=json.loads((fixtures/'manifest.json').read_text(encoding='utf-8'))
checks=json.loads((raw/'verification.json').read_text(encoding='utf-8'))
results=[]
for case in manifest['cases']:
 oracle=json.loads((fixtures/case['assertions']).read_text(encoding='utf-8'))
 patient=oracle['evaluationContext']['patientId']
 assert '/' not in patient and '\\' not in patient
 dest=root/'tests/results/fhir/patient'/patient/'parameters'
 dest.mkdir(parents=True,exist_ok=True)
 outputs=[]
 for source,name in [('evaluation.json','evaluation.json'),('apply-raw.json','apply.json')]:
  src=raw/case['id']/source;target=dest/name;shutil.copyfile(src,target)
  outputs.append({'path':target.relative_to(root).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
 activity=next(x for x in checks['activityChecks'] if x['case']==case['id'])
 results.append({'case':case['id'],'input':(fixtures/case['bundle']).relative_to(root).as_posix(),'artifacts':outputs,'activityCheckPass':activity['pass']})
(root/'tests/results/native-fixture-manifest.json').write_text(json.dumps({'producer':'Native Library evaluate and PlanDefinition apply over unchanged original diagnostic bundles','notCelGeneratedInput':True,'cases':results},indent=2)+'\n',encoding='utf-8')
print('Materialized unchanged native outputs for',len(results),'original fixtures.')
