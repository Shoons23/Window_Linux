#include <WiFi.h>
#include <ESP32Servo.h>

const char* ssid = "addinedu_class_1(2.4G)";
const char* password = "addinedu1";

Servo servo;
const int servo_pin = 5;
WiFiServer server(80);

struct protocol{
  int pin = 21;
  int status = 0;
};

void setup() {
  // put your setup code here, to run once:
  servo.attach(servo_pin);
  
  Serial.begin(115200);
  Serial.println("ESP32 TCP Server Start");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() !=WL_CONNECTED){
    delay(1000);
    Serial.println(".");
  }

  Serial.println();
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient client = server.available();
  if (client){
    Serial.print("Client Connected : ");
    Serial.println(client.remoteIP());
    
    struct protocol p;
    while (client.connected()){
      char data[8];
      while (client.available()> 0){
        client.readBytes(data, 8);
        memcpy(&p, &data, sizeof(p));

        if (p.pin == servo_pin){
          servo.write(p.status);
        }
        else if (p.pin == 35){
          int value = analogRead(p.pin);
          p.status = value;

          memcpy(&data, &p, sizeof(p));
        }
        else{
          digitalWrite(p.pin, p.status);
        }
        Serial.println(p.pin);
        Serial.println(p.status);
        
        client.write(data, 8);
      }

      delay(10);
    }
    
    client.stop();
    Serial.println("Client Disconnected!");
  }
}
