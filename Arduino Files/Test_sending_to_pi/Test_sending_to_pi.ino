#include <SoftwareSerial.h>

#define rxPin 13
#define txPin 12

// Set up a new SoftwareSerial object


void setup()  {
    Serial.begin(115200);
    
    // Set the baud rate for the SoftwareSerial object
}

void loop() {
    Serial.println("hey");
    delay(100);
}
