String AWS_ACCESS_KEY = "AKIATC67JBOKS66BGGF3";
String AWS_SECRET_ACCESS = "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";
String BUCKET_NAME = "thesisshipdetection";

void setup() {
  Serial.begin(115200);
}

void loop() {
 String toSend = "";
 toSend += AWS_ACCESS_KEY + ",";
 toSend += AWS_SECRET_ACCESS + ",";
 toSend += BUCKET_NAME;

 Serial.println(toSend);

 delay(1000);
}
