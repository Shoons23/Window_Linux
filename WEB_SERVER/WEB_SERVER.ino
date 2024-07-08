#include <WiFi.h>
#include <WebServer.h>

const char *ssid = "Fxck";
const char *password = "1234567890";

WebServer server(80);
// Web page
const char html[] PROGMEM = R"rawliteral(
<!DOCTYPE>
<html>
<body>
<center>
<h1>Hello, ESP32 Web Server!</h1>
<a href="on"><button>LED ON</button></a>
<a href="off"><button>LED OFF</button></a> 
</center>
</body>
</html>
)rawliteral";

const int ledPin = 23;

void handle_root(); //페이지 요청 들어오면 처리하는 함수
void ledOn();
void ledoff();


void setup() {
  
  pinMode(ledPin, OUTPUT);

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

  // 서버시작

  server.on("/", handle_root);
  server.on("/on", HTTP_GET, ledOn);
  server.on("/off", HTTP_GET, ledOff);
  
  server.begin();

  Serial.println("HTTP Server Started!");
  delay(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();
}

void handle_root(){
  server.send(200, "text/html", html);
}

void ledOn(){
  digitalWrite(ledPin, HIGH);
  server.send(200, "text/html", html);
}

void ledOff(){
  digitalWrite(ledPin, LOW);
  server.send(200, "text/html", html);
}