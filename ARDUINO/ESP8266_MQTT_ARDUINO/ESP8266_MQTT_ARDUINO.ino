#include <ESP8266WiFi.h>
#include <PubSubClient.h>
 
const char* ssid = "COLDSPOT";
const char* password =  "1234567890";
const char* mqttServer = "192.168.43.135";
const int mqttPort = 1883;
const int QoS_LEVEL = 1;
//const char* mqttUser = "YourMqttUser";
//const char* mqttPassword = "YourMqttUserPassword";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup()
{
//  ESP.restart();
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client"))
    {
      Serial.println("connected");  
    }
    else
    {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
 
  client.publish("rpi_gateway/esp8266", "Hello from ESP8266", QoS_LEVEL);
  //client.subscribe("esp/test");
 
}
 
void callback(char* topic_msg, byte* payload, unsigned int length)
{
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic_msg);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("-----------------------");
 
}
 
void loop()
{
  client.publish("rpi_gateway/esp8266", "MESSAGE FROM ESP8266", QoS_LEVEL);
  delay(1000);
  client.loop();
}
