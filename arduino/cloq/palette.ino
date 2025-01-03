uint32_t* test_palette = new uint32_t[6]{
  strip.ColorHSV(0 * 256),
  strip.ColorHSV(15 * 256),
  strip.ColorHSV(122 * 256),
  strip.Color(230, 0, 160),
  strip.Color(19, 0, 155),
  strip.Color(225, 172, 187)
};

uint32_t transPink = hueAngleToColour(305);
uint32_t transBlue = hueAngleToColour(180);
uint32_t white = strip.Color(0, 0, 0, 255);

uint32_t* trans_flag = new uint32_t[6]{
  transBlue,
  white,
  transPink
};

void bumpPalette(int time) {
  showPalette(floor(time / 100));
}

void showPalette(int offset) {
  int interval = strip.numPixels() / 3; // TODO count palette size
  int spacing = 20;
  for (int segment=0; segment<3; segment++) {
    uint32_t firstColour = test_palette[segment % 3];
    uint32_t secondColour = test_palette[(segment + 1) % 3];
    for (int i=0; i<interval - spacing; i++) {
      strip.setPixelColor((segment * interval + i + offset) % strip.numPixels(), interpolateRgb(firstColour, secondColour, static_cast<float>(i) / static_cast<float>(interval)));
    }
    for (int i=interval - spacing; i<interval; i++) {
      strip.setPixelColor((segment * interval + i + offset) % strip.numPixels(), secondColour);
    }
  }
  strip.show();

}

void transFlag(int time) {
  strip.clear();
  switch ((time / 10000) % 3) {
    case 0:
      stepChunks(time, trans_flag, 3);
      break;
    case 1:
      stepAroundEdge(time, trans_flag, 3);
      break;
    default:
      radiatePalette(time, trans_flag, 3);
  }
  strip.show();
}

void stepChunks(int time, uint32_t* palette, int palette_size) {
  for (int i=0; i<12; i++) {
    paintNumber((i + time / 2000) % 12, palette[palette_size * i / 12]);
  }
}

void stepAroundEdge(int time, uint32_t* palette, int palette_size) {
  // I 300% don't understand c++ why can't I just get the number of objects in the damn array
  for (int i=1; i<=12; i++) {
    paintNumber(i, palette[(i + time / 2000) % palette_size]);
  }
}

void paintNumber(int number, uint32_t colour) {
  int start = handStartFor(number);
  int end = handEndFor(number);
  for (int i=start; i<end; i++) {
    strip.setPixelColor(i, colour);
  }
}
