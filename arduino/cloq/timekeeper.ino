
void bumpClock(int time) {
  strip.clear();
  lastMins = floor(time / 1000);
  lastHours = floor(time / (1000 * 60));
  // "Tropick":
  // paintTime(lastHours, lastMins % 60, 0, time, 20, (time % 5000) * 10 / 5000);
  // "Lounge":
  // paintTime(lastHours, lastMins % 60, 0, time, 75, (time % 5000) * 10 / 5000);
  // "Gentle":
  paintTime(lastHours, lastMins % 60, 0, time, 200, (time % 5000) * 10 / 5000);

}

int lengthOfHourHand = 3;
int lengthOfNumberStrip = 15;

void paintTime(int hours, int mins, int secs, uint32_t hue, int variance, int fade) {
  paintMins(mins, hue, variance, fade);
  paintHour(hours % 12);
  strip.show();
}

void paintMins(int mins, uint32_t hue, int hue_spread, int fade) {
  int hand = flint(mins, 12);
  int end = handEndFor(hand);
  for (int i=0; i<75; i++) {
    int brightness = floor(lerp(255.0, 0.0, i / (75.0 - fade)));
    if (brightness < 0) brightness = 0;
    strip.setPixelColor((strip.numPixels() + end - i) % strip.numPixels(),
      // strip.ColorHSV(hue + (65536L * i / hue_spread), 255, 255 - (i * 3)));
      strip.ColorHSV(hue - (65536L * i / hue_spread), 255, brightness));
  }

  // int handStart = handStartFor(hand);
  // int handEnd = handEndFor(hand);

  // int start = handStart < handEnd ? handStart : handEnd;
  // int end = handStart < handEnd ? handEnd : handStart;

  // for (int i=start; i<=end; i++) {
  //   strip.setPixelColor(i, strip.ColorHSV(0, 255, 255 - ));
  // }
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