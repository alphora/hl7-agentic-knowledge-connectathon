import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import ca.uhn.fhir.context.FhirContext;
import org.hl7.fhir.instance.model.api.*;
import org.hl7.fhir.r4.model.*;
import org.opencds.cqf.fhir.cr.library.LibraryProcessor;
import org.opencds.cqf.fhir.cr.plandefinition.PlanDefinitionProcessor;
import org.opencds.cqf.fhir.cr.questionnaireresponse.QuestionnaireResponseProcessor;
import org.opencds.cqf.fhir.utility.monad.Eithers;
import org.opencds.cqf.fhir.utility.repository.InMemoryFhirRepository;

/** Thin operation adapter. Clinical rules live in the authored CQL/FHIR. */
public class SteadiNative {
 static final FhirContext CTX=FhirContext.forR4Cached();
 static final List<String> EXPRESSIONS=List.of("In Screening Population","Completed Three Question Screen","At Increased Fall Risk","Exercise Intervention Applicable","Consider Multifactorial Intervention","Initial Population","Denominator","Numerator","Assessment Response");
 static <T extends IBaseResource> T read(Class<T> type,String path)throws Exception{
  return CTX.newJsonParser().parseResource(type,Files.readString(Path.of(path),StandardCharsets.UTF_8));
 }
 static void save(Path target,IBaseResource value)throws Exception{
  Files.writeString(target,CTX.newJsonParser().setPrettyPrint(true).encodeResourceToString(value),StandardCharsets.UTF_8);
 }
 public static void main(String[] args)throws Exception{
  if(args.length!=6)throw new IllegalArgumentException("knowledge.json data.json parameters.json Patient/id Encounter/id output-directory");
  Bundle knowledge=read(Bundle.class,args[0]),data=read(Bundle.class,args[1]);
  Parameters parameters=read(Parameters.class,args[2]);
  if(!args[3].matches("Patient/[A-Za-z0-9.-]{1,64}")||!args[4].matches("Encounter/[A-Za-z0-9.-]{1,64}"))throw new IllegalArgumentException("Use relative Patient/id and Encounter/id identities");
  List<Parameters.ParametersParameterComponent> selected=parameters.getParameter().stream().filter(p->p.getName().equals("Encounter Id")).toList();
  if(selected.size()!=1||!(selected.get(0).getValue() instanceof StringType id)||!args[4].equals("Encounter/"+id.getValue()))throw new IllegalArgumentException("Encounter parameter and guidance target must match");
  long matchingPatients=data.getEntry().stream().filter(e->e.getResource() instanceof Patient&&args[3].equals("Patient/"+e.getResource().getIdElement().getIdPart())).count();
  if(matchingPatients!=1)throw new IllegalArgumentException("Exactly one matching patient required");
  Set<String> parameterNames=new HashSet<>();
  for(var parameter:parameters.getParameter())if(!parameterNames.add(parameter.getName()))throw new IllegalArgumentException("Duplicate selection or execution parameter");
  List<Encounter> encounters=data.getEntry().stream().map(Bundle.BundleEntryComponent::getResource).filter(v->v instanceof Encounter).map(v->(Encounter)v).filter(v->args[4].equals("Encounter/"+v.getIdElement().getIdPart())).toList();
  if(encounters.size()!=1)throw new IllegalArgumentException("Exactly one selected encounter required");
  String subject=encounters.get(0).getSubject().getReference();
  if(subject==null||!(subject.equals(args[3])||subject.endsWith("/"+args[3])))throw new IllegalArgumentException("Selected encounter must belong to selected patient");
  Path out=Path.of(args[5]);Files.createDirectories(out);
  if(!knowledge.getEntry().stream().allMatch(e->e.hasResource()&&!List.of("Patient","Encounter","QuestionnaireResponse","Observation").contains(e.getResource().fhirType())))
   throw new IllegalArgumentException("Knowledge bundle must contain definitions only");
  InMemoryFhirRepository repo=new InMemoryFhirRepository(CTX,knowledge);
  Parameters result=(Parameters)new LibraryProcessor(repo).evaluate(Eithers.forMiddle3(new IdType("Library","Steadi")),args[3],EXPRESSIONS,parameters,false,data,null,(IBaseResource)null,(IBaseResource)null,(IBaseResource)null);
  save(out.resolve("evaluation.json"),result);failOnOutcome(result);
  boolean complete=false;QuestionnaireResponse response=null;
  for(var parameter:result.getParameter()){
   if(parameter.getName().equals("Completed Three Question Screen")&&parameter.getValue() instanceof BooleanType b)complete=b.booleanValue();
   if(parameter.getName().equals("Assessment Response")&&parameter.getResource() instanceof QuestionnaireResponse r)response=r;
  }
  if(complete){
   if(response==null)throw new IllegalStateException("Native complete result did not expose the selected response");
   String selectedCanonical=response.getQuestionnaire();
   Questionnaire q=knowledge.getEntry().stream().map(Bundle.BundleEntryComponent::getResource).filter(r->r instanceof Questionnaire).map(r->(Questionnaire)r).filter(r->responseCanonical(r).equals(selectedCanonical)).findFirst().orElseThrow(()->new IllegalStateException("Missing exact versioned Questionnaire"));
   IBaseBundle extracted=new QuestionnaireResponseProcessor(repo).extract(Eithers.forRight((IBaseResource)response),Eithers.forRight((IBaseResource)q),parameters,data,false);
   save(out.resolve("extraction-raw.json"),extracted);failOnOutcome(extracted);
   Bundle adapted=((Bundle)extracted).copy();
   adapted.getMeta().setSecurity(response.getMeta().getSecurity().stream().map(Coding::copy).toList());
   Extension category=q.getExtensionByUrl("http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-observation-extract-category");
   if(category==null||!(category.getValue() instanceof CodeableConcept))throw new IllegalStateException("Expected explicit Questionnaire extraction category");
   for(var entry:adapted.getEntry()){
    if(!(entry.getResource() instanceof Observation observation))throw new IllegalStateException("Unexpected extracted resource");
    observation.setCategory(List.of(((CodeableConcept)category.getValue()).copy()));
    observation.getMeta().setSecurity(response.getMeta().getSecurity().stream().map(Coding::copy).toList());
    observation.setDerivedFrom(List.of(new Reference("QuestionnaireResponse/"+response.getIdElement().getIdPart())));
    entry.getRequest().setMethod(Bundle.HTTPVerb.PUT).setUrl("Observation/"+observation.getIdElement().getIdPart());
   }
   save(out.resolve("extraction.json"),adapted);
  }
  Files.writeString(out.resolve("operations.json"),"{\"extractionInvoked\":"+complete+"}",StandardCharsets.UTF_8);
  IBaseParameters applied=new PlanDefinitionProcessor(repo).applyR5(Eithers.forMiddle3(new IdType("PlanDefinition","steadi-screening-guidance")),List.of(args[3]),args[4],null,null,null,null,null,null,null,parameters,false,data,null,(IBaseResource)null,(IBaseResource)null,(IBaseResource)null);
  save(out.resolve("apply-raw.json"),applied);failOnOutcome(applied);
  Parameters adaptedApply=read(Parameters.class,out.resolve("apply-raw.json").toString());
  for(var parameter:adaptedApply.getParameter())if(parameter.getResource() instanceof Bundle bundle){
   Map<String,String> targets=new HashMap<>();
   for(var entry:bundle.getEntry())if(entry.hasResource()){
    Resource resource=entry.getResource();String relative=resource.fhirType()+"/"+resource.getIdElement().getIdPart();
    if(targets.put(resource.getIdElement().getIdPart(),relative)!=null)throw new IllegalStateException("Ambiguous generated id");
   }
   for(var entry:bundle.getEntry())if(entry.getResource() instanceof RequestGroup group)
    fixActions(group.getAction(),targets);
  }
  save(out.resolve("apply.json"),adaptedApply);
 }
 static void fixActions(List<RequestGroup.RequestGroupActionComponent> actions,Map<String,String> targets){
  for(var action:actions){
   if(action.hasResource()&&targets.containsKey(action.getResource().getReference()))
    action.getResource().setReference(targets.get(action.getResource().getReference()));
   fixActions(action.getAction(),targets);
  }
 }
 static void failOnOutcome(IBaseResource value){
  if(value instanceof OperationOutcome outcome)
   for(var issue:outcome.getIssue())if(issue.getSeverity()==OperationOutcome.IssueSeverity.ERROR||issue.getSeverity()==OperationOutcome.IssueSeverity.FATAL)throw new IllegalStateException(issue.getDiagnostics());
  if(value instanceof Parameters parameters)for(var p:parameters.getParameter())checkParameter(p);
  if(value instanceof Bundle bundle)for(var entry:bundle.getEntry())if(entry.hasResource())failOnOutcome(entry.getResource());
 }
 static void checkParameter(Parameters.ParametersParameterComponent p){
  if(p.hasResource())failOnOutcome(p.getResource());
  for(var part:p.getPart())checkParameter(part);
 }
 static String responseCanonical(Questionnaire q){return q.getUrl()+"|"+q.getVersion();}
}
