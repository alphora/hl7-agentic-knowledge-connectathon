import java.nio.file.*;
import java.util.*;
import com.fasterxml.jackson.databind.*;
import ca.uhn.fhir.context.FhirContext;
import org.hl7.fhir.instance.model.api.*;
import org.hl7.fhir.r4.model.*;
import org.opencds.cqf.fhir.cr.library.LibraryProcessor;
import org.opencds.cqf.fhir.cr.plandefinition.PlanDefinitionProcessor;
import org.opencds.cqf.fhir.utility.monad.Eithers;
import org.opencds.cqf.fhir.utility.repository.InMemoryFhirRepository;

// Test client only. Runs unmodified CRL-generated knowledge on the original fixtures.
public class BreastCancerProbe {
  static final FhirContext CTX=FhirContext.forR4Cached();
  static final ObjectMapper JSON=new ObjectMapper();
  static Resource read(Path p)throws Exception {
    return (Resource)CTX.newJsonParser().parseResource(Files.readString(p));
  }
  static void save(Path p,IBaseResource r)throws Exception {
    Files.writeString(p,CTX.newJsonParser().setPrettyPrint(true).encodeResourceToString(r));
  }
  public static void main(String[] args)throws Exception {
    if(args.length!=4)throw new IllegalArgumentException("artifactRoot fixtureRoot outputRoot rootPlanId");
    Path root=Path.of(args[0]).toAbsolutePath().normalize();
    Path fixtures=Path.of(args[1]).toAbsolutePath().normalize();
    Path out=Path.of(args[2]).toAbsolutePath().normalize();
    if(Files.exists(out))throw new IllegalArgumentException("Output already exists: "+out);
    Files.createDirectories(out);
    JsonNode manifest=JSON.readTree(Files.readString(fixtures.resolve("manifest.json")));
    List<String> expressions=new ArrayList<>();
    for(JsonNode e:manifest.get("expressions"))expressions.add(e.asText());
    Bundle knowledge=new Bundle().setType(Bundle.BundleType.COLLECTION);
    Library target=null;
    try(var paths=Files.walk(root.resolve("src/fhir"))) {
      for(Path p:paths.filter(x->x.toString().endsWith(".json")).sorted().toList()) {
        Resource r=read(p);
        if(r instanceof Library l) {
          for(Attachment a:l.getContent())if("text/cql".equals(a.getContentType()) && a.hasUrl()) {
            Path cql=p.getParent().resolve(a.getUrl()).normalize();
            if(!cql.startsWith(root.resolve("src")) || !Files.isRegularFile(cql))
              throw new IllegalArgumentException("Unresolved local CQL: "+a.getUrl());
            a.setData(Files.readAllBytes(cql)); a.setUrl(null);
          }
          if(l.hasName() && l.getName().equals("BreastCancerNeoadjuvantInterface")) {
            if(target!=null)throw new IllegalArgumentException("Multiple target libraries");
            target=l;
          }
        }
        knowledge.addEntry().setResource(r);
      }
    }
    if(target==null)throw new IllegalArgumentException("Missing generated BreastCancerNeoadjuvantInterface library");
    InMemoryFhirRepository repo=new InMemoryFhirRepository(CTX,knowledge);
    var settings=org.opencds.cqf.fhir.cr.CrSettings.getDefault();
    settings.getEvaluationSettings().addRegisteredNamespace("hl7.fhir.uv.cql","http://hl7.org/fhir/uv/cql");
    LibraryProcessor evaluator=new LibraryProcessor(repo,settings);
    PlanDefinitionProcessor applicator=new PlanDefinitionProcessor(repo,settings);
    int failed=0;
    for(JsonNode c:manifest.get("cases")) {
      String id=c.get("id").asText();
      if(!id.matches("[A-Za-z0-9_-]+"))throw new IllegalArgumentException("Unsafe case ID");
      Path dest=out.resolve(id); Files.createDirectories(dest);
      try {
        Bundle data=(Bundle)read(fixtures.resolve(c.get("bundle").asText()));
        JsonNode oracle=JSON.readTree(Files.readString(fixtures.resolve(c.get("assertions").asText())));
        String subject="Patient/"+oracle.get("evaluationContext").get("patientId").asText();
        long patients=data.getEntry().stream().filter(e->e.getResource() instanceof Patient).count();
        if(patients!=1)throw new IllegalArgumentException("Expected one fixture Patient");
        Parameters parameters=new Parameters();
        var result=evaluator.evaluate(Eithers.forMiddle3(new IdType("Library",target.getIdElement().getIdPart())),subject,expressions,parameters,false,data,null,(IBaseResource)null,(IBaseResource)null,(IBaseResource)null);
        save(dest.resolve("evaluation.json"),result);
        var applied=applicator.applyR5(Eithers.forMiddle3(new IdType("PlanDefinition",args[3])),List.of(subject),null,null,null,null,null,null,null,null,parameters,false,data,null,(IBaseResource)null,(IBaseResource)null,(IBaseResource)null);
        save(dest.resolve("apply-raw.json"),applied);
        Files.writeString(dest.resolve("invocation.txt"),"PlanDefinition/"+args[3]+"\nLibrary/"+target.getIdElement().getIdPart()+"\n"+subject+"\nOriginal fixture: "+c.get("bundle").asText()+"\n");
        System.out.println("Executed "+id);
      } catch(Exception e) {
        failed++;
        Files.writeString(dest.resolve("execution-error.txt"),e.toString());
        e.printStackTrace(System.err);
      }
    }
    System.out.println("Execution failures: "+failed);
    if(failed>0)System.exit(1);
  }
}
