#define LED_BUILTIN 2
#define REED 15

volatile unsigned int presses;
volatile unsigned int lastPressHeard;
int loopno;

void IRAM_ATTR pinthing()
{
  if (!digitalRead(REED) && millis() - lastPressHeard > 100)
  {
    presses++;
  }
  lastPressHeard = millis();
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
  loopno++;
  // put your main code here, to run repeatedly:
  if (digitalRead(REED)) {
    digitalWrite(LED_BUILTIN, LOW);
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  if (loopno % 10 == 0)
  {
    Serial.println(presses);
  }
}
