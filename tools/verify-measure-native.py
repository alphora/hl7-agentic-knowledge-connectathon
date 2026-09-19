"""Execute the authored Measure with the pinned native engine and unchanged fixtures."""
import argparse,hashlib,json,subprocess,tempfile,datetime,uuid
from pathlib import Path
from fixture_contract import load_fixtures,validate_assertions
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/measure-native';OUT.mkdir(parents=True,exist_ok=True)
def save(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
summary={'status':'incomplete','runId':str(uuid.uuid4()),'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timezone':'UTC','cases':[],'limits':['Synthetic track context; no general clinical deployment qualification','Independent participant interoperability testing remains pending']}
save(OUT/'summary.json',summary)
try:
 parser=argparse.ArgumentParser();parser.add_argument('--jar',required=True,type=Path);args=parser.parse_args()
 digest=hashlib.sha256(args.jar.read_bytes()).hexdigest()
 assert digest=='9870fc867547f65518c5cd6e698ace77b60a9e98797ed38330c25d06cbf5cb2e','Unqualified engine'
 summary['engineSha256']=digest
 fixtures=load_fixtures(ROOT)
 measure=json.loads((ROOT/'input/fhir/Measure/steadi-screening-completion.json').read_text())
 lib=json.loads((ROOT/'generated/companions/Library/SteadiMeasure.json').read_text())
 summary['inputs']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['input/cql/SteadiMeasure.cql','input/fhir/Measure/steadi-screening-completion.json','generated/companions/Library/SteadiMeasure.json']}
 with tempfile.TemporaryDirectory(prefix='measure-run-',dir=ROOT/'.cache') as temp:
  work=Path(temp)
  resources=[measure,lib,json.loads((ROOT/'input/fhir/Questionnaire/steadi-three-question-screen.json').read_text())]

  for fixture in fixtures:
   resources += [e['resource'] for e in json.loads(fixture.with_name('bundle.json').read_text())['entry']]
  for r in resources:
   p=work/'src/fhir'/r['resourceType']/(r['id']+'.json');p.parent.mkdir(parents=True,exist_ok=True);save(p,r)
  for fixture in fixtures:
   oracle=json.loads(fixture.read_text());case=oracle['fixtureId'];context=oracle['evaluationContext'];mp=context['measurementPeriod']
   reports=work/'reports'/case;reports.mkdir(parents=True)
   cmd=['java','-Duser.timezone=UTC','-jar',str(args.jar),'measure','-source='+str(ROOT/'input/cql'),'-name=SteadiMeasure','-root='+str(work),'-data='+str(work),'-fv=R4','-c=Patient','-cv='+context['patientId'],'--measure=steadi-screening-completion','--period-start='+mp['start'][:10],'--period-end='+mp['end'][:10],'--apply-scoring=true','--report-path='+str(reports)]
   run=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',timeout=120)
   (OUT/(case+'.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
   row={'fixtureId':case,'exitCode':run.returncode,'passed':False}
   summary['cases'].append(row);save(OUT/'summary.json',summary)
   assert run.returncode==0,run.stderr
   found=[json.loads(p.read_text(encoding='utf-8-sig')) for p in reports.rglob('*.json')]
   found=[r for r in found if r.get('resourceType')=='MeasureReport']
   assert len(found)==1,case+' requires exactly one MeasureReport'
   report=found[0];save(OUT/(case+'.json'),report)
   assert report['status']=='complete' and report['type']=='individual'
   assert report['subject']['reference']=='Patient/'+context['patientId']
   assert report['measure']==measure['url']+'|'+measure['version']
   def instant(value): return datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
   assert instant(report['period']['start'])==instant(mp['start'])
   assert instant(report['period']['end'])==instant(mp['end'])
   assert len(report['group'])==1,'Exactly one population group required'
   populations=report['group'][0]['population']
   assert len(populations)==3,'Exactly three populations required'
   actual={p['code']['coding'][0]['code']:p['count'] for p in populations}
   labels={'Initial Population':'initial-population','Denominator':'denominator','Numerator':'numerator'}
   expected={labels[a['expression']]:int(a['expected']['value']) for a in validate_assertions(oracle,case)}
   assert actual==expected,(case,actual,expected)
   score=report['group'][0].get('measureScore',{}).get('value')
   if expected['denominator']:
    assert score==expected['numerator']/expected['denominator'],('Unexpected measure score',score)
   else:
    assert score is None,'No score expected for zero denominator'
   row.update(actual=actual,expected=expected,measureScore=score,passed=True)
   save(OUT/'summary.json',summary)
   print(case+': '+str(actual),flush=True)
 summary['status']='passed'
 save(OUT/'summary.json',summary)
 print('Native MeasureReports passed for all six supplied fixtures.',flush=True)
except BaseException as error:
 summary.update(status='failed',error=str(error));save(OUT/'summary.json',summary);raise
