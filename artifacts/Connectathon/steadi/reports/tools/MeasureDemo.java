import java.nio.file.*;
import java.time.*;
import java.util.*;
import ca.uhn.fhir.context.FhirContext;
import org.hl7.fhir.r4.model.*;
import org.opencds.cqf.fhir.utility.repository.InMemoryFhirRepository;
import org.opencds.cqf.fhir.cr.measure.r4.R4MultiMeasureService;
import org.opencds.cqf.fhir.cr.measure.MeasureEvaluationOptions;
import org.opencds.cqf.fhir.cr.measure.common.MeasurePeriodValidator;
import org.opencds.cqf.fhir.cr.measure.common.MeasureReference;

// Transport adapter: native engine evaluates generated CQL; no clinical calculations here.
public class MeasureDemo {
  public static void main(String[] args) throws Exception {
    var ctx=FhirContext.forR4Cached();
    Path root=Path.of(args[0]), out=Path.of(args[1]);
    if(Files.exists(out)) throw new IllegalArgumentException("Use a fresh output directory");
    Files.createDirectories(out);
    Bundle bundle=new Bundle().setType(Bundle.BundleType.COLLECTION);
    List<String> subjects=new ArrayList<>();
    String measureId=null;
    for(Path tree:List.of(root.resolve("src/fhir"),root.resolve("tests/data/fhir/patient"))) {
      try(var paths=Files.walk(tree)) {
        for(Path p:paths.filter(x->x.toString().endsWith(".json")).sorted().toList()) {
          Resource r=(Resource)ctx.newJsonParser().parseResource(Files.readString(p));
          if(r instanceof Library l) for(Attachment a:l.getContent()) {
            if("text/cql".equals(a.getContentType()) && a.hasUrl()) {
              Path cql=p.getParent().resolve(a.getUrl()).normalize();
              if(!cql.startsWith(root.resolve("src").normalize())) throw new IllegalArgumentException("CQL outside source root");
              a.setData(Files.readAllBytes(cql)); a.setUrl(null);
            }
          }
          if(r instanceof Measure m) {
            if(measureId!=null) throw new IllegalArgumentException("Multiple Measures");
            measureId=m.getIdElement().getIdPart();
          }
          if(r instanceof Patient) subjects.add(r.getIdElement().getIdPart());
          bundle.addEntry().setResource(r);
        }
      }
    }
    if(measureId==null)throw new IllegalArgumentException("No Measure");
    var repo=new InMemoryFhirRepository(ctx,bundle);
    var options=MeasureEvaluationOptions.defaultOptions();
    options.getEvaluationSettings().addRegisteredNamespace("hl7.fhir.uv.cql","http://hl7.org/fhir/uv/cql");
    var service=new R4MultiMeasureService(repo,options,"https://example.org/demo",new MeasurePeriodValidator());
    var reference=MeasureReference.fromOperationParams(List.of(new IdType("Measure",measureId)),List.of(),List.of()).get(0);
    var start=ZonedDateTime.parse("2026-01-01T00:00:00Z");
    var end=ZonedDateTime.parse("2026-12-31T23:59:59Z");
    for(String subject:subjects) {
      var result=service.evaluate(reference,start,end,"subject","Patient/"+subject,null,new Parameters(),null,null);
      Files.writeString(out.resolve(subject+".json"),ctx.newJsonParser().setPrettyPrint(true).encodeResourceToString(result));
    }
    var summary=service.evaluate(reference,start,end,"population",null,null,new Parameters(),null,null);
    Files.writeString(out.resolve("summary.json"),ctx.newJsonParser().setPrettyPrint(true).encodeResourceToString(summary));
    System.out.println("Wrote native MeasureReports for "+subjects.size()+" individuals and summary.");
  }
}
