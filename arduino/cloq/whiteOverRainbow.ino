int head = 5;
int tail = 0;

int whiteSpeed = 75;
int whiteLength = 5;

void bumpWhiteOverRainbow(int now) {
  int hueOffset = now * 2;
  for(int i=0; i<strip.numPixels(); i++) {  // For each pixel in strip...
    if(((i >= tail) && (i <= head)) ||      //  If between head & tail...
        ((tail > head) && ((i >= tail) || (i <= head)))) {
      strip.setPixelColor(i, strip.Color(0, 0, 0, 255)); // Set white
    } else {                                             // else set rainbow
      int pixelHue = hueOffset + (i * 65536L / strip.numPixels());
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
  }

  strip.show(); // Update strip with new contents
  // There's no delay here, it just runs full-tilt until the timer and
  // counter combination below runs out.

  if((now - lastTime) > whiteSpeed) { // Time to update head/tail?
    if(++head >= strip.numPixels()) {      // Advance head, wrap around
      head = 0;
    }
    if(++tail >= strip.numPixels()) {      // Advance tail, wrap around
      tail = 0;
    }
    lastTime = now;                   // Save time of last movement
  }
}
