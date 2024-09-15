int lerp(float a, float b, float t) {
  // https://en.cppreference.com/w/cpp/numeric/lerp
  return a + t * (b - a);
}

int flint(int x, int y) {
  // geddit, floor int
  return (x - (x % y)) / y;
}
