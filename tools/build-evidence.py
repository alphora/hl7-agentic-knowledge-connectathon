"""Build the required descriptive R4 evidence companions; no executable rules are added."""
import json, html, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'input/evidence.json').read_text(encoding='utf-8'))
BASE=json.loads((ROOT/'package.json').read_text())['crl']['canonicalBase']
REV=json.loads((ROOT/'docs/intake.json').read_text())['revision']
TRACK='https://github.com/reason-healthcare/hl7-agentic-knowledge-connectathon/blob/'+REV+'/use-cases/steadi/README.md'
OUT=ROOT/'generated/companions'
def write(resource):
    p=OUT/resource['resourceType']/(resource['id']+'.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(resource,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def citation(key):
    if key=='track':
        return {'type':'derived-from','display':'STEADI track scope and executable contract','document':{'url':TRACK}}
    src=DATA['sources'][key]
    actual=ROOT/'.cache/challenge'/src['path']
    assert hashlib.sha256(actual.read_bytes()).hexdigest()==src['sha256']
    return {'type':'citation','display':'; '.join(src['locators']),
        'citation':'Supplied snapshot SHA-256 '+src['sha256'],
        'document':{'url':src['url'],'contentType':'text/html'}}
def base(kind,item):
    return {'resourceType':kind,'id':item['id'],'url':BASE+'/'+kind+'/'+item['id'],
        'version':DATA['version'],'status':'draft','title':item['title'],
        'date':DATA['date'],'publisher':'Alphora'}
for item in DATA['variables']:
    r=base('EvidenceVariable',item)
    r.update(description=item['description'],
        characteristic=[{'description':item['title'],'definitionCodeableConcept':{'text':item['description']}}],
        relatedArtifact=[citation(item['source'])],
        text={'status':'generated','div':'<div xmlns="http://www.w3.org/1999/xhtml"><p>'+html.escape(item['description'])+'</p></div>'})
    write(r)
ids={x['id'] for x in DATA['variables']}
for item in DATA['evidence']:
    for role in ['population','intervention','comparator','outcome']: assert item[role] in ids
    r=base('Evidence',item)
    roles=f"Intervention: {item['intervention']}. Comparator: {item['comparator']}. Outcome: {item['outcome']}."
    paragraphs=[roles,item['finding'],'Recommendation grade '+item['grade']+': '+item['recommendation'],item['netBenefit'],'Harms: '+item['harms'],'Limitations: '+item['limitations']]
    r.update(description='\n\n'.join(paragraphs),
        exposureBackground={'reference':'EvidenceVariable/'+item['population'],'display':'Population: '+item['population']},
        exposureVariant=[{'reference':'EvidenceVariable/'+item['intervention'],'display':'Intervention'},{'reference':'EvidenceVariable/'+item['comparator'],'display':'Comparator'}],
        outcome=[{'reference':'EvidenceVariable/'+item['outcome'],'display':'Incident fall rate'}],
        relatedArtifact=[citation('recommendation'),citation('evidenceUpdate')],
        note=[{'text':'Descriptive FHIR R4 evidence. Numerical findings are attributed narrative, not computable R5 statistic elements. Array order does not encode comparator direction. Guidance linkage to the final CRL-generated artifacts remains pending.'}],
        text={'status':'generated','div':'<div xmlns="http://www.w3.org/1999/xhtml">'+''.join('<p>'+html.escape(p)+'</p>' for p in paragraphs)+'</div>'})
    write(r)
print(json.dumps({'Evidence':len(DATA['evidence']),'EvidenceVariable':len(DATA['variables']),'sourceHashesVerified':True}))
