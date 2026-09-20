"""Complete generated STEADI responses as a client, invoke native $extract, compare raw outputs."""
import argparse,copy,hashlib,json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--classpath',required=True)
p.add_argument('--java',default='java')
a=p.parse_args()
run=root/'tests/verification/extraction'
run.mkdir(parents=True,exist_ok=True)
source=root/'src/source/challenge/test-bundles/cases'
manifest=json.loads((root/'tests/results/questionnaire-manifest-mv.json').read_text())
fixture={'Younger Than 65':'younger-than-65','Eligible All No':'eligible-all-no','Eligible Unsteady Yes':'eligible-unsteady-yes','Eligible Prior Fall Yes':'eligible-prior-fall-yes','Eligible Incomplete Response':'eligible-incomplete-response','Eligible No Response':'eligible-no-response'}
profiles={'unsteady':'steadi-unsteady','worries-about-falling':'steadi-worries-about-falling','fallen-in-past-year':'steadi-fallen-in-past-year'}
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def artifact(case,kind):return root/next(x['path'] for x in case['artifacts'] if x['resourceType']==kind)
allno=next(c for c in manifest['cases'] if c['caseName']=='Eligible All No')
records=[]
for case in manifest['cases']:
 name=fixture[case['caseName']];oracle=read(source/name/'assertions.json')['sdcExtraction']
 record={'case':name,'invocationExpected':oracle['invocationExpected'],'invoked':False,'scope':'supplemental generated-form reuse; not an apply-produced QR' if name=='younger-than-65' else 'generated-output check'}
 if not oracle['invocationExpected']:
  record['reason']='Client does not submit incomplete or absent responses to baseline extraction.'
  write(run/name/'operation.json',record);records.append(record);continue
 directory=run/name
 template=allno if name=='younger-than-65' else case
 qpath=artifact(template,'Questionnaire');qrpath=artifact(template,'QuestionnaireResponse')
 q=read(qpath);qr=read(qrpath)
 subject='Patient/'+case['compartmentDir'].split('/')[-1]
 bundle=read(source/name/'bundle.json')
 supplied=next(e['resource'] for e in bundle['entry'] if e['resource']['resourceType']=='QuestionnaireResponse')
 if name=='younger-than-65':
  qr['id']='steadi-younger-client-response';qr['subject']={'reference':subject}
  record['templateReason']='Age-gated apply emitted no Questionnaire. Client reuses the unchanged generated eligible-all-no Questionnaire for the age-independent extraction test, with the younger case all-false answers.'
 for key in ['authored','encounter']:qr[key]=copy.deepcopy(supplied[key])
 qr['author']={'reference':subject};qr['status']='completed'
 # Completion and launch metadata are client actions, not edits to generated definitions or saved producer Q/QR.
 answers=[x['answer'][0]['valueBoolean'] for x in walk(qr) if 'answer' in x]
 assert len(answers)==3 and all(type(x) is bool for x in answers)
 patient=read(next((root/'tests/data/fhir'/case['compartmentDir']/'patient').glob('*.json')))
 encounter=copy.deepcopy(next(e['resource'] for e in bundle['entry'] if e['resource']['resourceType']=='Encounter'))
 encounter['subject']={'reference':subject}
 context={'resourceType':'Bundle','type':'collection','entry':[{'resource':patient},{'resource':encounter}]}
 write(directory/'questionnaire.json',q);write(directory/'client-response.json',qr);write(directory/'context.json',context)
 record.update({'invoked':True,'questionnaireSource':qpath.relative_to(root).as_posix(),'questionnaireSourceSha256':hashlib.sha256(qpath.read_bytes()).hexdigest(),'responseTemplate':qrpath.relative_to(root).as_posix(),'clientChanges':['status completed','authored and encounter from supplied context','author is synthetic patient']})
 write(directory/'operation.json',record);records.append(record)
command=[a.java,'-Xmx1024m','--class-path',a.classpath,str(root/'reports/tools/ExtractDemo.java'),str(root)]
result=subprocess.run(command,capture_output=True,text=True,timeout=120)
(run/'engine.log').write_text(result.stdout+'\n'+result.stderr)
if result.returncode:raise RuntimeError('Native extraction failed: '+result.stderr[-3000:])
print(result.stdout)
for record in records:
 if not record['invoked']:continue
 name=record['case'];directory=run/name;qr=read(directory/'client-response.json')
 output=read(directory/'extraction-raw.json');obs=[e['resource'] for e in output.get('entry',[]) if e.get('resource',{}).get('resourceType')=='Observation']
 errors=[i for x in walk(output) if x.get('resourceType')=='OperationOutcome' for i in x.get('issue',[]) if i.get('severity') in ['error','fatal']]
 expected=read(source/name/'assertions.json')['sdcExtraction']['expectedObservations']
 checks=[{'field':'observationCount','pass':len(obs)==3,'actual':len(obs)},{'field':'engineErrors','pass':not errors,'actual':errors}]
 for e in expected:
  suffix=profiles[e['linkId']]
  matches=[o for o in obs if any(x.split('|')[0].endswith('/'+suffix) for x in o.get('meta',{}).get('profile',[]))]
  checks.append({'question':e['linkId'],'field':'oneAssociatedObservation','pass':len(matches)==1,'actual':len(matches)})
  if len(matches)!=1:continue
  o=matches[0]
  fields={'valueBoolean':(o.get('valueBoolean'),e['valueBoolean']),'status':(o.get('status'),'final'),'subject':(o.get('subject',{}).get('reference'),qr['subject']['reference']),'effectiveDateTime':(o.get('effectiveDateTime'),qr['authored']),'encounter':(o.get('encounter',{}).get('reference'),qr['encounter']['reference'])}
  for field,(actual,wanted) in fields.items():checks.append({'question':e['linkId'],'field':field,'expected':wanted,'actual':actual,'pass':actual==wanted})
  for field,actual,wanted in [('code',o.get('code',{}).get('coding',[]),{k:e['code'][k] for k in ['system','code']}),('category',[c for cat in o.get('category',[]) for c in cat.get('coding',[])],{'system':'http://terminology.hl7.org/CodeSystem/observation-category','code':'survey'})]:
   checks.append({'question':e['linkId'],'field':field,'expected':wanted,'actual':actual,'pass':any(all(c.get(k)==v for k,v in wanted.items()) for c in actual)})
  checks.append({'question':e['linkId'],'field':'authorToPerformer','expected':qr['author'],'actual':o.get('performer',[]),'pass':qr['author'] in o.get('performer',[])})
  expected_ref='QuestionnaireResponse/'+qr['id']
  checks.append({'question':e['linkId'],'field':'derivedFrom','expected':expected_ref,'actual':o.get('derivedFrom',[]),'pass':any(x.get('reference')==expected_ref for x in o.get('derivedFrom',[]))})
 record['checks']=checks;record['pass']=all(c['pass'] for c in checks)
summary={'scope':'Generated Q plus client-completed QR extraction; incoming challenge QR ingestion is not required by this check.','runtime':'cqf-fhir-cr-cli-4.7-crl-4aee6041','records':records,'allContractFieldsPass':all(r.get('pass',True) for r in records),'engineOutputRepaired':False,'primaryCompletedResponses':3,'primaryFinalObservationCounts':[next(c['actual'] for c in x['checks'] if c['field']=='observationCount') for x in records if x['invoked'] and x['case']!='younger-than-65'],'youngerCase':'Supplemental extraction check only; age-gated apply correctly did not generate a Questionnaire.'}
write(run/'verification.json',summary)
print(json.dumps({'invoked':sum(r['invoked'] for r in records),'allContractFieldsPass':summary['allContractFieldsPass'],'failedFields':sorted({c['field'] for r in records for c in r.get('checks',[]) if not c['pass']})},indent=2))
