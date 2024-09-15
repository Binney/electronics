uint32_t red = strip.ColorHSV(65536L * 0.01);
uint32_t yellow = strip.ColorHSV(65536L * 0.08);


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
