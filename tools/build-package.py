"""Build a deterministic FHIR R4 NPM package and PUT knowledge transaction."""
from pathlib import Path
import gzip,hashlib,io,json,tarfile,uuid
ROOT=Path(__file__).resolve().parents[1]
report_path=ROOT/'verification/package.json';report_path.parent.mkdir(parents=True,exist_ok=True)
run_id=str(uuid.uuid4())
report_path.write_text(json.dumps({'status':'incomplete','runId':run_id})+'\n',encoding='utf-8')
try:
 def encode(value):return (json.dumps(value,indent=2)+'\n').encode()
 def save(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encode(value))
 meta=json.loads((ROOT/'package.json').read_bytes());BASE=meta['crl']['canonicalBase'];VERSION=meta['version']
 deps={'hl7.fhir.r4.core':'4.0.1','hl7.fhir.uv.sdc':'4.0.0','hl7.fhir.uv.cpg':'2.0.0'}
 resources=[]
 for folder in ('input/fhir','generated/companions'):
  for p in sorted((ROOT/folder).rglob('*.json')):
   r=json.loads(p.read_bytes())
   if r['resourceType']!='ImplementationGuide':resources.append((p,r))
 ig={'resourceType':'ImplementationGuide','id':'alphora-steadi','url':BASE+'/ImplementationGuide/alphora-steadi','version':VERSION,'name':'AlphoraSteadi','title':'Alphora STEADI Connectathon','status':'draft','experimental':True,'date':meta['crl']['date'],'publisher':'Alphora','description':'Synthetic requirement-bounded STEADI assessment, guidance, evidence and completion measure. Direct-authored CQL/FHIR; not clinically approved.','packageId':'org.alphora.steadi','license':'MIT','fhirVersion':['4.0.1'],'dependsOn':[{'uri':'http://hl7.org/fhir/uv/sdc/ImplementationGuide/hl7.fhir.uv.sdc','packageId':'hl7.fhir.uv.sdc','version':'4.0.0'},{'uri':'http://hl7.org/fhir/uv/cpg/ImplementationGuide/hl7.fhir.uv.cpg','packageId':'hl7.fhir.uv.cpg','version':'2.0.0'}],'definition':{'resource':[{'reference':{'reference':r['resourceType']+'/'+r['id']},'name':r.get('title',r.get('name',r['id'])),'exampleBoolean':False} for _,r in resources]}}
 p=ROOT/'input/fhir/ImplementationGuide/alphora-steadi.json';save(p,ig);resources.append((p,ig))
 identities=[(r['resourceType'],r['id']) for _,r in resources];assert len(set(identities))==len(resources),'Duplicate type/id'
 canonicals={r['url']+'|'+r['version'] for _,r in resources if 'url' in r};assert len(canonicals)==len(resources),'Missing/duplicate canonical version'
 # Local canonical references, including evidence links, must resolve exactly.
 references=[]
 def walk(value):
  if isinstance(value,dict):
   for key,item in value.items():
    if key in ('url','system'):continue
    walk(item)
  elif isinstance(value,list):
   for item in value:walk(item)
  elif isinstance(value,str) and value.startswith(BASE+'/'):
   assert value in canonicals,'Unresolved local canonical '+value
   references.append(value)
 for _,r in resources:walk(r)
 files={}
 index=[]
 for p,r in resources:
  name=r['resourceType']+'-'+r['id']+'.json';files['package/'+name]=p.read_bytes()
  index.append({'filename':name,'resourceType':r['resourceType'],'id':r['id'],'url':r['url'],'version':r['version']})
 files['package/.index.json']=encode({'index-version':2,'files':index})
 files['package/package.json']=encode({'name':'org.alphora.steadi','version':VERSION,'type':'IG','date':'20260919000000','license':'MIT','canonical':BASE,'url':'https://github.com/alphora/hl7-agentic-knowledge-connectathon','title':'Alphora STEADI Connectathon','description':'Direct-authored synthetic STEADI challenge artifacts','fhirVersions':['4.0.1'],'dependencies':deps,'author':'Alphora'})
 for folder,suffix in [('input/cql','cql'),('generated/elm','json')]:
  for p in sorted((ROOT/folder).glob('*.'+suffix)):files['package/'+p.name]=p.read_bytes()
 files['package/LICENSE']= (ROOT/'LICENSE').read_bytes();files['package/upstream-MIT.txt']=(ROOT/'licenses/upstream-MIT.txt').read_bytes()
 # Bundle is a submission convenience; resources retain their original identities/canonicals.
 transaction={'resourceType':'Bundle','id':'alphora-steadi-knowledge','type':'transaction','entry':[{'resource':r,'request':{'method':'PUT','url':r['resourceType']+'/'+r['id']}} for _,r in resources]}
 save(ROOT/'dist/knowledge-transaction.json',transaction)
 final_archive=ROOT/'dist'/('org.alphora.steadi-'+VERSION+'.tgz');final_archive.parent.mkdir(exist_ok=True)
 archive=final_archive.with_name(final_archive.name+'.'+str(uuid.uuid4())+'.tmp')
 with archive.open('wb') as stream:
  with gzip.GzipFile(filename='',fileobj=stream,mode='wb',mtime=0) as zipped:
   with tarfile.open(fileobj=zipped,mode='w') as tar:
    for name,data in sorted(files.items()):
     info=tarfile.TarInfo(name);info.size=len(data);info.mtime=0;info.mode=0o644;tar.addfile(info,io.BytesIO(data))
 with tarfile.open(archive,'r:gz') as tar:
  assert sorted(tar.getnames())==sorted(files)
  for name,data in files.items():assert tar.extractfile(name).read()==data
 archive.replace(final_archive);archive=final_archive
 report={'runId':run_id,'status':'passed','package':archive.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'resources':len(resources),'resolvedLocalCanonicalReferences':len(references),'dependencies':deps,'files':{n:hashlib.sha256(b).hexdigest() for n,b in sorted(files.items())},'limits':['Structural inventory/reference/package checks only; full profile/terminology validation remains separate','Not published to a package registry']}
 save(ROOT/'verification/package.json',report);print(json.dumps({k:report[k] for k in ('status','resources','sha256')}))
except BaseException as error:
 report_path.write_text(json.dumps({'status':'failed','runId':run_id,'error':str(error)},indent=2)+'\n',encoding='utf-8')
 raise
finally:
 if 'archive' in globals() and archive.name.endswith('.tmp') and archive.exists():archive.unlink()
