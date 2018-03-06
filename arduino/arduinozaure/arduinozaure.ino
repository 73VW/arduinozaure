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
    Serial.print("My name is Arduinozaure. Send [ok] to start. Number of analogic pins: ");
    Serial.println(NUM_ANALOG_INPUTS);
    delay(250);
    String cmd = Serial.readString();
    if(cmd == "ok")
      break;
  }
}

void attente()
{
  Serial.println("You can now ask a sensor value. Send me its pin number.");
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
    if(pinNumber >= 0 && pinNumber < NUM_ANALOG_INPUTS){
      pinMode(pinNumber, INPUT);
      long val = analogRead(pinNumber);
      msg = val;
    }
    else
    {
      msg = "Wrong pin number specified..\r\nTry again..";
    }
    Serial.println(msg);
  }
}
