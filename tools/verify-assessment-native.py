"""Native CQL/extract/apply checks against immutable fixtures and explicit controls."""
from pathlib import Path
import argparse,copy,datetime,hashlib,importlib.util,json,subprocess,uuid
from fixture_contract import load_fixtures
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/assessment-native';OUT.mkdir(parents=True,exist_ok=True)
NAMES=['In Screening Population','Completed Three Question Screen','At Increased Fall Risk','Exercise Intervention Applicable','Consider Multifactorial Intervention','Initial Population','Denominator','Numerator']
def read(p):return json.loads(p.read_bytes())
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def require(test,message):
 if not test:raise AssertionError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resources(bundle,kind):return [e['resource'] for e in bundle.get('entry',[]) if e['resource']['resourceType']==kind]
def instant(v):return datetime.datetime.fromisoformat(v.replace('Z','+00:00')).isoformat()
def observation(r):
 return {'status':r['status'],'category':r['category'],'code':r['code'],'subject':r['subject'],'encounter':r['encounter'],'effectiveDateTime':instant(r['effectiveDateTime']),'issued':instant(r['issued']),'performer':r['performer'],'valueBoolean':r['valueBoolean'],'derivedFrom':r['derivedFrom'],'security':r.get('meta',{}).get('security',[])}
def obs_set(bundle):return sorted([observation(r) for r in resources(bundle,'Observation')],key=lambda r:json.dumps(r['code'],sort_keys=True))
def params(enc,period,qr=None,context=True):
 entries=[{'name':'Encounter Id','valueString':enc},{'name':'Track Context Confirmed','valueBoolean':context},{'name':'Measurement Period','valuePeriod':{k:period[k] for k in ('start','end')}}]
 if qr:entries.append({'name':'Questionnaire Response Id','valueString':qr})
 return {'resourceType':'Parameters','parameter':entries}
summary={'status':'incomplete','runId':str(uuid.uuid4()),'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':[],'controls':[],'limits':['Direct authoring and explicit adapter; not CRL emission','Synthetic inputs only; not clinical approval','Not a second FHIR server round trip']}
save(OUT/'summary.json',summary)
try:
 parser=argparse.ArgumentParser();parser.add_argument('--jar',required=True,type=Path);args=parser.parse_args()
 spec=importlib.util.spec_from_file_location('native_runtime',ROOT/'tools/native-runtime.py');runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
 cp=runtime.prepare(args.jar);summary['engineSha256']=digest(args.jar)
 inputs=sorted((ROOT/'input/fhir').rglob('*.json'))+sorted((ROOT/'generated/companions').rglob('*.json'))
 inputs += [ROOT/'input/cql/Steadi.cql',ROOT/'input/cql/SteadiMeasure.cql',ROOT/'tools/java/SteadiNative.java',ROOT/'tools/native-runtime.py',Path(__file__)]
 summary['inputs']={p.relative_to(ROOT).as_posix():digest(p) for p in inputs}
 # Verify runtime libraries embed the current authored CQL and ELM bytes.
 import base64
 for name in ('Steadi','SteadiMeasure'):
  lib=read(ROOT/f'generated/companions/Library/{name}.json')
  for content_type,path in [('text/cql',ROOT/f'input/cql/{name}.cql'),('application/elm+json',ROOT/f'generated/elm/{name}.json')]:
   attachment=[c for c in lib['content'] if c['contentType']==content_type]
   require(len(attachment)==1 and base64.b64decode(attachment[0]['data'])==path.read_bytes(),'Stale library attachment: '+name)
 work=ROOT/'.cache/assessment-runs'/summary['runId'];work.mkdir(parents=True)
 knowledge={'resourceType':'Bundle','type':'collection','entry':[{'resource':read(p)} for p in inputs if '/fhir/' in p.as_posix() or '/companions/' in p.as_posix()]}
 save(work/'knowledge.json',knowledge)
 def run_case(name,bundle,period,expected,extracted=None,qr_id=None,error=False,context=True):
  case_dir=work/name;case_dir.mkdir()
  save(case_dir/'input.json',bundle)
  patient=resources(bundle,'Patient')[0]['id'];encounter=resources(bundle,'Encounter')[0]['id']
  save(case_dir/'parameters.json',params(encounter,period,qr_id,context))
  result=runtime.execute(cp,[work/'knowledge.json',case_dir/'input.json',case_dir/'parameters.json','Patient/'+patient,'Encounter/'+encounter,case_dir/'output'])
  (case_dir/'runtime.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
  row={'name':name,'inputSha256':digest(case_dir/'input.json'),'parameters':read(case_dir/'parameters.json'),'passed':False}
  if error:
   require(result.returncode!=0,'Expected duplicate-answer rejection')
   require('expected a list with at most one element' in (result.stdout+result.stderr).lower(),'Unexpected error instead of cardinality rejection')
   save(OUT/name/'input.json',bundle)
   save(OUT/name/'evaluation.json',read(case_dir/'output/evaluation.json'))
   row.update(passed=True,expected='cardinality error',exitCode=result.returncode);return row
  require(result.returncode==0,name+': '+result.stderr[-3000:])
  output=case_dir/'output';evaluation=read(output/'evaluation.json')
  actual={}
  for n in NAMES:
   items=[p for p in evaluation['parameter'] if p['name']==n]
   require(len(items)==1,name+': missing/duplicate result '+n)
   p=items[0];values=[k for k in p if k.startswith('value')]
   require(not values or values==['valueBoolean'],name+': non-Boolean value '+n)
   if not values:require(p.get('_valueBoolean',{}).get('extension')==[{'url':'http://hl7.org/fhir/StructureDefinition/data-absent-reason','valueCode':'unknown'}],name+': null must carry explicit unknown semantics')
   actual[n]=p.get('valueBoolean')
  require(actual==dict(zip(NAMES,expected)),str((name,actual,expected)))
  operations=read(output/'operations.json');require(operations['extractionInvoked'] is expected[1],name+': extraction invocation')
  if expected[1]:
   got=read(output/'extraction.json');require(len(got.get('entry',[]))==3,name+': extraction count')
   if extracted is not None:require(obs_set(got)==obs_set(extracted),name+': extracted resources differ from immutable oracle')
   selected=next(p['resource'] for p in evaluation['parameter'] if p['name']=='Assessment Response')
   answer_by_link={i['linkId']:i['answer'][0]['valueBoolean'] for i in selected['item']}
   question=resources(knowledge,'Questionnaire')[0]
   expected_answers={i['code'][0]['code']:answer_by_link[i['linkId']] for i in question['item']}
   require({o['code']['coding'][0]['code']:o['valueBoolean'] for o in resources(got,'Observation')}==expected_answers,name+': extraction must reflect selected response')
   for entry in got['entry']:require(entry['request']=={'method':'PUT','url':'Observation/'+entry['resource']['id']},name+': invalid transaction')
  else:require(not (output/'extraction.json').exists(),name+': no extraction for incomplete response')
  applied=read(output/'apply.json');returns=[p['resource'] for p in applied['parameter'] if p['name']=='return']
  require(len(returns)==1 and returns[0]['resourceType']=='Bundle',name+': expected one application Bundle')
  result_bundle=returns[0];communications=resources(result_bundle,'CommunicationRequest');groups=resources(result_bundle,'RequestGroup')
  expected_count=2 if expected[3] is True else 0
  require(len(communications)==expected_count,name+': guidance count')
  require(len(groups)==1,name+': RequestGroup count')
  require(groups[0]['intent']=='proposal',name+': guidance is a proposal')
  require(len(groups[0].get('action',[]))==expected_count,name+': action count')
  identities={r['resourceType']+'/'+r['id'] for r in resources(result_bundle,'CommunicationRequest')}
  expected_links={'exercise-guidance':('exercise-guidance-exercise-guidance','exercise-fall-rate'),'multifactorial-guidance':('multifactorial-guidance-multifactorial-guidance','multifactorial-fall-rate')}
  for action in groups[0].get('action',[]):
   require(action['id'] in expected_links,name+': unknown guidance action')
   target,evidence=expected_links[action['id']]
   require(action['resource']['reference']=='CommunicationRequest/'+target and action['resource']['reference'] in identities,name+': incorrect action target')
   require(action['documentation']==[{'type':'justification','resource':'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/Evidence/'+evidence+'|0.1.0'}],name+': incorrect evidence link')
  message_oracle={
   'exercise-guidance-exercise-guidance':'Exercise interventions are recommended for community-dwelling adults aged 65 years or older at increased fall risk (USPSTF grade B). This guidance does not select or order a particular intervention.',
   'multifactorial-guidance-multifactorial-guidance':'Individualize whether to offer multifactorial fall-prevention interventions for community-dwelling adults aged 65 years or older at increased fall risk, considering prior falls, comorbidities and patient preferences (USPSTF grade C). This is not a routine intervention order.'}
  if expected_count:require({r['id'] for r in communications}==set(message_oracle),name+': exact distinct guidance identities')
  for resource in communications:
   require(resource['subject']['reference']=='Patient/'+patient and resource['encounter']['reference']=='Encounter/'+encounter,name+': wrong guidance context')
   require(resource['status']=='active' and len(resource['payload'])==1 and resource['payload'][0]['contentString']==message_oracle[resource['id']],name+': missing guidance')
  # All raw and adapted outputs are retained with their hashes; logs stay in ignored cache.
  hashes={}
  for p in output.glob('*.json'):
   save(OUT/name/p.name,read(p));hashes[p.name]=digest(OUT/name/p.name)
  save(OUT/name/'input.json',bundle)
  row.update(passed=True,expressions=actual,extractionInvoked=expected[1],guidanceCount=len(communications),outputs=hashes)
  return row
 fixtures=load_fixtures(ROOT);inventory=read(ROOT/'docs/intake.json')['files']
 for fixture in fixtures:
  oracle=read(fixture);name=oracle['fixtureId'];bundle=read(fixture.with_name('bundle.json'))
  require(sorted(a['expression'] for a in oracle['assertions'])==sorted(NAMES),'Exact eight assertions required')
  expected=[next(a['expected']['value'] for a in oracle['assertions'] if a['expression']==n) for n in NAMES]
  source=fixture.with_name('extracted-bundle.json');rel=source.relative_to(ROOT/'.cache/challenge').as_posix()
  require(digest(source)==next(i['sha256'] for i in inventory if i['path']==rel),'Extraction oracle hash mismatch')
  row=run_case(name,bundle,oracle['evaluationContext']['measurementPeriod'],expected,read(source))
  summary['cases'].append(row);save(OUT/'summary.json',summary);print(name+': passed',flush=True)
 base=read(fixtures[0].with_name('bundle.json'));period=read(fixtures[0])['evaluationContext']['measurementPeriod']
 def control(name,bundle,expected,qr=None,error=False):
  summary['controls'].append(run_case(name,bundle,period,expected,qr_id=qr,error=error));save(OUT/'summary.json',summary);print(name+': passed',flush=True)
 positive=copy.deepcopy(base);resources(positive,'QuestionnaireResponse')[0]['item'][0]['answer'][0]['valueBoolean']=True
 control('answer-yes',positive,[True]*8)
 control('change-to-no',copy.deepcopy(base),[True,True,False,False,False,True,True,True])
 cleared=copy.deepcopy(positive);resources(cleared,'QuestionnaireResponse')[0]['item'][2].pop('answer')
 control('clear-answer',cleared,[True,False,None,None,None,True,True,False])
 control('restore-answer',positive,[True]*8)
 younger=copy.deepcopy(positive);resources(younger,'Patient')[0]['birthDate']='1976-01-01'
 control('younger-positive',younger,[False,True,True,False,False,False,False,False])
 nonamb=copy.deepcopy(positive);enc=resources(nonamb,'Encounter')[0];other=copy.deepcopy(enc);other['id']='other-ambulatory';enc['class']['code']='IMP';nonamb['entry'].append({'resource':other})
 control('selected-nonambulatory',nonamb,[False,True,True,False,False,True,True,False])
 birthday=copy.deepcopy(positive);resources(birthday,'Patient')[0]['birthDate']='1961-09-01';later=copy.deepcopy(resources(birthday,'Encounter')[0]);later['id']='after-birthday';later['period']['start']='2026-10-15T09:00:00Z';later['period']['end']='2026-10-15T10:00:00Z';birthday['entry'].append({'resource':later})
 control('age-at-selected-encounter',birthday,[False,True,True,False,False,True,True,False])
 mixed=copy.deepcopy(positive);qr=resources(mixed,'QuestionnaireResponse')[0];qr2=copy.deepcopy(qr);qr['item'][2].pop('answer');qr2['id']='other-partial';qr2['item'][0].pop('answer');mixed['entry'].append({'resource':qr2})
 control('do-not-pool-responses',mixed,[True,False,None,None,None,True,True,False],qr=qr['id'])
 foreign=copy.deepcopy(positive);resources(foreign,'QuestionnaireResponse')[0]['encounter']['reference']='Encounter/foreign'
 control('foreign-response-encounter',foreign,[True,False,None,None,None,True,True,False])
 wrongq=copy.deepcopy(positive);resources(wrongq,'QuestionnaireResponse')[0]['questionnaire']='https://example.org/Questionnaire/unrelated|1'
 control('unrecognized-questionnaire',wrongq,[True,False,None,None,None,True,True,False])
 duplicate=copy.deepcopy(positive);answer=resources(duplicate,'QuestionnaireResponse')[0]['item'][0]['answer'];answer.append(copy.deepcopy(answer[0]))
 control('duplicate-answer-error',duplicate,[],error=True)
 summary['controls'].append(run_case('context-false',positive,period,[False,True,True,False,False,False,False,False],context=False))
 summary['controls'].append(run_case('excluded-period',positive,{'start':'2025-01-01T00:00:00Z','end':'2025-12-31T23:59:59Z'},[False,False,None,False,False,False,False,False]))
 mismatch=work/'target-mismatch';mismatch.mkdir();save(mismatch/'input.json',positive)
 enc=resources(positive,'Encounter')[0]['id'];patient=resources(positive,'Patient')[0]['id'];save(mismatch/'parameters.json',params(enc,period))
 rejected=runtime.execute(cp,[work/'knowledge.json',mismatch/'input.json',mismatch/'parameters.json','Patient/'+patient,'Encounter/foreign-target',mismatch/'output'])
 require(rejected.returncode!=0 and 'Encounter parameter and guidance target must match' in rejected.stderr,'Reject inconsistent evaluation and guidance encounter')
 summary['controls'].append({'name':'guidance-target-mismatch','passed':True,'exitCode':rejected.returncode,'expected':'Encounter parameter and guidance target must match'})
 summary.update(status='passed',fixtureAssertions=48,completedAt=datetime.datetime.now(datetime.timezone.utc).isoformat());save(OUT/'summary.json',summary)
 print('Native assessment/extraction/apply: six fixtures and fourteen controls passed.',flush=True)
except BaseException as error:
 summary.update(status='failed',error=str(error));save(OUT/'summary.json',summary);raise
