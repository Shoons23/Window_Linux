#include <ESP32Servo.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

Servo servo;
const int servo_pin = 5;
const int photoresistor_pin = 35;

const char *ssid = "addinedu_class_1(2.4G)";
const char *password = "addinedu1";

AsyncWebServer server(80);
const char* INPUT_PARAM1 = "degree";

const char html[] PROGMEM = R"rawliteral(
  <!DOCTYPE html>
  <html>
  <body>
  <center>
  <h1>Hello, ESP32 WEb Server - Async</h1>
  <div>
  Photoresistor Value : <div id="sensor">None</div>
  </div>

  <form action="/get">
  Servo Degree : <input type="text" name="degree">
  <input type="submit" value="Submit">
  </form>
  </center>
  <script>
  setInterval(getSensorValue, 1000);
  function getSensorValue(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
      if(this.readyState == 4 && this.status == 200){
        document.getElementById("sensor").innerHTML = this.responseText;
      }
    };
    xhttp.open("GET", "/sensor", true);
    xhttp.send();
  }
  </script>
  </body>
  </html>
  )rawliteral";
// const char html[] PROGMEM = R"rawliteral(
//   <!DOCTYPE html>
//   <html>
//   <head>
//     <style>
//       body {
//         font-family: Arial, sans-serif;
//         background-color: #f0f0f0;
//         padding: 20px;
//       }
//       h1 {
//         text-align: center;
//         color: #333333;
//       }
//       form {
//         text-align: center;
//         margin-top: 20px;
//       }
//       input[type=text] {
//         padding: 10px;
//         width: 200px;
//         box-sizing: border-box;
//         border: 2px solid #ccc;
//         border-radius: 4px;
//         font-size: 16px;
//       }
//       input[type=submit] {
//         background-color: #4CAF50;
//         color: white;
//         padding: 10px 20px;
//         text-align: center;
//         text-decoration: none;
//         display: inline-block;
//         font-size: 16px;
//         border: none;
//         border-radius: 4px;
//         cursor: pointer;
//       }
//       input[type=submit]:hover {
//         background-color: #45a049;
//       }
//     </style>
//   </head>
//   <body>
//     <h1>Hello, ESP32 Web Server - Async</h1>
//     <form action="/get">
//       Servo Degree: <input type="text" name="degree">
//       <input type="submit" value="Submit">
//     </form>
//   </body>
//   </html>
// )rawliteral";


String processor(const String& var){
  Serial.println(var);
  return var;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("ESP32 Web Server Start");
  Serial.println(ssid);

  servo.attach(servo_pin);

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
  server.on("/sensor", HTTP_GET, [] (AsyncWebServerRequest *request){
    int sensor = analogRead(photoresistor_pin);
    String s1 = String(sensor);
    Serial.println(s1);
    request -> send(200,"text/plain", s1);
  });
  server.on("/get", HTTP_GET, [] (AsyncWebServerRequest *req) {
    String inputMessage = req->getParam(INPUT_PARAM1)->value();
    Serial.println(inputMessage);
    float degree = inputMessage.toFloat();
    servo.write(degree);
    req->send_P(200, "text/html", html, processor);
  });
  
  
  server.begin();

  Serial.println("HTTP Server Started!");
  delay(100);
}

void loop() {
  // put your main code here, to run repeatedly:
 
}
