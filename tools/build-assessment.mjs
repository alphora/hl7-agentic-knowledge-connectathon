import fs from 'node:fs';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {CqlTranslator,LibraryManager,ModelManager,createModelInfoProvider,createLibrarySourceProvider,stringAsSource} from '@cqframework/cql/cql-to-elm';
import {SystemModelInfoProvider} from '@cqframework/cql/cql';
import cql from 'cql-execution';
import cqlfhir from 'cql-exec-fhir';
import {caseIds,prefix,validateInventory,verifyBytes} from './fixture-contract.mjs';
const root=new URL('../',import.meta.url),read=p=>fs.readFileSync(new URL(p,root),'utf8');
const write=(p,x)=>{fs.mkdirSync(new URL(p.substring(0,p.lastIndexOf('/')+1),root),{recursive:true});fs.writeFileSync(new URL(p,root),JSON.stringify(x,null,2)+'\n');};
const names=['In Screening Population','Completed Three Question Screen','At Increased Fall Risk','Exercise Intervention Applicable','Consider Multifactorial Intervention','Initial Population','Denominator','Numerator'];
const runId=randomUUID();write('verification/assessment-cql-js.json',{status:'incomplete',runId});
try {
 const inventory=JSON.parse(read('docs/intake.json')).files;validateInventory(inventory);
 const model=new ModelManager();model.modelInfoLoader.registerModelInfoProvider(new SystemModelInfoProvider());
 model.modelInfoLoader.registerModelInfoProvider(createModelInfoProvider((id,namespace,version)=>id==='FHIR'&&version==='4.0.1'?stringAsSource(read('.cache/preflight/models/fhir-modelinfo-4.0.1.xml')):null));
 const manager=new LibraryManager(model);
 manager.librarySourceLoader.registerProvider(createLibrarySourceProvider((id,namespace,version)=>{
  if(id==='FHIRHelpers'&&version==='4.0.1')return stringAsSource(read('.cache/preflight/models/FHIRHelpers-4.0.1.cql'));
  if(id==='SteadiMeasure'&&version==='0.1.0')return stringAsSource(read('input/cql/SteadiMeasure.cql'));
  return null;
 }));
 const translator=CqlTranslator.fromText(read('input/cql/Steadi.cql'),manager);
 const errors=translator.errors.asJsReadonlyArrayView().map(String),warnings=translator.warnings.asJsReadonlyArrayView().map(String);
 write('verification/assessment-translation.json',{errors,warnings,translator:'@cqframework/cql@5.3.0'});
 assert.equal(errors.length,0,errors.join('\n'));
 const elm=JSON.parse(translator.toJson());write('generated/elm/Steadi.json',elm);
 const measure=JSON.parse(read('generated/elm/SteadiMeasure.json'));
 const meta=JSON.parse(read('package.json')),base=meta.crl.canonicalBase;
 write('generated/companions/Library/Steadi.json',{resourceType:'Library',id:'Steadi',url:base+'/Library/Steadi',version:meta.version,name:'Steadi',title:'STEADI assessment and guidance logic',status:'draft',experimental:true,date:meta.crl.date,publisher:'Alphora',type:{coding:[{system:'http://terminology.hl7.org/CodeSystem/library-type',code:'logic-library'}]},relatedArtifact:[{type:'depends-on',resource:base+'/Library/SteadiMeasure|'+meta.version}],content:[{contentType:'text/cql',data:Buffer.from(read('input/cql/Steadi.cql')).toString('base64')},{contentType:'application/elm+json',data:Buffer.from(JSON.stringify(elm,null,2)+'\n').toString('base64')}]});
 const cases=[];
 for(const id of caseIds){
  for(const name of ['assertions.json','bundle.json']){const path=prefix+id+'/'+name;verifyBytes(fs.readFileSync(new URL('.cache/challenge/'+path,root)),inventory.find(f=>f.path===path));}
  const oracle=JSON.parse(read('.cache/challenge/'+prefix+id+'/assertions.json')),bundle=JSON.parse(read('.cache/challenge/'+prefix+id+'/bundle.json'));
  assert.equal(oracle.fixtureId,id);assert.deepEqual(oracle.assertions.map(a=>a.expression).sort(),[...names].sort());
  const mp=oracle.evaluationContext.measurementPeriod,enc=bundle.entry.find(e=>e.resource.resourceType==='Encounter').resource;
  const params={'Encounter Id':enc.id,'Measurement Period':new cql.Interval(cql.DateTime.parse(mp.start),cql.DateTime.parse(mp.end),mp.startInclusive,mp.endInclusive),'Track Context Confirmed':true};
  const patient=cqlfhir.PatientSource.FHIRv401();patient.loadBundles([bundle]);
  const library=new cql.Library(elm,new cql.Repository({SteadiMeasure:measure}));
  const result=await new cql.Executor(library,undefined,params).exec(patient,cql.DateTime.parse('2026-06-15T12:00:00Z'));
  const values=result.patientResults[oracle.evaluationContext.patientId];
  const checks=oracle.assertions.map(a=>({expression:a.expression,expected:a.expected.value,actual:values[a.expression],present:Object.hasOwn(values,a.expression),passed:Object.hasOwn(values,a.expression)&&values[a.expression]===a.expected.value}));
  cases.push({fixtureId:id,checks});
 }
 const controls=[];
 for(const [id,period,context,expected] of [
  ['context-false',['2026-01-01T00:00:00Z','2026-12-31T23:59:59Z'],false,[false,true,true,false,false,false,false,false]],
  ['excluded-period',['2025-01-01T00:00:00Z','2025-12-31T23:59:59Z'],true,[false,false,null,false,false,false,false,false]]
 ]){
  const bundle=JSON.parse(read('.cache/challenge/'+prefix+'eligible-unsteady-yes/bundle.json'));
  const enc=bundle.entry.find(e=>e.resource.resourceType==='Encounter').resource;
  const patient=cqlfhir.PatientSource.FHIRv401();patient.loadBundles([bundle]);
  const library=new cql.Library(elm,new cql.Repository({SteadiMeasure:measure}));
  const params={'Encounter Id':enc.id,'Measurement Period':new cql.Interval(cql.DateTime.parse(period[0]),cql.DateTime.parse(period[1]),true,true),'Track Context Confirmed':context};
  const result=await new cql.Executor(library,undefined,params).exec(patient,cql.DateTime.parse('2026-06-15T12:00:00Z'));
  const values=result.patientResults['patient-eligible-unsteady-yes'];
  const actual=names.map(n=>values[n]);controls.push({id,expected,actual});assert.deepEqual(actual,expected,id);
 }
 const report={controls,status:cases.every(c=>c.checks.every(a=>a.passed))?'passed':'failed',runId,engine:'cql-execution@3.3.2',cases};
 write('verification/assessment-cql-js.json',report);assert.equal(report.status,'passed');
 console.log(JSON.stringify({status:report.status,cases:cases.length,assertions:cases.reduce((n,c)=>n+c.checks.length,0)}));
}catch(error){write('verification/assessment-cql-js.json',{status:'failed',runId,error:String(error)});throw error;}
