#include new_inferencing.h
#include Arduino_LSM9DS1.h

eisignal_t ei_signal;  
ei_impulse_result_t result;
float values[3];
float x, y, z;

void setup() {
    delay(2000);   Wait for 2 seconds
    
    Serial.begin(9600);
    if (!IMU.begin()) {
        Serial.println(Failed to initialize IMU!);
        while (1);
    }
    Serial.println(Select a sensor (A)ccelerometer, (G)yroscope, (M)agnetometer);
}

void loop() {
    if (Serial.available()) {
        char choice = Serial.read();
        
        if (choice == 'A'  choice == 'a') {
            IMU.readAcceleration(x, y, z);
            values[0] = x;
            values[1] = y;
            values[2] = z;
        } else if (choice == 'G'  choice == 'g') {
            IMU.readGyroscope(x, y, z);
            values[0] = x;
            values[1] = y;
            values[2] = z;
        } else if (choice == 'M'  choice == 'm') {
            IMU.readMagneticField(x, y, z);
            values[0] = x;
            values[1] = y;
            values[2] = z;
        } else {
            Serial.println(Invalid choice. Please choose (A)ccelerometer, (G)yroscope, (M)agnetometer);
            return;
        }
        
        Serial.print(Read from Sensor );
        Serial.print(x, 2);  
        Serial.print(, );
        Serial.print(y, 2);  
        Serial.print(, );
        Serial.println(z, 2);  

        delay(50);   Optional Adding a small delay for stabilization

        Serial.print(Sending to Model );
        Serial.print(values[0], 2);
        Serial.print(, );
        Serial.print(values[1], 2);
        Serial.print(, );
        Serial.println(values[2], 2);
        
        ei_signal.total_length = 3;
        ei_signal.get_data = &get_data;

        EI_IMPULSE_ERROR res = run_classifier(&ei_signal, &result, false);
        if (res != EI_IMPULSE_OK) {
            Serial.println(Error running classifier);
            return;
        }

         Print confidences for all labels
        for (int i = 0; i  5; i++) {
            Serial.print(result.classification[i].label);
            Serial.print(  );
            Serial.println(result.classification[i].value, 2);
        }
    }
}

static int get_data(size_t offset, size_t length, float out_ptr) {
    if (offset + length  3) return -1;
    for (size_t ix = 0; ix  length; ix++) {
        out_ptr[ix] = values[offset + ix];
    }
    return 0;
}
