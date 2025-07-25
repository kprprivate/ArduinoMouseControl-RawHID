#include "HID-Project.h"

uint8_t rawhidData[64];

void setup() {
  Serial.begin(9600);
  RawHID.begin(rawhidData, sizeof(rawhidData));
  Mouse.begin();
  Serial.println("Arduino started!");
}

void loop() {
  // Check if data is available and read it
  int bytesRead = RawHID.read();

  if (bytesRead > 0) {
    Serial.print("Bytes read: ");
    Serial.println(bytesRead);

    // Debug: Print all received data
    Serial.print("Received: ");
    for (int i = 0; i < bytesRead && i < 64; i++) {
      Serial.print(rawhidData[i], HEX);
      Serial.print(" ");
      if (i == 15) Serial.println(); // New line every 16 bytes
    }
    Serial.println();

    // Data is in the rawhidData buffer
    uint8_t cmd = rawhidData[0];
    Serial.print("Command: 0x");
    Serial.println(cmd, HEX);

    switch (cmd) {
      case 0x01: // Discovery request
        Serial.println("Discovery request - sending response");
        {
          uint8_t response[64] = {0}; // Initialize all to 0
          memcpy(response, "Arduino_Mouse", 13);
          RawHID.write(response, 64);
        }
        break;

      case 0x02: // Mouse move
        {
          int16_t x = (int16_t)(rawhidData[1] | (rawhidData[2] << 8));
          int16_t y = (int16_t)(rawhidData[3] | (rawhidData[4] << 8));
          Serial.print("Mouse move: x=");
          Serial.print(x);
          Serial.print(" y=");
          Serial.println(y);
          Mouse.move(x, y);
        }
        break;

      case 0x03: // Left click down
        Serial.println("Left click down");
        Mouse.press(MOUSE_LEFT);
        break;

      case 0x04: // Left click up
        Serial.println("Left click up");
        Mouse.release(MOUSE_LEFT);
        break;

      case 0x05: // Mouse wheel
        {
          int8_t wheel = (int8_t)rawhidData[1];
          Serial.print("Mouse wheel: ");
          Serial.println(wheel);
          Mouse.move(0, 0, wheel);
        }
        break;

      default:
        Serial.print("Unknown command: 0x");
        Serial.println(cmd, HEX);
        break;
    }
  }
}