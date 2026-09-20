import java.nio.file.*;
import org.cqframework.cql.cql2elm.*;
// Translation transport only. All clinical expressions come from CRL-generated CQL.
public class ExportElm {
  public static void main(String[] args) throws Exception {
    Path cql=Path.of(args[0]).toAbsolutePath(), out=Path.of(args[1]).toAbsolutePath();
    Files.createDirectories(out);
    var manager=new LibraryManager(new ModelManager());
    manager.getNamespaceManager().addNamespace(new org.hl7.cql.model.NamespaceInfo("hl7.fhir.uv.cql","http://hl7.org/fhir/uv/cql"));
    manager.getLibrarySourceLoader().registerProvider(new DefaultLibrarySourceProvider(new kotlinx.io.files.Path(cql.toFile())));
    int count=0;
    try(var paths=Files.list(cql)) {
      for(Path p:paths.filter(x->x.toString().endsWith(".cql")).sorted().toList()) {
        var translator=CqlTranslator.fromFile(p.toString(),manager);
        if(!translator.getErrors().isEmpty()) throw new IllegalStateException(p+": "+translator.getErrors());
        Files.writeString(out.resolve(p.getFileName().toString().replace(".cql",".json")),translator.toJson());
        System.out.println(p.getFileName()+": ELM JSON emitted; warnings="+translator.getWarnings().size()); count++;
      }
    }
    System.out.println("Translated "+count+" generated CQL libraries.");
  }
}
