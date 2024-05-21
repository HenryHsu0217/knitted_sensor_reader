#include <WiFi.h>

const char* ssid     = "Your SSID";
const char* password = "Your password";
const uint16_t port = 8080;
const char * host = "Host IP";
WiFiClient client;
const int sensorPin = A0;
int sensorValue=0;
int loopcount=0;
void setup() {
    Serial.begin(9600);
    delay(10);
    Serial.println();
    Serial.print("[WiFi] Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);
    analogReadResolution(10);
    int tryDelay = 500;
    int numberOfTries = 40;

    while (WiFi.status() != WL_CONNECTED && numberOfTries > 0) {
        delay(tryDelay);
        numberOfTries--;
        Serial.print(".");
    }

    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[WiFi] Failed to connect.");
        // Consider resetting or handling the failed connection properly
    } else {
        Serial.println(WiFi.status());
        Serial.println("[WiFi] WiFi is connected!");
        Serial.print("[WiFi] IP address: ");
        Serial.println(WiFi.localIP());

        // Attempt to connect to the host
        Serial.println("Attempting to connect to host...");
        if(client.connect(host, port)) {
            Serial.println("Connected to host successfully!");
        } else {
            Serial.println("Failed to connect to host.");
            // Handle connection failure to host
        }
    }
}

void loop() {
  analogReadResolution(12);
  sensorValue = 4095-analogRead(sensorPin);
    if (client.connected()) {
        Serial.print(loopcount);
        Serial.print("  ");
        Serial.println(sensorValue);
        client.print(String(loopcount)+" "+String(sensorValue));
    }
    loopcount++;
    delay(50);
}