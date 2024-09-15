// it's the cloq
// check it out
#include <math.h>

#include <RV-3028-C7.h>

struct Coord {
  float x;
  float y;
} ledsLocations [180];

RV3028 rtc;

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#include "InputDebounce.h"

#define BUTTON_DEBOUNCE_DELAY   20   // [ms]

// D3 = GPIO6
#define LED_PIN     6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT  180

// NeoPixel brightness, 0 (min) to 255 (max)
#define BRIGHTNESS 50 // Set BRIGHTNESS to about 1/5 (max = 255)

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRBW + NEO_KHZ800);

int buttonPin = 12;
static InputDebounce switchButton;

int mode = 6;

void setup() {

  // Wire.begin();
  // while (rtc.begin() == false) {
  //   Serial.println("Something went wrong, check wiring");
  //   delay(1000);
  // }
  // Serial.println("RTC online!");
  randomSeed(analogRead(0));

  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(BRIGHTNESS);

  pinMode(buttonPin, INPUT);
  // TODO startup sequence?
  // wipeNumbers();

  switchButton.registerCallbacks(onButtonPressed, NULL, NULL, NULL);
  switchButton.setup(buttonPin, BUTTON_DEBOUNCE_DELAY, InputDebounce::PIM_INT_PULL_UP_RES);

  fillLedLocations();
}

void onButtonPressed(uint8_t pin) {
  Serial.println("Pressed button!");
  mode = (mode + 1) % 8;
}

int fade = 255;
int lastSeconds = 0;
int lastMins = 0;
int lastHours = 20;
int lastTime = 0;

void loop() {
  int now = millis();
  switchButton.process(now);

  if (mode == 0) {
    // Clock
    bumpClock(now);
  } else if (mode == 1) {
    bumpWhiteOverRainbow(now);
  } else if (mode == 2) {
    transFlag(now);
  } else if (mode == 3) {
    landslide(now);
  } else if (mode == 4) {
    bumpPalette(now);
  } else if (mode == 5) {
    radiateRainbow(now);
  } else if (mode == 6) {
    bump_vertical_wipe();
  } else {
    bump_vertical_rainbow();
  }
  // lastTime = time;
  // delay(100);

  // if (rtc.updateTime() == false) //Updates the time variables from RTC
  // {
  //   Serial.println("RTC failed to update");
  //   return;
  // }

  // String currentTime = rtc.stringTimeStamp();
  // if (lastSeconds == rtc.getSeconds()) {
  //   fade = fade * 0.97;
  // } else {
  //   fade = 255;
  // }
  // paintTime(rtc.getHours(), rtc.getMinutes(), rtc.getSeconds(), fade);
  // lastSeconds = rtc.getSeconds();

}
