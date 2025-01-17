const int buttonPin = 15;
const int ledPin = 2;

int ledState = HIGH;        // the current state of the output pin
int buttonState;            // the current reading from the input pin
int lastButtonState = LOW;  // the previous reading from the input pin
int presses;

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers
unsigned long lastPrint;

void setup() {
  Serial.begin(115200);
  Serial.println("Hello World");

  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);

  digitalWrite(ledPin, ledState);
}

void checkPress() {
  int reading = digitalRead(buttonPin);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      if (buttonState == HIGH) {
        presses++;
      }
    }
  }
  lastButtonState = reading;
}

void loop() {
  checkPress();
  digitalWrite(ledPin, digitalRead(buttonPin));
  if (millis() - lastPrint > 100) {
    lastPrint = millis();
    Serial.print("Presses: ");
    Serial.println(presses);
  }
}
