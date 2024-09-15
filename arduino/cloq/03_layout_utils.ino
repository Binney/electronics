#include <math.h>

#define PI 3.14159265

const float innerRadius = 60.0; // Not accurate, but looks about right
const float outerRadius = 140.0;
// Middle of circle = (0, 0)

void fillLedLocations() {
  for (int i=0; i<LED_COUNT; i++) {
    Coord ledI = coordForLed(i);
    ledsLocations[i].x = ledI.x;
    ledsLocations[i].y = ledI.y;
  }
}

Coord coordForLed(int led) {
  int digit = led_to_digit(led); 
  float angle = PI / 2 - digit * PI / 6; // radians innit, anticlockwise from 3
  float handRadius = (outerRadius - innerRadius) * (led % 15) / 15.0; // 15 lights per digit
  Coord result;
  float radius;
  if (digit % 2 == 0) {
    // Even number, start on the outside
    radius = outerRadius - handRadius;
    result.x = radius * cos(angle);
    result.y = radius * sin(angle);
  } else {
    // Odd number, start on the inside
    radius = innerRadius + handRadius;
    result.x = radius * cos(angle);
    result.y = radius * sin(angle);
  }

  Serial.print(led);
  Serial.print(": ");
  Serial.print(digit);
  Serial.print(" r=");
  Serial.print(radius);
  Serial.print(", a=");
  Serial.print(angle);
  Serial.print(" - ");
  Serial.print(result.x);
  Serial.print(", ");
  Serial.println(result.y);

  return result;
}

int led_to_digit(int led) {
  // 180 LEDs, 12 numbers
  int digit = flint(led, 15);
  return (digit + 6) % 12; // starts at 6 not 0
}

int handInsideFor(int digit) {
  if (digit % 2 == 0) {
    return handEndFor(digit);
  }
  return handStartFor(digit);
}

int handOutsideFor(int digit) {
  if (digit % 2 == 0) {
    return handStartFor(digit);
  }
  return handEndFor(digit);
}

int handStartFor(int digit) {
  if (digit >= 6) {
    return (digit - 6) * 15;
  }
  if (digit >= 4) {
    return (digit + 6) * 15 + 1;
  }
  return (digit + 6) * 15;
}

int handEndFor(int digit) {
  if (digit >= 6) {
    return (digit - 5) * 15 - 1;
  }
  if (digit == 3 || digit == 4) {
    return (digit + 7) * 15;
  }
  return (digit + 7) * 15 - 1;
}
