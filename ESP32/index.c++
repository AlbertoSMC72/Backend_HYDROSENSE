#include <Adafruit_MPU6050.h>

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>
#include <ArduinoJson.h> // Librería para manejar JSON

// --- MPU6050 ---
Adafruit_MPU6050 mpu;
#define MPU6050_ADDRESS 0x68

// --- Termistor ---
const int analogPin = 32; // Pin analógico del termistor (GPIO32)
const float BETA = 3950.0;
const float T_REF = 298.15;
const float R0 = 100000.0;

// --- Sensor de flujo de agua ---
const int sensorPin = 4;
volatile int pulseCount = 0;
float flowRate = 0;
unsigned long oldTime = 0;

void IRAM_ATTR pulseCounter() {
    pulseCount++;
}

void setupMPU6050() {
    if (!mpu.begin()) {
        while (1) {
            delay(10);
        }
    }
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
}

void setAccelOffsetX(int16_t offset) {
    Wire.beginTransmission(MPU6050_ADDRESS);
    Wire.write(0x06);
    Wire.write(offset & 0xFF);
    Wire.endTransmission();
}

void setAccelOffsetY(int16_t offset) {
    Wire.beginTransmission(MPU6050_ADDRESS);
    Wire.write(0x08);
    Wire.write(offset >> 8);
    Wire.write(offset & 0xFF);
    Wire.endTransmission();
}

void readMPU6050(JsonObject& json) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    json["acceleration_x"] = a.acceleration.x;
    json["acceleration_y"] = a.acceleration.y;
    json["acceleration_z"] = a.acceleration.z;
    json["gyro_x"] = g.gyro.x;
    json["gyro_y"] = g.gyro.y;
    json["gyro_z"] = g.gyro.z;
}

void readThermistor(JsonObject& json) {
    int analogValue = analogRead(analogPin);
    if (analogValue == 0) {
        json["temperature"] = "Error";
    } else {
        float voltage = analogValue / 4095.0 * 3.3;
        float resistance = 100000.0 * voltage / (3.3 - voltage);
        float temperatureK = 1 / (1/T_REF + (1/BETA) * log(resistance / R0));
        float temperatureC = temperatureK - 273.15;
        json["temperature"] = temperatureC;
    }
}

void readFlowSensor(JsonObject& json) {
    if ((millis() - oldTime) > 1000) {
        detachInterrupt(sensorPin);
        flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / 7.5;
        oldTime = millis();
        json["flow_rate"] = flowRate;
        pulseCount = 0;
        attachInterrupt(digitalPinToInterrupt(sensorPin), pulseCounter, FALLING);
    }
}

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(100);
    setupMPU6050();
    pinMode(sensorPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(sensorPin), pulseCounter, FALLING);
}

void loop() {
    StaticJsonDocument<200> doc;
    JsonObject json = doc.to<JsonObject>();

    readMPU6050(json);
    readThermistor(json);
    readFlowSensor(json);
    
    serializeJson(json, Serial);
    Serial.println();
    delay(1000);
}