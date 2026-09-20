"""Build directly authored FHIR guidance, with explicit outgoing evidence links."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
meta=json.loads((ROOT/'package.json').read_text());BASE=meta['crl']['canonicalBase'];VERSION=meta['version']
def save(resource):
 p=ROOT/'input/fhir'/resource['resourceType']/(resource['id']+'.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(resource,indent=2)+'\n',encoding='utf-8')
def common(kind,id,title):
 return dict(resourceType=kind,id=id,url=BASE+'/'+kind+'/'+id,version=VERSION,name=''.join(w.title() for w in id.split('-')),title=title,status='draft',experimental=True,date=meta['crl']['date'],publisher='Alphora')
plan=common('PlanDefinition','steadi-screening-guidance','STEADI screening and prevention guidance')
plan.update(description='Direct-authored STEADI challenge guidance. Applicability is evaluated from the supplied, coherent QuestionnaireResponse; this does not order an intervention.',type={'coding':[{'system':'http://terminology.hl7.org/CodeSystem/plan-definition-type','code':'workflow-definition'}]},library=[BASE+'/Library/Steadi|'+VERSION],relatedArtifact=[],action=[])
rows=[
 ('exercise-guidance','Exercise Intervention Applicable','Exercise fall-prevention guidance','exercise-fall-rate','Exercise interventions are recommended for community-dwelling adults aged 65 years or older at increased fall risk (USPSTF grade B). This guidance does not select or order a particular intervention.'),
 ('multifactorial-guidance','Consider Multifactorial Intervention','Individualized multifactorial consideration','multifactorial-fall-rate','Individualize whether to offer multifactorial fall-prevention interventions for community-dwelling adults aged 65 years or older at increased fall risk, considering prior falls, comorbidities and patient preferences (USPSTF grade C). This is not a routine intervention order.')]
for id,expression,title,evidence,message in rows:
 link={'type':'justification','resource':BASE+'/Evidence/'+evidence+'|'+VERSION}
 action=common('ActivityDefinition',id,title)
 action.update(library=[BASE+'/Library/Steadi|'+VERSION],description=message,kind='CommunicationRequest',intent='proposal',code={'coding':[{'system':'http://hl7.org/fhir/uv/cpg/CodeSystem/cpg-activity-type-cs','code':'send-message'}]},relatedArtifact=[link],dynamicValue=[{'path':'payload.contentString','expression':{'language':'text/cql','expression':title+' Message'}}])
 save(action);plan['relatedArtifact'].append(link)
 plan['action'].append({'id':id,'title':title,'documentation':[link],'condition':[{'kind':'applicability','expression':{'language':'text/cql','expression':expression}}],'definitionCanonical':action['url']+'|'+VERSION})
save(plan)
print('Authored PlanDefinition and two CommunicationRequest ActivityDefinitions.')
