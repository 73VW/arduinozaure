#define NUM_DIGITAL_PINS 12
void setup()
{
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}

void loop()
{
  annonce();
  attente();
}

void annonce()
{
  while(Serial.available() == 0)
  {
    Serial.println("My name is Arduinozaure\rSend [ok] to start.");
    Serial.print("Number of digital pins: ");
    Serial.println(NUM_DIGITAL_PINS);
    delay(500);
    String cmd = Serial.readString();
    if(cmd == "ok")
      break;
  }
}

void attente()
{
  Serial.println("You can now ask a sensor value.\rSend me its pin number.");
  while(true)
  {
    unsigned long start = millis();
    int pinNumber = 0;
    while(Serial.available() == 0)
    {
      if(millis() - start > 10000)
        return;
    }
    String m = Serial.readString();
    pinNumber = m.toInt();
    String msg;
    if(pinNumber > 1 && pinNumber < (NUM_DIGITAL_PINS + 2)){
      pinMode(pinNumber, INPUT);
      long val = digitalRead(pinNumber);
      msg = "Value for pin ";
      msg += pinNumber;
      msg += ": ";
      msg += val;
    }
    else
    {
      msg = "Wrong pin number specified..\rTry again..";
    }
    Serial.println(msg);
  }
}
