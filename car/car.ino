#include <WiFi.h>
#include <WebSocketsServer.h>

// WiFi credentials
const char* ssid = "Jadoo";
const char* password = "987654321";

// GPIO pins
const int pin12 = 13;
const int pin13 = 12;
const int pin14 = 14;
const int pin27 = 27;

// WebSocket server
WebSocketsServer webSocket = WebSocketsServer(81);

// Function to handle WebSocket messages
void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
  if (type == WStype_TEXT) {
    String message = String((char*)payload);
    Serial.println("Received: " + message);

    // Parse the message
    if (message.startsWith("D12=")) {
      digitalWrite(pin12, message.substring(4).toInt() == 1 ? HIGH : LOW);
    } else if (message.startsWith("D13=")) {
      digitalWrite(pin13, message.substring(4).toInt() == 1 ? HIGH : LOW);
    } else if (message.startsWith("D14=")) {
      digitalWrite(pin14, message.substring(4).toInt() == 1 ? HIGH : LOW);
    } else if (message.startsWith("D27=")) {
      digitalWrite(pin27, message.substring(4).toInt() == 1 ? HIGH : LOW);
    }
  }
}

void setup() {
  // Initialize serial and pins
  Serial.begin(115200);
  pinMode(pin12, OUTPUT);
  pinMode(pin13, OUTPUT);
  pinMode(pin14, OUTPUT);
  pinMode(pin27, OUTPUT);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.println(WiFi.localIP());

  // Start WebSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  Serial.println("WebSocket server started on port 81");
}

void loop() {
  webSocket.loop();
}
