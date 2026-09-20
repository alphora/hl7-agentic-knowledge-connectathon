import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import ca.uhn.fhir.context.FhirContext;
import org.hl7.fhir.instance.model.api.*;
import org.hl7.fhir.r4.model.*;
import org.opencds.cqf.fhir.cr.library.LibraryProcessor;
import org.opencds.cqf.fhir.cr.plandefinition.PlanDefinitionProcessor;
import org.opencds.cqf.fhir.utility.monad.Eithers;
import org.opencds.cqf.fhir.utility.repository.InMemoryFhirRepository;

// Diagnostic client only: evaluates unmodified CRL-generated logic and retains raw results.
public class GeneratedProbe {
  static final FhirContext CTX=FhirContext.forR4Cached();
  static Resource read(Path p)throws Exception { return (Resource)CTX.newJsonParser().parseResource(Files.readString(p)); }
  static void save(Path p,IBaseResource r)throws Exception { Files.writeString(p,CTX.newJsonParser().setPrettyPrint(true).encodeResourceToString(r)); }
  public static void main(String[] args)throws Exception {
    Path root=Path.of(args[0]), facts=Path.of(args[1]), out=Path.of(args[2]);
    if(Files.exists(out))throw new IllegalArgumentException("Use a fresh output directory");
    Files.createDirectories(out);
    Bundle knowledge=new Bundle().setType(Bundle.BundleType.COLLECTION);
    Library target=null;
    try(var paths=Files.walk(root.resolve("src/fhir"))) {
      for(Path p:paths.filter(x->x.toString().endsWith(".json")).sorted().toList()) {
        Resource r=read(p);
        if(r instanceof Library l) {
          for(Attachment a:l.getContent())if("text/cql".equals(a.getContentType()) && a.hasUrl()) {
            Path cql=p.getParent().resolve(a.getUrl()).normalize();
            if(!cql.startsWith(root.resolve("src").normalize()) || !Files.isRegularFile(cql))throw new IllegalArgumentException("Unresolved CQL: "+a.getUrl());
            a.setData(Files.readAllBytes(cql)); a.setUrl(null);
          }
          if(l.hasName() && l.getName().endsWith("Interface")) {
            if(target!=null)throw new IllegalArgumentException("Ambiguous generated interface library");
            target=l;
          }
        }
        knowledge.addEntry().setResource(r);
      }
    }
    if(target==null)throw new IllegalArgumentException("Missing generated interface library");
    Bundle data=new Bundle().setType(Bundle.BundleType.COLLECTION); Patient patient=null;
    try(var paths=Files.walk(facts)) {
      for(Path p:paths.filter(x->x.toString().endsWith(".json")).sorted().toList()) {
        Resource r=read(p); data.addEntry().setResource(r);
        if(r instanceof Patient x) { if(patient!=null)throw new IllegalArgumentException("Multiple Patients"); patient=x; }
      }
    }
    if(patient==null)throw new IllegalArgumentException("Missing Patient");
    String subject="Patient/"+patient.getIdElement().getIdPart();
    InMemoryFhirRepository repo=new InMemoryFhirRepository(CTX,knowledge);
    org.opencds.cqf.fhir.cr.CrSettings settings=org.opencds.cqf.fhir.cr.CrSettings.getDefault();
    settings.getEvaluationSettings().addRegisteredNamespace("hl7.fhir.uv.cql","http://hl7.org/fhir/uv/cql");
    Parameters parameters=new Parameters();
    var result=new LibraryProcessor(repo,settings).evaluate(Eithers.forMiddle3(new IdType("Library",target.getIdElement().getIdPart())),subject,List.of("In Screening Population","Completed Three Question Screen","At Increased Fall Risk","Exercise Intervention Applicable","Consider Multifactorial Intervention","Initial Population","Denominator","Numerator"),parameters,false,data,null,(IBaseResource)null,(IBaseResource)null,(IBaseResource)null);
    save(out.resolve("evaluation.json"),result);
    String planId=args.length>3?args[3]:"steadi";
    var applied=new PlanDefinitionProcessor(repo,settings).applyR5(Eithers.forMiddle3(new IdType("PlanDefinition",planId)),List.of(subject),null,null,null,null,null,null,null,null,parameters,false,data,null,(IBaseResource)null,(IBaseResource)null,(IBaseResource)null);
    save(out.resolve("apply-raw.json"),applied);
    Files.writeString(out.resolve("invocation.txt"),"PlanDefinition/"+planId+"\nLibrary/"+target.getIdElement().getIdPart()+"\n"+subject+"\n");
    System.out.println("Retained raw evaluation and root PlanDefinition apply in "+out);
  }
}
