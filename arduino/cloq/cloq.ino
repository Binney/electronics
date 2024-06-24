// it's the cloq
// check it out
#include <math.h>

#include <RV-3028-C7.h>

RV3028 rtc;

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// D3 = GPIO6
#define LED_PIN     6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT  180

// NeoPixel brightness, 0 (min) to 255 (max)
#define BRIGHTNESS 50 // Set BRIGHTNESS to about 1/5 (max = 255)

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRBW + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)

void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  // Wire.begin();
  // while (rtc.begin() == false) {
  //   Serial.println("Something went wrong, check wiring");
  //   delay(1000);
  // }
  // Serial.println("RTC online!");


  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(BRIGHTNESS);

}

// TODO fill me in if strip lengths aren't always 15
// std::map<int, int> numbers = {
//   {0, 0},
//   {1, 15},
//   {2, 15},

// }
int fade = 255;
int lastSeconds = 0;

void loop() {
  for (int i=0; i<12; i++) {
    strip.setPixelColor(handStartFor(i), strip.ColorHSV(i * 65536L / 12));
    strip.setPixelColor(handEndFor(i), strip.Color(0, 0, 0, 255));//strip.ColorHSV(i * 65536L / 12));
    strip.show();
    delay(100);
  }
  delay(1000);
  strip.clear();
  strip.show();

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

// void tickWipe(int hue, int tick) {
//   for(int i=0; i<strip.numPixels(); i++) {
//     strip.setPixelColor(i, strip.ColorHSV(hue, 100, brightnessFor(i - tick))); // Why does negative modulo never do what I expect it to :'((((
//   }
//   strip.show();
// }

// int brightnessFor(int delta) {
//   return ((strip.numPixels() + delta) % strip.numPixels()) * 255 / strip.numPixels();
// }

int lengthOfHourHand = 3;
int lengthOfNumberStrip = 15;

void paintTime(int hours, int mins, int secs, int fade) {

  int minuteHandOffset = lengthOfNumberStrip * mins;
  // TODO correct for wherever we start around the circle
  for (int i=minuteHandOffset; i<minuteHandOffset + lengthOfNumberStrip; i++) {
    strip.setPixelColor(i, strip.ColorHSV(1000, 255, 255));
  }

  int secondHandOffset = lengthOfNumberStrip * secs;
  int secondsCorrectForZigzag = 3;//floor(secs / 5) % 2; // TODO correct for this plus circle start
  strip.setPixelColor(secondHandOffset, strip.ColorHSV(9000, 255, fade));

  int hourHandOffset = lengthOfNumberStrip * hours;
  // TODO correct for zigzag and circle start
  for (int i=hourHandOffset; i<hourHandOffset + lengthOfHourHand; i++) {
    strip.setPixelColor(i, strip.ColorHSV(5000, 255, 255));
  }

  strip.show();

}

void printTime(int hours, int mins, int secs) {
  Serial.print("the time is: ");
  Serial.print(hours);
  Serial.print(":");
  Serial.print(mins);
  Serial.print(":");
  Serial.println(secs);
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

// Fill strip pixels one after another with a color. Strip is NOT cleared
// first; anything there will be covered pixel by pixel. Pass in color
// (as a single 'packed' 32-bit value, which you can get by calling
// strip.Color(red, green, blue) as shown in the loop() function above),
// and a delay time (in milliseconds) between pixels.
void colorWipe(uint32_t color, int wait) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}

void whiteOverRainbow(int whiteSpeed, int whiteLength) {

  if(whiteLength >= strip.numPixels()) whiteLength = strip.numPixels() - 1;

  int      head          = whiteLength - 1;
  int      tail          = 0;
  int      loops         = 3;
  int      loopNum       = 0;
  uint32_t lastTime      = millis();
  uint32_t firstPixelHue = 0;

  for(;;) { // Repeat forever (or until a 'break' or 'return')
    for(int i=0; i<strip.numPixels(); i++) {  // For each pixel in strip...
      if(((i >= tail) && (i <= head)) ||      //  If between head & tail...
         ((tail > head) && ((i >= tail) || (i <= head)))) {
        strip.setPixelColor(i, strip.Color(0, 0, 0, 255)); // Set white
      } else {                                             // else set rainbow
        int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
        strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
      }
    }

    strip.show(); // Update strip with new contents
    // There's no delay here, it just runs full-tilt until the timer and
    // counter combination below runs out.

    firstPixelHue += 40; // Advance just a little along the color wheel

    if((millis() - lastTime) > whiteSpeed) { // Time to update head/tail?
      if(++head >= strip.numPixels()) {      // Advance head, wrap around
        head = 0;
        if(++loopNum >= loops) return;
      }
      if(++tail >= strip.numPixels()) {      // Advance tail, wrap around
        tail = 0;
      }
      lastTime = millis();                   // Save time of last movement
    }
  }
}

void pulseWhite(uint8_t wait) {
  for(int j=0; j<256; j++) { // Ramp up from 0 to 255
    // Fill entire strip with white at gamma-corrected brightness level 'j':
    strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
    strip.show();
    delay(wait);
  }

  for(int j=255; j>=0; j--) { // Ramp down from 255 to 0
    strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
    strip.show();
    delay(wait);
  }
}

void rainbowFade2White(int wait, int rainbowLoops, int whiteLoops) {
  int fadeVal=0, fadeMax=100;

  // Hue of first pixel runs 'rainbowLoops' complete loops through the color
  // wheel. Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to rainbowLoops*65536, using steps of 256 so we
  // advance around the wheel at a decent clip.
  for(uint32_t firstPixelHue = 0; firstPixelHue < rainbowLoops*65536;
    firstPixelHue += 256) {

    for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...

      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      uint32_t pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());

      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the three-argument variant, though the
      // second value (saturation) is a constant 255.
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue, 255,
        255 * fadeVal / fadeMax)));
    }

    strip.show();
    delay(wait);

    if(firstPixelHue < 65536) {                              // First loop,
      if(fadeVal < fadeMax) fadeVal++;                       // fade in
    } else if(firstPixelHue >= ((rainbowLoops-1) * 65536)) { // Last loop,
      if(fadeVal > 0) fadeVal--;                             // fade out
    } else {
      fadeVal = fadeMax; // Interim loop, make sure fade is at max
    }
  }

  for(int k=0; k<whiteLoops; k++) {
    for(int j=0; j<256; j++) { // Ramp up 0 to 255
      // Fill entire strip with white at gamma-corrected brightness level 'j':
      strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
      strip.show();
    }
    delay(1000); // Pause 1 second
    for(int j=255; j>=0; j--) { // Ramp down 255 to 0
      strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
      strip.show();
    }
  }

  delay(500); // Pause 1/2 second
}
