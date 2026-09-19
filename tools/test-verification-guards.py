"""Regression controls for incomplete inventories and stale verification results."""
import copy,json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from fixture_contract import CASE_IDS,EXPRESSIONS,PREFIX,validate_inventory,validate_assertions
ROOT=Path(__file__).resolve().parents[1]
class ContractTests(unittest.TestCase):
 def setUp(self):
  self.rows=[{'path':PREFIX+c+'/'+n} for c in CASE_IDS for n in ('assertions.json','bundle.json')]
  self.oracle={'fixtureId':CASE_IDS[0],'assertions':[{'expression':e,'expected':{'value':True}} for e in EXPRESSIONS]}
 def test_valid_contract(self):validate_inventory(self.rows);validate_assertions(self.oracle,CASE_IDS[0])
 def test_empty_inventory(self):
  with self.assertRaises(AssertionError):validate_inventory([])
 def test_missing_case(self):
  with self.assertRaises(AssertionError):validate_inventory(self.rows[2:])
 def test_missing_assertion(self):
  self.oracle['assertions'].pop()
  with self.assertRaises(AssertionError):validate_assertions(self.oracle,CASE_IDS[0])
 def test_duplicate_assertion(self):
  self.oracle['assertions'].append(copy.deepcopy(self.oracle['assertions'][0]))
  with self.assertRaises(AssertionError):validate_assertions(self.oracle,CASE_IDS[0])
 def test_javascript_contract(self):
  script="""import assert from 'node:assert/strict';
import {caseIds,expressions,prefix,validateInventory,validateAssertions,verifyBytes} from './tools/fixture-contract.mjs';
const files=caseIds.flatMap(id=>['assertions.json','bundle.json'].map(name=>({path:prefix+id+'/'+name})));
const oracle={fixtureId:caseIds[0],assertions:expressions.map(expression=>({expression,expected:{value:true}}))};
validateInventory(files);validateAssertions(oracle,caseIds[0]);
assert.throws(()=>validateInventory([]));assert.throws(()=>validateInventory(files.slice(2)));
assert.throws(()=>validateAssertions({...oracle,assertions:oracle.assertions.slice(1)},caseIds[0]));
assert.throws(()=>validateAssertions({...oracle,assertions:[...oracle.assertions,oracle.assertions[0]]},caseIds[0]));
assert.throws(()=>verifyBytes(Buffer.from('changed'),{path:'test',sha256:'bad'}));
"""
  subprocess.run(['node','--input-type=module','-e',script],cwd=ROOT,check=True,capture_output=True)
 def run_failure(self,kind):
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp);(target/'tools').mkdir();(target/'verification/measure-native').mkdir(parents=True)
   for name in ('verify-measure-native.py','fixture_contract.py','validate-companions.py'):shutil.copyfile(ROOT/'tools'/name,target/'tools'/name)
   if kind in ('missing-jar','invalid-jar'):
    result=target/'verification/measure-native/summary.json';script='verify-measure-native.py';args=['--jar',str(target/'bad.jar')]
    if kind=='invalid-jar':(target/'bad.jar').write_bytes(b'not qualified')
   else:
    result=target/'verification/fhir-json-structure.json';script='validate-companions.py';args=[]
    if kind=='malformed-resource':
     (target/'.cache/fhir-schema').mkdir(parents=True);(target/'input/fhir').mkdir(parents=True)
     (target/'.cache/fhir-schema/fhir.schema.json').write_text('{}')
     (target/'verification/measure-native/summary.json').write_text(json.dumps({'status':'passed','cases':[{}]*6}))
     (target/'input/fhir/malformed.json').write_text('{not json')
   result.write_text(json.dumps({'status':'passed','runId':'old'}))
   env={**os.environ,'PYTHONPATH':str(ROOT/'.cache/python')}
   run=subprocess.run([sys.executable,str(target/'tools'/script),*args],capture_output=True,env=env)
   self.assertNotEqual(run.returncode,0)
   report=json.loads(result.read_text());self.assertEqual(report['status'],'failed');self.assertNotEqual(report['runId'],'old')
   if kind=='malformed-resource':self.assertIn('property name',report['error'])
 def test_missing_jar_invalidates_pass(self):self.run_failure('missing-jar')
 def test_invalid_jar_invalidates_pass(self):self.run_failure('invalid-jar')
 def test_missing_schema_invalidates_pass(self):self.run_failure('missing-schema')
 def test_malformed_resource_invalidates_pass(self):self.run_failure('malformed-resource')
if __name__=='__main__':unittest.main(verbosity=2)
