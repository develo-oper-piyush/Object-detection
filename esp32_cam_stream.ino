/*
  ESP32-CAM Stream Sketch with LED Control for Vehicle Priority
  - Designed for AI-Thinker ESP32-CAM module
  - Serves an MJPEG stream at /stream and single captures at /capture
  - Controls 3 LEDs (Red, Yellow, Green) for vehicle priority indication
  - Responds to /led?color=red|yellow|green|off endpoint
  - Edit WIFI_SSID and WIFI_PASSWORD below, then upload from Arduino IDE

  LED Connections:
  - Red LED (High Priority): GPIO 12
  - Yellow LED (Medium Priority): GPIO 13
  - Green LED (Low Priority): GPIO 15
  
  Required Arduino libs: "ESP32" board support (install via Board Manager),
  and use example "CameraWebServer" as reference if needed.
*/

#include "esp_camera.h"
#include <WiFi.h>

// Replace with your network credentials
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// LED pin definitions for priority indication
#define LED_RED_PIN 12      // High priority (Emergency vehicles)
#define LED_YELLOW_PIN 13   // Medium priority (Commercial vehicles)
#define LED_GREEN_PIN 15    // Low priority (Personal vehicles)

// Camera pin definitions for AI-Thinker module
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5

#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void startCameraServer();
void setupLEDs();
void setLEDColor(String color);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // Initialize LED pins
  setupLEDs();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // init with high specs to start, reduce if unstable
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // connect to wifi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }
  Serial.println();
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());

  startCameraServer();
  Serial.println("Camera Stream Ready. Use /stream for MJPEG.");
  Serial.println("LED Control: Use /led?color=red|yellow|green|off");
}

void setupLEDs() {
  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_YELLOW_PIN, OUTPUT);
  pinMode(LED_GREEN_PIN, OUTPUT);
  
  // Turn off all LEDs initially
  digitalWrite(LED_RED_PIN, LOW);
  digitalWrite(LED_YELLOW_PIN, LOW);
  digitalWrite(LED_GREEN_PIN, LOW);
  
  Serial.println("LEDs initialized");
}

void setLEDColor(String color) {
  // Turn off all LEDs first
  digitalWrite(LED_RED_PIN, LOW);
  digitalWrite(LED_YELLOW_PIN, LOW);
  digitalWrite(LED_GREEN_PIN, LOW);
  
  // Turn on the requested LED
  if (color == "red") {
    digitalWrite(LED_RED_PIN, HIGH);
    Serial.println("LED: RED (High Priority)");
  } else if (color == "yellow") {
    digitalWrite(LED_YELLOW_PIN, HIGH);
    Serial.println("LED: YELLOW (Medium Priority)");
  } else if (color == "green") {
    digitalWrite(LED_GREEN_PIN, HIGH);
    Serial.println("LED: GREEN (Low Priority)");
  } else if (color == "off") {
    // All LEDs already off
    Serial.println("LED: OFF (No vehicles)");
  }
}

void loop() {
  // nothing to do here — web server handles everything
  delay(1000);
}

#include <WebServer.h>

WebServer server(80);

static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=frame";

void handleStream() {
  WiFiClient client = server.client();
  String response = String("HTTP/1.1 200 OK\r\n") +
    "Content-Type: " + _STREAM_CONTENT_TYPE + "\r\n" +
    "Cache-Control: no-cache\r\n" +
    "Connection: close\r\n" +
    "\r\n";
  client.print(response);

  while (1) {
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      return;
    }

    client.printf("--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n", fb->len);
    client.write(fb->buf, fb->len);
    client.printf("\r\n");
    esp_camera_fb_return(fb);

    if(!client.connected()){
      break;
    }
    delay(10);
  }
}

void handleRoot(){
  server.send(200, "text/plain", "ESP32-CAM Vehicle Detection System\n\nEndpoints:\n/stream - MJPEG video feed\n/capture - Single image capture\n/led?color=red|yellow|green|off - LED control");
}

void handleCapture(){
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    server.send(503, "text/plain", "Camera capture failed");
    return;
  }
  server.sendHeader("Content-Type", "image/jpeg");
  server.sendHeader("Content-Length", String(fb->len));
  server.send(200, "image/jpeg", "");
  WiFiClient client = server.client();
  client.write(fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

void handleLED(){
  if (server.hasArg("color")) {
    String color = server.arg("color");
    setLEDColor(color);
    server.send(200, "text/plain", "LED color set to: " + color);
  } else {
    server.send(400, "text/plain", "Missing color parameter. Use: /led?color=red|yellow|green|off");
  }
}

void startCameraServer(){
  server.on("/", HTTP_GET, handleRoot);
  server.on("/stream", HTTP_GET, [](){ handleStream(); });
  server.on("/capture", HTTP_GET, handleCapture);
  server.on("/led", HTTP_GET, handleLED);
  server.begin();
}
