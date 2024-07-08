#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>


const char *ssid = "addinedu_class_1(2.4G)";
const char *password = "addinedu1";

AsyncWebServer server(80);

const int ledPin = 2;
const int ledPin2 = 22;
const int ledPin3 = 23;
// Web page
const char html[] PROGMEM = R"rawliteral(
<!DOCTYPE>
<html>
<body>
<center>
<h1>Hello, ESP32 Web Server!</h1>
<div>LED PIN 21 : 
<input type="checkbox" onchange="toggleCheckBox(this)" />
<div>LED PIN 22 : 
<input type="checkbox" onchange="toggleCheckBox2(this)" />
<div>LED PIN 23 : 
<input type="checkbox" onchange="toggleCheckBox3(this)" />
</div>
<script>
function toggleCheckBox(element){
  var req = new XMLHttpRequest();
  if (element.checked){
    req.open("GET", "/on", true);
  } 
  else{
    req.open("GET", "/off", true);
  }
  req.send();
}
function toggleCheckBox2(element){
  var req = new XMLHttpRequest();
  if (element.checked){
    req.open("GET", "/on2", true);
  } 
  else{
    req.open("GET", "/off2", true);
  }
  req.send();
}
function toggleCheckBox3(element){
  var req = new XMLHttpRequest();
  if (element.checked){
    req.open("GET", "/on3", true);
  } 
  else{
    req.open("GET", "/off3", true);
  }
  req.send();
}
</script>
</center>
</body>
</html>
)rawliteral";


String processor(const String& var){
  Serial.println(var);
  return var;
}


void setup() {
  
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);

  Serial.begin(115200);
  Serial.println("ESP32 Web Server Start");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());



  server.on("/", HTTP_GET, [] (AsyncWebServerRequest *req) {
    req->send_P(200, "text/html", html, processor);
  });
  server.on("/on", HTTP_GET, [] (AsyncWebServerRequest *req) {
    Serial.println("on1");
    digitalWrite(ledPin, HIGH);
    req->send_P(200, "text/html", html, processor);
  });
  server.on("/off", HTTP_GET, [] (AsyncWebServerRequest *req) {
    Serial.println("off1");
    digitalWrite(ledPin, LOW);
    req->send_P(200, "text/html", html, processor);
  });
  server.on("/on2", HTTP_GET, [] (AsyncWebServerRequest *req) {
    Serial.println("on2");
    digitalWrite(ledPin2, HIGH);
    req->send_P(200, "text/html", html, processor);
  });
  server.on("/off2", HTTP_GET, [] (AsyncWebServerRequest *req) {
    Serial.println("off2");
    digitalWrite(ledPin2, LOW);
    req->send_P(200, "text/html", html, processor);
  });
  server.on("/on3", HTTP_GET, [] (AsyncWebServerRequest *req) {
    Serial.println("on3");
    digitalWrite(ledPin3, HIGH);
    req->send_P(200, "text/html", html, processor);
  });
  server.on("/off3", HTTP_GET, [] (AsyncWebServerRequest *req) {
    Serial.println("off3");
    digitalWrite(ledPin3, LOW);
    req->send_P(200, "text/html", html, processor);
  });
    

  server.begin();

  Serial.println("HTTP Server Started!");
  delay(100);
}

void loop() {

}
