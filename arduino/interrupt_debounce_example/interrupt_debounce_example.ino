#define LED_BUILTIN 2
#define REED 15

volatile unsigned int presses;
volatile unsigned int lastPressHeard;
volatile unsigned int stablePinState;
volatile unsigned int lastCheckedInterrupt;
int debounceInterval = 50;

int printInterval = 100;
int lastPrintedAt;

void IRAM_ATTR pinthing()
{
  if (!digitalRead(REED) && stablePinState && millis() - lastCheckedInterrupt > debounceInterval)
  {
    lastPressHeard = millis();
    stablePinState = 0;
    presses++;
  }
  lastCheckedInterrupt = millis();
}

void setup() {
  Serial.begin(115200);
  Serial.println("Hello World");
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(REED, INPUT_PULLUP);
  attachInterrupt(REED, pinthing, CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(REED)) {
    digitalWrite(LED_BUILTIN, LOW);
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  if (millis() - lastPrintedAt > printInterval) {
    Serial.print("Presses: ");
    Serial.print(presses);
    Serial.print("\tPin state: ");
    Serial.println(digitalRead(REED));
  }
  if (millis() - lastPressHeard > debounceInterval) {
    stablePinState = digitalRead(REED);
  }
}
