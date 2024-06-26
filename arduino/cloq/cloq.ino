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
  randomSeed(analogRead(0));

  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(BRIGHTNESS);

  // pulseWhite(30, 50);
  // pulseWhite(15, 100);
  // pulseWhite(5, 255);
  // pulseYellow(1);
}

int fade = 255;
int lastSeconds = 0;
int lastMins = 0;
int lastHours = 20;
int lastTime = 0;

void loop() {
  strip.clear();
  int time = millis();
  lastMins = floor(time / 1000);
  lastHours = floor(time / (5000 * 60));
  // "Tropick":
  // paintTime(lastHours, lastMins % 60, 0, time, 20);
  // "Lounge":
  // paintTime(lastHours, lastMins % 60, 0, time, 75);
  // ain't got a name for this one yet
  paintTime(lastHours, lastMins % 60, 0, time, 200, (time % 5000) * 10 / 5000);

  lastTime = time;
  // delay(100);

  //wipeNumbers();

  //whiteOverRainbow(75, 5);

  //pulseYellow(1);

  //rainbowFade2White(3, 3, 1);
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

void wipeNumbers() {
    for (int i=1; i<=12; i++) { // Clocks are 1-indexed ok
    int start = handStartFor(i);
    int end = handEndFor(i);
    if (i % 2 == 0) {
      // Count inwards
      for (int j=end; j>=start; j--) {
        for (int k=end; k>=j; k--) {
          strip.setPixelColor(k, strip.ColorHSV((i * 65536L / 12) + (k - j) * 65536L / 36));
        }
        strip.show();
        delay(100);
      }
      for (int j=end; j>=start; j--) {
        strip.setPixelColor(j, strip.Color(0, 0, 0));
        strip.show();
        delay(100);
      }
    } else {
      // Count outwards
      for (int j=start; j<=end; j++) {
        for (int k=start; k<=j; k++) {
          strip.setPixelColor(k, strip.ColorHSV((i * 65536L / 12) + (j - k) * 65536L / 36));
        }
        strip.show();
        delay(100);
      }
      for (int j=start; j<=end; j++) {
        strip.setPixelColor(j, strip.Color(0, 0, 0));
        strip.show();
        delay(100);
      }
    }
    strip.clear();
  }

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

void paintTime(int hours, int mins, int secs, uint32_t hue, int variance, int fade) {
  paintMins(mins, hue, variance, fade);
  paintHour(hours % 12);
  strip.show();
}

void paintMins(int mins, uint32_t hue, int hue_spread, int fade) {
  int hand = sixtyToTwelve(mins);
  int end = handEndFor(hand);
  for (int i=0; i<75; i++) {
    int brightness = floor(lerp(255.0, 0.0, i / (75.0 - fade)));
    if (brightness < 0) brightness = 0;
    strip.setPixelColor((strip.numPixels() + end - i) % strip.numPixels(),
      // strip.ColorHSV(hue + (65536L * i / hue_spread), 255, 255 - (i * 3)));
      strip.ColorHSV(hue + (65536L * i / hue_spread), 255, brightness));
  }

  // int handStart = handStartFor(hand);
  // int handEnd = handEndFor(hand);

  // int start = handStart < handEnd ? handStart : handEnd;
  // int end = handStart < handEnd ? handEnd : handStart;

  // for (int i=start; i<=end; i++) {
  //   strip.setPixelColor(i, strip.ColorHSV(0, 255, 255 - ));
  // }
}

int lerp(float a, float b, float t) {
  // https://en.cppreference.com/w/cpp/numeric/lerp
  return a + t * (b - a);
}

void paintHour(int hour) {
  int start = handInsideFor(hour);
  if (hour % 2 == 0) {
    // Count downwards
    for (int i=start; i>start-lengthOfHourHand; i--) {
      strip.setPixelColor(i, strip.Color(0, 0, 0, 255));
    }
  } else {
    // Count upwards
    for (int i=start; i<start+lengthOfHourHand; i++) {
      strip.setPixelColor(i, strip.Color(100, 50, 0, 255));
    }

  }

}

void printTime(int hours, int mins, int secs) {
  Serial.print("the time is: ");
  Serial.print(hours);
  Serial.print(":");
  Serial.print(mins);
  Serial.print(":");
  Serial.println(secs);
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

int sixtyToTwelve(int x) {
  return (x - (x % 5)) / 5;
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

void pulseWhite(uint8_t wait, int max) {
  for(int j=0; j<max; j++) { // Ramp up from 0 to 255
    // Fill entire strip with white at gamma-corrected brightness level 'j':
    strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
    strip.show();
    delay(wait);
  }

  for(int j=max; j>=0; j--) { // Ramp down from 255 to 0
    strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
    strip.show();
    delay(wait);
  }
}

void pulseYellow(uint8_t wait) {
  for(int j=0; j<256; j++) { // Ramp up from 0 to 255
    // Fill entire strip with white at gamma-corrected brightness level 'j':
    strip.fill(strip.Color(strip.gamma8(j), strip.gamma8(j) / 2.5, 0, 0));
    strip.show();
    delay(wait);
  }

  for(int j=255; j>=0; j--) { // Ramp down from 255 to 0
    strip.fill(strip.Color(strip.gamma8(j), strip.gamma8(j) / 2.5, 0, 0));
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
