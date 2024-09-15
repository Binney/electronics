int stars[3][2] = {
  {3, 255},
  {100, 100},
  {169, 69}
};

void landslide(int now) {
  int offset = floor(now * 1L / 100);
  Serial.println(offset);
  for(int i=0; i<strip.numPixels() / 2; i++) {
    int diff = i * 10000L / strip.numPixels() - 5000L;
    strip.setPixelColor((i + offset) % strip.numPixels(), strip.gamma32(strip.ColorHSV(diff)));
  }
  for(int i=strip.numPixels() / 2; i<strip.numPixels(); i++) {
    int diff = 5000L - i * 10000L / strip.numPixels();
    strip.setPixelColor((i + offset) % strip.numPixels(), strip.gamma32(strip.ColorHSV(diff)));
  }
  for (int i=0; i<3; i++) {
    int value = stars[i][1];
    if (value <= 0) {
      // Remove key and roll another
      int newStar = floor(random(strip.numPixels()));
      stars[i][0] = newStar;
      stars[i][1] = 255 - floor(random(50));
    } else {
      strip.setPixelColor(stars[i][0], strip.ColorHSV(0, 0, value));
      stars[i][1] = value - 1;
    }
  }
  strip.show();
}
