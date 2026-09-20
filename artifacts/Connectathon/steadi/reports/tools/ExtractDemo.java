import java.nio.file.*;
import java.util.*;
import ca.uhn.fhir.context.FhirContext;
import org.hl7.fhir.instance.model.api.*;
import org.hl7.fhir.r4.model.*;
import org.opencds.cqf.fhir.cr.questionnaireresponse.QuestionnaireResponseProcessor;
import org.opencds.cqf.fhir.utility.monad.Eithers;
import org.opencds.cqf.fhir.utility.repository.InMemoryFhirRepository;

/** Operation adapter only. Uses generated definitions and client-completed QR, with no output repair. */
class ExtractDemo {
 static final FhirContext CTX=FhirContext.forR4Cached();
 static Resource read(Path p)throws Exception{return (Resource)CTX.newJsonParser().parseResource(Files.readString(p));}
 public static void main(String[] args)throws Exception{
  Path root=Path.of(args[0]),run=root.resolve("tests/verification/extraction");
  Bundle knowledge=new Bundle().setType(Bundle.BundleType.COLLECTION);
  try(var files=Files.walk(root.resolve("src/fhir"))){
   for(Path p:files.filter(x->x.toString().endsWith(".json")).sorted().toList())knowledge.addEntry().setResource(read(p));
  }
  var settings=org.opencds.cqf.fhir.cr.CrSettings.getDefault();
  settings.getEvaluationSettings().addRegisteredNamespace("hl7.fhir.uv.cql","http://hl7.org/fhir/uv/cql");
  for(String name:List.of("younger-than-65","eligible-all-no","eligible-unsteady-yes","eligible-prior-fall-yes")){
   Path dir=run.resolve(name);
   Questionnaire q=(Questionnaire)read(dir.resolve("questionnaire.json"));
   QuestionnaireResponse qr=(QuestionnaireResponse)read(dir.resolve("client-response.json"));
   if(qr.getStatus()!=QuestionnaireResponse.QuestionnaireResponseStatus.COMPLETED)throw new IllegalArgumentException("Not completed: "+name);
   Bundle data=(Bundle)read(dir.resolve("context.json"));
   var repository=new InMemoryFhirRepository(CTX,knowledge.copy());
   IBaseBundle extracted=new QuestionnaireResponseProcessor(repository,settings).extract(Eithers.forRight((IBaseResource)qr),Eithers.forRight((IBaseResource)q),new Parameters(),data,false);
   Files.writeString(dir.resolve("extraction-raw.json"),CTX.newJsonParser().setPrettyPrint(true).encodeResourceToString(extracted));
   System.out.println(name+": native $extract returned "+((Bundle)extracted).getEntry().size()+" entries");
  }
 }
}
