import {caseIds, prefix, validateInventory, validateAssertions, verifyBytes} from './fixture-contract.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import { CqlTranslator, LibraryManager, ModelManager, createModelInfoProvider, createLibrarySourceProvider, stringAsSource } from '@cqframework/cql/cql-to-elm';
import { SystemModelInfoProvider } from '@cqframework/cql/cql';
import cql from 'cql-execution';
import cqlfhir from 'cql-exec-fhir';

const root=new URL('../',import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root),'utf8');
const write=(p,v)=>fs.writeFileSync(new URL(p,root),JSON.stringify(v,null,2)+'\n');
fs.mkdirSync(new URL('verification/',root),{recursive:true});
const runId=new Date().toISOString();
write('verification/measure-cql-js.json',{status:'incomplete',runId});
try {
const inventory=JSON.parse(read('docs/intake.json')).files;
validateInventory(inventory);
for(const id of caseIds) for(const name of ['assertions.json','bundle.json']){
 const path=prefix+id+'/'+name; verifyBytes(fs.readFileSync(new URL('.cache/challenge/'+path,root)),inventory.find(f=>f.path===path));
}
const model=new ModelManager();
model.modelInfoLoader.registerModelInfoProvider(new SystemModelInfoProvider());
model.modelInfoLoader.registerModelInfoProvider(createModelInfoProvider((id,namespace,version)=>
  id==='FHIR' && version==='4.0.1' ? stringAsSource(read('.cache/preflight/models/fhir-modelinfo-4.0.1.xml')) : null));
const manager=new LibraryManager(model);
manager.librarySourceLoader.registerProvider(createLibrarySourceProvider((id,namespace,version)=>
  id==='FHIRHelpers' && version==='4.0.1' ? stringAsSource(read('.cache/preflight/models/FHIRHelpers-4.0.1.cql')) : null));

fs.mkdirSync(new URL('generated/elm/',root),{recursive:true});
fs.mkdirSync(new URL('verification/',root),{recursive:true});

const translator=CqlTranslator.fromText(read('input/cql/SteadiMeasure.cql'),manager);
const errors=translator.errors.asJsReadonlyArrayView().map(String);
const warnings=translator.warnings.asJsReadonlyArrayView().map(String);
write('verification/measure-translation.json',{translator:'@cqframework/cql@5.3.0',errors,warnings});
assert.equal(errors.length,0,errors.join('\n'));
const elm=JSON.parse(translator.toJson());
write('generated/elm/SteadiMeasure.json',elm);
fs.mkdirSync(new URL('generated/companions/Library/',root),{recursive:true});
const metadata=JSON.parse(read('package.json'));
write('generated/companions/Library/SteadiMeasure.json',{
 resourceType:'Library',id:'SteadiMeasure',url:metadata.crl.canonicalBase+'/Library/SteadiMeasure',
 version:metadata.version,name:'SteadiMeasure',title:'STEADI screening-completion measure logic',
 status:'draft',experimental:true,date:metadata.crl.date,publisher:'Alphora',
 type:{coding:[{system:'http://terminology.hl7.org/CodeSystem/library-type',code:'logic-library'}]},
 content:[{contentType:'text/cql',data:Buffer.from(read('input/cql/SteadiMeasure.cql')).toString('base64')},
 {contentType:'application/elm+json',data:Buffer.from(JSON.stringify(elm,null,2)+'\n').toString('base64')}]
});

const cases=[];
for(const id of caseIds){
  const file={path:prefix+id+'/assertions.json'};
  const assertions=JSON.parse(read('.cache/challenge/'+file.path));
  const selected=validateAssertions(assertions,id);
  const path=file.path.replace(/assertions.json$/,'bundle.json');
  const bundle=JSON.parse(read('.cache/challenge/'+path));
  const source=cqlfhir.PatientSource.FHIRv401(); source.loadBundles([bundle]);
  const mp=assertions.evaluationContext.measurementPeriod;
  const params={
    'Measurement Period':new cql.Interval(cql.DateTime.parse(mp.start),cql.DateTime.parse(mp.end),mp.startInclusive,mp.endInclusive),
    'Track Context Confirmed':true
  };
  const library=new cql.Library(elm);
  const results=await new cql.Executor(library,undefined,params).exec(source,cql.DateTime.parse('2026-06-15T12:00:00Z'));
  const values=results.patientResults[assertions.evaluationContext.patientId];
  const checks=selected.map(a=>({expression:a.expression,expected:a.expected.value,actual:values[a.expression],present:Object.hasOwn(values,a.expression),passed:Object.hasOwn(values,a.expression)&&values[a.expression]===a.expected.value}));
  cases.push({fixtureId:assertions.fixtureId,checks});
}
const report={runId,status:cases.every(c=>c.checks.every(t=>t.passed))?'passed':'failed',engine:'cql-execution@3.3.2',dataProvider:'cql-exec-fhir@2.2.0',evaluationDateTime:'2026-06-15T12:00:00Z',trackContextConfirmed:true,cases};
write('verification/measure-cql-js.json',report);
console.log(JSON.stringify({status:report.status,cases:cases.length,checks:cases.reduce((n,c)=>n+c.checks.length,0)}));
assert.equal(report.status,'passed');

} catch(error){write('verification/measure-cql-js.json',{status:'failed',runId,error:String(error)});throw error;}
