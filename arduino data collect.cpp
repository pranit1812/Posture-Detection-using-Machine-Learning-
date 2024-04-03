#include <Arduino_LSM9DS1.h>

unsigned long startTime;

void setup() {
  Serial.begin(115200);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  startTime = millis(); // Record the start time
}

void loop() {
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - startTime;

  // Collect data for 2 seconds (2000 milliseconds)
  if (elapsedTime < 2000) {
    float accX, accY, accZ;
    float gyroX, gyroY, gyroZ;
    float magX, magY, magZ;

    IMU.readAcceleration(accX, accY, accZ);
    IMU.readGyroscope(gyroX, gyroY, gyroZ);
    IMU.readMagneticField(magX, magY, magZ);

    Serial.print("AccX: ");
    Serial.print(accX);
    Serial.print(" | AccY: ");
    Serial.print(accY);
    Serial.print(" | AccZ: ");
    Serial.print(accZ);
    Serial.print(" | GyroX: ");
    Serial.print(gyroX);
    Serial.print(" | GyroY: ");
    Serial.print(gyroY);
    Serial.print(" | GyroZ: ");
    Serial.print(gyroZ);
    Serial.print(" | MagX: ");
    Serial.print(magX);
    Serial.print(" | MagY: ");
    Serial.print(magY);
    Serial.print(" | MagZ: ");
    Serial.println(magZ);
  } else {
    // Stop collecting data after 2 seconds
    Serial.println("Data collection complete");
    while (1); // You can also add code here to perform any necessary post-processing or actions
  }
}
