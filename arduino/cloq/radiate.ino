void radiateRainbow(int time) {
  strip.clear();
  int step = time / 200;
  long radiateLength = 65536L / 40;
  for (int number=0; number<12; number++) {
      int start = handStartFor(number);
      int end = handEndFor(number);
      for (int i=0; i<end - start; i++) {
      if (number % 2 == 0) {
        strip.setPixelColor(start + i, strip.ColorHSV(step + i * radiateLength));
      } else {
        strip.setPixelColor(end - i, strip.ColorHSV(step + i * radiateLength));
      }
    }
  }
  strip.show();
}

void radiatePalette(int time, uint32_t* palette, int palette_size) {
  int step = time / 200;
  int radiateLength = 8;
  for (int number=0; number<12; number++) {
      int start = handStartFor(number);
      int end = handEndFor(number);
      for (int i=0; i<end - start; i++) {
      if (number % 2 == 0) {
        strip.setPixelColor(start + i, palette[((i + step) / radiateLength) % palette_size]);
      } else {
        strip.setPixelColor(end - i, palette[((i + step) / radiateLength) % palette_size]);
      }
    }
  }
}
