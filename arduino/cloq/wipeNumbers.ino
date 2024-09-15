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

