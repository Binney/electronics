#include <math.h>

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PI 3.14159265

#define BUTTON_DEBOUNCE_DELAY   20   // [ms]

// D3 = GPIO6
#define LED_PIN     6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT  180

// NeoPixel brightness, 0 (min) to 255 (max)
#define BRIGHTNESS 50 // Set BRIGHTNESS to about 1/5 (max = 255)

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRBW + NEO_KHZ800);

struct Coord {
  float x;
  float y;
} ledsLocations [180];

int mode = 1;

const float innerRadius = 92.0;
const float outerRadius = 152.0;
// Middle of circle = (0, 0)

void setup() {
  Serial.begin(9600);
  Serial.println("Hello world!");
  // put your setup code here, to run once:
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(BRIGHTNESS);

  fillLedLocations();
}

void loop() {
  if (mode == 0) {
    bump_wipe();
  } else {
    bump_rainbow();
  }
}

uint32_t white = strip.Color(0, 0, 0, 255);
uint32_t blue = strip.ColorHSV(65536L / 2);
uint32_t red = strip.ColorHSV(65536L * 0.01);
uint32_t yellow = strip.ColorHSV(65536L * 0.08);

int hue_offset = 0;
void bump_rainbow() {
  hue_offset += 40;
  update_rainbow();
}

void update_rainbow() {
  for (int i=0; i<strip.numPixels(); i++) {
    Coord loc = ledsLocations[i];
    float hue = (loc.y + outerRadius) / (outerRadius * 2); // scale of 0-1
    strip.setPixelColor(i, strip.ColorHSV(65536L * hue + hue_offset));
  }
  strip.show();
}

float wipe_y = 170.0;
bool going_up = false;
void bump_wipe() {
  if (going_up) {
    wipe_y += 0.5;
    if (wipe_y > 170.0) {
      going_up = false;
    }
  } else {
    wipe_y -= 0.5;
    if (wipe_y < -170.0) {
      going_up = true;
    }
  }
  update_wipe();
}

void update_wipe() {
  for (int i=0; i<strip.numPixels(); i++) {
    if (ledsLocations[i].y > wipe_y) {
      strip.setPixelColor(i, yellow);
    } else {
      strip.setPixelColor(i, red);
    }
  }
  strip.show();
}

void fillLedLocations() {
  for (int i=0; i<180; i++) {
    Coord ledI = coordForLed(i);
    ledsLocations[i].x = ledI.x;
    ledsLocations[i].y = ledI.y;
  }
}

Coord coordForLed(int led) {
  int digit = led_to_digit(led); 
  float angle = PI / 2 - digit * PI / 6; // radians innit, anticlockwise from 3
  int handRadius = (outerRadius - innerRadius) * (led % 15) / 15.0; // 15 lights per digit
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
  Serial.print(" ");
  Serial.print(radius);
  Serial.print(", ");
  Serial.print(angle);
  Serial.print(" - ");
  Serial.print(result.x);
  Serial.print(", ");
  Serial.println(result.y);

  return result;
}

int led_to_digit(int led) {
  // 180 LEDs, 12 numbers
  int digit = (led - (led % 15)) / 15;
  return (digit + 6) % 12; // starts at 6 not 0
}
