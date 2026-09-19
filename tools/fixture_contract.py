import hashlib,json
CASE_IDS=('eligible-all-no','eligible-incomplete-response','eligible-no-response','eligible-prior-fall-yes','eligible-unsteady-yes','younger-than-65')
EXPRESSIONS={'Initial Population','Denominator','Numerator'}
PREFIX='use-cases/steadi/test-bundles/cases/'
def validate_inventory(files):
 actual=sorted(r['path'] for r in files if r['path'].startswith(PREFIX) and r['path'].endswith('/assertions.json'))
 assert actual==sorted(PREFIX+c+'/assertions.json' for c in CASE_IDS),'Exact six fixture identities required'
 for case in CASE_IDS:
  for name in ('assertions.json','bundle.json'):
   assert sum(r['path']==PREFIX+case+'/'+name for r in files)==1,'Exactly one inventoried input required'
def validate_assertions(oracle,case):
 assert oracle['fixtureId']==case,'Fixture identity mismatch'
 selected=[a for a in oracle['assertions'] if a['expression'] in EXPRESSIONS]
 assert sorted(a['expression'] for a in selected)==sorted(EXPRESSIONS),'Three distinct measure expressions required'
 assert all(type(a['expected']['value']) is bool for a in selected),'Boolean oracle required'
 return selected
def load_fixtures(root):
 files=json.loads((root/'docs/intake.json').read_text())['files'];validate_inventory(files)
 result=[]
 for case in CASE_IDS:
  for name in ('assertions.json','bundle.json'):
   rel=PREFIX+case+'/'+name;row=next(r for r in files if r['path']==rel)
   assert hashlib.sha256((root/'.cache/challenge'/rel).read_bytes()).hexdigest()==row['sha256'],'Fixture hash mismatch: '+rel
  path=root/'.cache/challenge'/PREFIX/case/'assertions.json'
  validate_assertions(json.loads(path.read_text()),case);result.append(path)
 return result
