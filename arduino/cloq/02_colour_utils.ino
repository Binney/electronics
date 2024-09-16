uint32_t red = hueAngleToColour(3.6);
uint32_t yellow = hueAngleToColour(30);


uint8_t redFrom(uint32_t colour) {
  return (colour >> 16) & 0xFF;
}

uint8_t greenFrom(uint32_t colour) {
  return (colour >> 8) & 0xFF;
}

uint8_t blueFrom(uint32_t colour) {
  return colour & 0xFF;
}

uint8_t whiteFrom(uint32_t colour) {
  return colour & 0xFF;
}

uint32_t interpolateRgb(uint32_t x, uint32_t y, float t) {
  uint8_t r = redFrom(x) + (redFrom(y) - redFrom(x)) * t;
  uint8_t g = greenFrom(x) + (greenFrom(y) - greenFrom(x)) * t;
  uint8_t b = blueFrom(x) + (blueFrom(y) - blueFrom(x)) * t;
  uint8_t w = whiteFrom(x) + (whiteFrom(y) - whiteFrom(x)) * t;
  return strip.Color(r, g, b, w);
}

uint32_t hueAngleToColour(float angle) {
  // hue between 0 and 360
  uint32_t hue = angle * 65536L / 360;
  return strip.ColorHSV(hue);
}
