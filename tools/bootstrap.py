"""Retrieve only pinned supplied inputs and technical dependencies; no clinical crawling."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
arg=argparse.ArgumentParser();arg.add_argument('--engine-jar',required=True,type=Path);args=arg.parse_args()
toolchain=json.loads((ROOT/'docs/toolchain.json').read_text())
inventory=json.loads((ROOT/'docs/intake.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
def obtain(url,target,expected):
 if target.exists():
  data=target.read_bytes()
 else:
  request=urllib.request.Request(url,headers={'User-Agent':'Alphora-STEADI-pinned-build/0.1'})
  with urllib.request.urlopen(request,timeout=60) as response:data=response.read()
 assert sha(data)==expected,'Digest mismatch: '+str(target)
 if not target.exists():
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 return data
cache=ROOT/'.cache/challenge'
for item in inventory['files']:
 rel=PurePosixPath(item['path'])
 assert not rel.is_absolute() and '..' not in rel.parts and ':' not in item['path']
 data=obtain('https://raw.githubusercontent.com/reason-healthcare/hl7-agentic-knowledge-connectathon/'+inventory['revision']+'/'+str(rel),cache.joinpath(*rel.parts),item['sha256'])
 assert len(data)==item['bytes']
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['gitBlobSha']
assert sha(args.engine_jar.read_bytes())==toolchain['engine']['sha256'],'Unqualified engine'
with zipfile.ZipFile(args.engine_jar) as jar:
 with zipfile.ZipFile(io.BytesIO(jar.read(toolchain['engine']['quickMember']))) as quick:
  for name,model in toolchain['engine']['models'].items():
   data=quick.read(model['member']);assert sha(data)==model['sha256']
   target=ROOT/'.cache/preflight/models'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
schema=toolchain['fhirSchema'];target=ROOT/'.cache/fhir-schema/fhir.schema.json'
if target.exists():assert sha(target.read_bytes())==schema['schemaSha256']
else:
 with urllib.request.urlopen(schema['url'],timeout=60) as response:data=response.read()
 assert sha(data)==schema['archiveSha256']
 with zipfile.ZipFile(io.BytesIO(data)) as archive:data=archive.read('fhir.schema.json')
 assert sha(data)==schema['schemaSha256']
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
target.with_name('origin.json').write_text(json.dumps(schema,indent=2)+'\n')
print('Verified '+str(len(inventory['files']))+' supplied inputs, pinned model/helpers and official R4 schema.')
