import javax.xml.validation.*; import javax.xml.transform.stream.StreamSource; import java.io.File;
public class ValidateXsd { public static void main(String[] a) throws Exception {
 SchemaFactory f=SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema");
 f.setFeature("http://apache.org/xml/features/validation/schema-full-checking", false); Schema s=f.newSchema(new File(a[0])); s.newValidator().validate(new StreamSource(new File(a[1]))); System.out.println("VALID"); } }
