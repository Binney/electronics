
int hue_offset = 0;
void bump_vertical_rainbow() {
  hue_offset += 40;
  update_vertical_rainbow();
}

void update_vertical_rainbow() {
  for (int i=0; i<strip.numPixels(); i++) {
    Coord loc = ledsLocations[i];
    float hue = -(loc.y + outerRadius) / (outerRadius * 2); // scale of 0-1
    strip.setPixelColor(i, strip.ColorHSV(65536L * hue - hue_offset));
  }
  strip.show();
}

float wipe_y = 170.0; // bit more than just +outerRadius to -outerRadius, give it turnaround time
bool going_up = false;
void bump_vertical_wipe() {
  if (going_up) {
    wipe_y += 0.5;
    if (wipe_y > 170.0) {
      going_up = false;
    }
  } else {
    wipe_y -= 0.5;
    if (wipe_y < -170.0) {
      going_up = true;
    }
  }
  update_vertical_wipe();
}

void update_vertical_wipe() {
  for (int i=0; i<strip.numPixels(); i++) {
    if (ledsLocations[i].y > wipe_y) {
      strip.setPixelColor(i, yellow);
    } else {
      strip.setPixelColor(i, red);
    }
  }
  strip.show();
}
