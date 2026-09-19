import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
export const caseIds=['eligible-all-no','eligible-incomplete-response','eligible-no-response','eligible-prior-fall-yes','eligible-unsteady-yes','younger-than-65'];
export const expressions=['Denominator','Initial Population','Numerator'];
export const prefix='use-cases/steadi/test-bundles/cases/';
export function validateInventory(files){
 const actual=files.filter(f=>f.path.startsWith(prefix)&&f.path.endsWith('/assertions.json')).map(f=>f.path).sort();
 assert.deepEqual(actual,caseIds.map(id=>prefix+id+'/assertions.json').sort(),'Exact six fixture identities required');
 for(const id of caseIds) for(const name of ['assertions.json','bundle.json'])
  assert.equal(files.filter(f=>f.path===prefix+id+'/'+name).length,1,'Exactly one inventoried input required');
}
export function validateAssertions(oracle,id){
 assert.equal(oracle.fixtureId,id,'Fixture identity mismatch');
 const selected=oracle.assertions.filter(a=>expressions.includes(a.expression));
 assert.deepEqual(selected.map(a=>a.expression).sort(),expressions,'Three distinct measure expressions required');
 for(const a of selected) assert.equal(typeof a.expected.value,'boolean','Boolean oracle required');
 return selected;
}
export function verifyBytes(bytes,row){
 assert.equal(createHash('sha256').update(bytes).digest('hex'),row.sha256,'Fixture hash mismatch: '+row.path);
}
