/**********************************************************************
 * Project Name : KU-CMS EyeBERT Relay Mux Board Controller
 * Description  : Set various RF relays to route test signals for
 *                KU-CMS EyeBERT test of cables
 * Sponsor      : A. Bean
 * Device       : Arduino Pro-Mini 5V
 * Compiler     : platformIO Core 6.1.10
 *              : Visual Studio Code 1.81.1
 * Module name  : sp128128.cpp
 * Last Revised : 28-August-2023
 *
 * Instrumentation Design Laboratory
 * Malott Hall, Room 6042
 * 1251 Wescoe Hall Drive, The University of Kansas
 * Lawrence, Kansas 66045
 *
 * Robert W. Young, Director, Design Engineer
 *
 * Notes        : Uses hardware serial port to accept comamnds &
 *                parameters.
 *
 *                Command List
 *                ID    no parameters, returns string with id info
 *                RST   no parameters, sets all relays to zero
 *                SMA   accept paramter 0-7 to indicate which SMA pair
 *                      to connect
 *                LED   accept parameter 2 or 3
 *
 * A valid command will return any necessary data followed by OK\r\n
 * An invalid command will return the string BAD COMMAND\r\n
 **********************************************************************/
#include "eyebertrelay.h"

uint16_t magic; // value for shift register to control relays & leds

/**********************************************************************
   void setup()
   Purpose   : Execute one time and setup all the I/O, memory,
               peripherals, etc.
   Arguments : none
   Returns   : none
   Calls     : various
   Notes     :
   Tested    :
 *********************************************************************/
void setup()
{

  // configure serial port
  Serial.begin(115200);

  // configure SPI port
  pinMode(MOSI, OUTPUT);
  pinMode(SCK, OUTPUT);
  pinMode(SCL, OUTPUT);
  pinMode(RCK, OUTPUT);
  digitalWrite(MOSI, LOW);
  digitalWrite(SCK, LOW);
  digitalWrite(SCL, HIGH);
  digitalWrite(RCK, HIGH);

  pinMode(EXTERNAL1, OUTPUT);
  pinMode(EXTERNAL2, OUTPUT);
  digitalWrite(EXTERNAL1, LOW);
  digitalWrite(EXTERNAL2, LOW);


  // set relays to default state
  Send595(0);

  // create command callbacks
  cmdCallBack.addCmd("ID", &cmdID);
  cmdCallBack.addCmd("RST", &cmdRST);
  cmdCallBack.addCmd("TX", &cmdTX);
  cmdCallBack.addCmd("RX", &cmdRX);
  cmdCallBack.addCmd("LED", &cmdLED);
  cmdCallBack.addCmd("MODE", &cmdMODE);

  // configure heartbeat
  pinMode(LED4, OUTPUT);
  Timer1.initialize(1000000); // 1000ms
  Timer1.attachInterrupt(blinkLED);
}

/**********************************************************************
   void loop()
   Purpose   : Called by main() (hidden in the Arduino environment)
   Arguments : none
   Returns   : none
   Calls     : various
   Notes     :
   Tested    :
 *********************************************************************/
void loop()
{
  // pending command on serial?
  cmdCallBack.updateCmdProcessing(&myParser, &myBuffer, &Serial);
}

/**********************************************************************
   void Send595(uint16_t val)
   Purpose   : Send 16-bits to 74HCT595 serial shift registers and
               latch. Bits control relays and LEDs
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     :
   Tested    :
 *********************************************************************/
void Send595(uint16_t val)
{
  magic = val;
  digitalWrite(RCK, LOW);
  shiftOut(MOSI, SCK, MSBFIRST, highByte(magic));
  shiftOut(MOSI, SCK, MSBFIRST, lowByte(magic));
  digitalWrite(RCK, HIGH);

#ifdef DEBUG
  for (int i = 0; i < 16; i++)
  {
    if (bitRead(magic, 15 - i) == 1)
      Serial.print("1 ");
    else
      Serial.print("0 ");
  }
  Serial.print("\r\n");
#endif
}

/**********************************************************************
   void cmdID(CmdParser *myParser)
   Purpose   : Respond to ID command and return string with NAME, SN
               FW and HW data.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : No parameters, any parameters will be ignored.
   Tested    :
 *********************************************************************/
void cmdID(CmdParser *myParser)
{
  char s[80];
  // return the ID string via serial
  sprintf(s, "%s %s %s %s", NAME, SN, FW, HW);
  Serial.print(s);
  Serial.println(F(" OK"));
}

/**********************************************************************
   void cmdRST(CmdParser *myParser)
   Purpose   : Force all relays to there default state. Also turns off
              LED2 and LED3
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : No parameters, any parameters will be ignored.
   Tested    :
 *********************************************************************/
void cmdRST(CmdParser *myParser)
{
  // reset relays to default positions
  // all open
  Send595(0x0000);
  // Serial.println("OK");
}

/**********************************************************************
   void cmdTX(CmdParser *myParser)
   Purpose   : Make a connection for the TX relay paths.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : SMAs are numbered T0 to T7. Accept 0 to 7 as parameter.
   Tested    :
 *********************************************************************/
void cmdTX(CmdParser *myParser)
{
  String s;
  uint16_t pcount;
  int sma;
  uint16_t temp;
#ifdef DEBUG
  char debugstring[80];
#endif

  pcount = myParser->getParamCount();
  // accept one parameter, 0 to 7 and connect relays to reach desired SMA
  if (pcount == 2) // possibly a valid command
  {
    s = myParser->getCmdParam(1);
    sma = (int)s.toInt();
    if ((sma < MINIMUM_SMA) || (sma > MAXIMUM_SMA))
    {
      // invalid index
      Serial.println(F("BAD COMMAND"));
    }
    else
    {
      // valid index
      temp = magic;         // get the old value
      temp = temp & 0xFF00; // clear the lower 8
      for (int x = 0; x < 3; x++)
      {
        if (txmap[sma][x] != -1)
          temp = temp | rlymap[txmap[sma][x]]; // build the word

#ifdef DEBUG
        sprintf(debugstring, "txmap[%d][%d] = %d", (int)sma, (int)x, (int)txmap[sma][x]);
        Serial.println(debugstring);
#endif
      }
      // send magic word to SPI port
      Send595(temp);
      // Serial.println("OK");
    }
  }
  else
    Serial.println(F("BAD COMMAND"));
}

/**********************************************************************
   void cmdRX(CmdParser *myParser)
   Purpose   : Make a connection for the RX relay paths.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : SMAs are numbered R0 to R7. Accept 0 to 7 as parameter.
   Tested    :
 *********************************************************************/
void cmdRX(CmdParser *myParser)
{
  String s;
  uint16_t pcount;
  int sma;
  uint16_t temp;
#ifdef DEBUG
  char debugstring[80];
#endif

  pcount = myParser->getParamCount();
  // accept one parameter, 0 to 7 and connect relays to reach desired SMA
  if (pcount == 2) // possibly a valid command
  {
    s = myParser->getCmdParam(1);
    sma = (int)s.toInt();
    if ((sma < MINIMUM_SMA) || (sma > MAXIMUM_SMA))
    {
      // invalid index
      Serial.println(F("BAD COMMAND"));
    }
    else
    {
      // valid index
      temp = magic;         // get value
      temp = temp & 0x00FF; // clear upper 8
      for (int x = 0; x < 3; x++)
      {
        if (rxmap[sma][x] != -1)
          temp = temp | rlymap[rxmap[sma][x]]; // build the word
#ifdef DEBUG
        sprintf(debugstring, "rxmap[%d][%d] = %d", (int)sma, (int)x, (int)rxmap[sma][x]);
        Serial.println(debugstring);
#endif
      }
      // send magic word to SPI port
      Send595(temp);
      // Serial.println("OK");
    }
  }
  else
    Serial.println(F("BAD COMMAND"));
}

/**********************************************************************
   void cmdLED(CmdParser *myParser)
   Purpose   : turn on or off LED2 and LED3 via the 74HCT595 registers
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : Accept two parameters, 2 or 3 for LED and ON or OFF
               for state;
   Tested    :
 *********************************************************************/
void cmdLED(CmdParser *myParser)
{
  String s;
  uint16_t pcount;
  long led;
  uint16_t temp;

  pcount = myParser->getParamCount();
  if (pcount == 3)
  {
    s = myParser->getCmdParam(1);
    led = s.toInt();
    s = myParser->getCmdParam(2);
    s.toUpperCase();
    if (s != "ON" && s != "OFF")
    {
      Serial.println(F("BAD COMMAND"));
    }
    else
    {
      temp = magic;
      switch (led)
      {
      case 2:
        if (s == "ON")
          temp = temp | LED2;
        else
          temp = temp & ~LED2;
        Send595(temp);
        // Serial.println("OK");
        break;
      case 3:
        if (s == "ON")
          temp = temp | LED3;
        else
          temp = temp & ~LED3;
        Send595(temp);
        // Serial.println("OK");
        break;
      default:
        Serial.println(F("BAD COMMAND"));
        break;
      }
    }
  }
}

void cmdMODE(CmdParser *myParser)
{
String s;
  uint16_t pcount;

    pcount = myParser->getParamCount();
  if (pcount >= 2)
  {
    s = myParser->getCmdParam(1);
    s.toUpperCase();
    if (s == "DMM")
    {
      // need a 2nd parameter of + or -
      s = myParser->getCmdParam(2);
      if (s == "+")
      {
        digitalWrite(EXTERNAL1, HIGH);
        digitalWrite(EXTERNAL2, LOW);
      }
      else if (s == "-")
      {
        digitalWrite(EXTERNAL1, HIGH);
        digitalWrite(EXTERNAL2, HIGH);
      }
      else
      {
        Serial.println(F("BAD COMMAND"));
      }
    }
    else if (s == "KC705")
    {
      digitalWrite(EXTERNAL1, LOW);
      digitalWrite(EXTERNAL2, LOW);
    }
    else
    {
      Serial.println(F("BAD COMMAND"));
    }
  }
}

/**********************************************************************
  void blinkLED(void)
   Purpose   : toggle the heartbeat LED attached to the ProMini
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     :
   Tested    :
 *********************************************************************/
void blinkLED(void)
{
  digitalWrite(LED4, !digitalRead(LED4));
}