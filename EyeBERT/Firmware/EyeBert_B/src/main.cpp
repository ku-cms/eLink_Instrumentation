/**********************************************************************
 * Project Name : KU-CMS REV B EyeBERT Relay Mux Board Controller
 * Description  : Set various RF relays to route test signals for
 *                KU-CMS EyeBERT test of cables
 * Sponsor      : A. Bean
 * Device       : Arduino Pro-Mini 5V
 * Compiler     : platformIO Core 6.1.15
 *              : Visual Studio Code 1.91.1
 * Module name  : main.cpp
 * Last Revised : 7-July-2024
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
 *                TX    Which TXp and TXn path to connect
 *                RX    Which RXp and RXn path to connect
 *                MODE  Final output SMA is either KC705 or DMM + or DMM -
 *                      for IBERT or 4-point resistance tests
 *
 * A valid command will not return any text.
 * An invalid command will return the string BAD COMMAND\r\n
 * Commands and parameters are case insensitive
 *
 * Examples :
 * ID
 * returns EyeBERTRelay 0001 0.1 B OK\r\n or similar
 *
 * TX 3
 * returns none but sets path from TXP3 and TXN3 to either the TXP/TXN
 * pair or the DMM+ and DMM- connector pair depending on state of MODE
 *
 * MODE kc705
 * returns none, connects the current TX/RX paths to the 4 sets of SMAs
 * connected to the KC705 FPGA board for IBERT testing.
 *
 * MODE dmm +
 * returns none, connects the current TX/RX paths to the two SMA used
 * by the DMM for 4 point resistance testing of the TXP and RXP paths.
 *
 * MODE DMM -
 * returns none, connects the current TX/RX paths to the two SMA used
 * by the DMM for 4 point resistance testing of the TXN and RXN paths.
 *
 *
 * Using ATMega328 @ 16MHz on board
 * Fuses L=0xFF, H=0xDE, E=0xFD, LB=0xFF
 **********************************************************************/
#include "eyebert_b.h"

/**********************************************************************
   void setup()
   Purpose   : Execute one time and setup all the I/O, memory,
               peripherals, etc.
   Arguments : none
   Returns   : none
   Calls     : various
   Notes     :
   Tested    : 7-2024
 *********************************************************************/
void setup()
{
  Serial.begin(115200);

  // configure MAX4822 reset line
  pinMode(RESET, OUTPUT);
  digitalWrite(RESET, HIGH);
  digitalWrite(RESET, LOW);
  digitalWrite(RESET, HIGH);

  // configure SPI
  pinMode(MOSI, OUTPUT);
  pinMode(SCK, OUTPUT);
  pinMode(CSbar, OUTPUT);
  digitalWrite(CSbar, HIGH);

  // configure other control lines
  pinMode(DMM_4RLY, OUTPUT);
  pinMode(HEARTBEAT, OUTPUT);
  pinMode(ERROR, OUTPUT);
  pinMode(RELAY, OUTPUT);
  digitalWrite(DMM_4RLY, 0);
  digitalWrite(HEARTBEAT, LOW);
  digitalWrite(ERROR, LOW);
  digitalWrite(RELAY, LOW);

  // create command callbacks
  cmdCallBack.addCmd("ID", &cmdID);
  cmdCallBack.addCmd("RST", &cmdRST);
  cmdCallBack.addCmd("TX", &cmdTX);
  cmdCallBack.addCmd("RX", &cmdRX);
  cmdCallBack.addCmd("MODE", &cmdMODE);

  ConfigureMax4822();

  // configure blinkable relays
  HeartbeatLEDState = 0;
  HeartbeatLEDCounter = 0;
  ErrorLEDCounter = 0;
  RelayLEDState = 0;
  RelayLEDCounter = 0;
  ErrorLEDState = 0;
  for (uint8_t i = 0; i < 4; i++)
    Max8422Data[i] = 0;

  Timer1.initialize(10000); // 10ms
  Timer1.attachInterrupt(blink);
}

/**********************************************************************
   void loop()
   Purpose   : Called by main() (hidden in the Arduino environment)
   Arguments : none
   Returns   : none
   Calls     : various
   Notes     :
   Tested    : 7-2024
 *********************************************************************/
void loop()
{
  // respond only to pending events on SERIAL
  cmdCallBack.updateCmdProcessing(&myParser, &myBuffer, &Serial);
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
   Tested    : 7-2024
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
               ERROR and RELAY leds
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : No parameters, any parameters will be ignored.
   Tested    : 7-2024
 *********************************************************************/
void cmdRST(CmdParser *myParser)
{
  Timer1.stop();
  ErrorLEDState = 0;
  RelayLEDState = 0;
  ErrorLEDCounter = 0;
  RelayLEDCounter = 0;

  // manipulate RESET line to clear all other relays
  digitalWrite(RESET, LOW);
  digitalWrite(RESET, HIGH);

  digitalWrite(DMM_4RLY, 0);
  digitalWrite(ERROR, LOW);
  digitalWrite(RELAY, LOW);

  // clear phantom copy
  for (uint8_t i = 0; i < 4; i++)
    Max8422Data[i] = 0;

  Timer1.restart();
}

/**********************************************************************
   void cmdTX(CmdParser *myParser)
   Purpose   : Make a connection for the TX relay paths.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : SMA paths are numbered 1 to 16 and passed as argument to
               command : e.g. TX 3
               Sets both TXP and TXN path as a pair.
   Tested    : 7-2024
 *********************************************************************/
void cmdTX(CmdParser *myParser)
{
  String s;
  uint16_t pcount;
  uint32_t rlypath, magic;
  uint8_t rly, state, idx;

  pcount = myParser->getParamCount();
  if (pcount == 2)
  {
    s = myParser->getCmdParam(1);
    rlypath = s.toInt();
    if (rlypath >= 1 && rlypath <= 16) // TX relay path
    {
      magic = tx2rly[rlypath - 1];
      for (uint8_t i = 0; i < 32; i++)
      {
        // get relay #
        rly = i + 1;
        if (valueinarray(rly, (uint8_t *)listoftxrly))
        {
          // get state (0 or 1)
          idx = 31 - i;
          state = CHECK_BIT(magic, idx);
          WriteMax4822(rly, state, false);
        }
        WriteMax4822(-1, -1, true);
      }
    }
    else
      BadCommand();
  }
  else
    BadCommand();
}

/**********************************************************************
   void cmdRX(CmdParser *myParser)
   Purpose   : Make a connection for the RX relay paths.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : SMA paths are numbered 1 to 16 and passed as argument to
               command : e.g. RX 3
               Sets both RXP and RXN path as a pair.
   Tested    : 7-2024
 *********************************************************************/
void cmdRX(CmdParser *myParser)
{
  String s;
  uint16_t pcount;
  uint32_t rlypath, magic;
  uint8_t rly, state, idx;

  pcount = myParser->getParamCount();
  if (pcount == 2)
  {
    s = myParser->getCmdParam(1);
    rlypath = s.toInt();
    if (rlypath >= 1 && rlypath <= 16) // RX relay path
    {
      magic = rx2rly[rlypath - 1];
      for (uint8_t i = 0; i < 32; i++)
      {
        // get relay #
        rly = i + 1;
        if (valueinarray(rly, (uint8_t *)listofrxrly))
        {
          // get state (0 or 1)
          idx = 31 - i;
          state = CHECK_BIT(magic, idx);
          WriteMax4822(rly, state, false);
        }
        WriteMax4822(-1, -1, true);
      }
    }
    else
      BadCommand();
  }
  else
    BadCommand();
}

/**********************************************************************
   void cmdMODE(CmdParser *myParser)
   Purpose   : Select connection of KC705 for EyeBert measurement or
               to 4-port resistance measurement with DMM.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : command accepts the parameters KC705 or DMM
               further, DMM requires a + or - to indicate which wire
               of the twisted pair is to be measured
               e.g. MODE DMM +
                    MODE KC705
   Tested    : 7-2024
 *********************************************************************/
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
      // need 2nd parameter of + or -
      s = myParser->getCmdParam(2);
      if (s == "+")
      {
        // RLY1 = 1
        // RLY2 = 1
        WriteMax4822(1, 1, false);
        WriteMax4822(2, 1, true);
        digitalWrite(DMM_4RLY, LOW);
        RelayLEDCounter = 0;
        RelayLEDState = 1;
      }
      else if (s == "-")
      {
        // RLY1 = 1
        // RLY2 = 1
        WriteMax4822(1, 1, false);
        WriteMax4822(2, 1, true);
        digitalWrite(DMM_4RLY, HIGH);
        RelayLEDCounter = 0;
        RelayLEDState = 1;
      }
      else
        BadCommand();
    }
    else if (s == "KC705")
    {
      // RLY1 = 0
      // RLY2 = 0
      WriteMax4822(1, 0, false);
      WriteMax4822(2, 0, true);
      digitalWrite(DMM_4RLY, LOW);
      RelayLEDCounter = 0;
      RelayLEDState = 1;
    }
    else
      BadCommand();
  }
  else
    BadCommand();
}

/**********************************************************************
  void blinkLED(void)
   Purpose   : toggle the heartbeat LED attached to the ProMini
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : LEDs are automatically extinguished when suffent
               10ms interrupts have passed.
   Tested    : 7-2024
 *********************************************************************/
void blink(void)
{

  if (ErrorLEDState == 1)
  {
    digitalWrite(ERROR, HIGH);
    if (++ErrorLEDCounter == 1000) // 10 seconds
    {
      ErrorLEDState = 0; // turn off next pass
      ErrorLEDCounter = 0;
    }
  }
  else
    digitalWrite(ERROR, LOW);

  if (RelayLEDState == 1)
  {
    digitalWrite(RELAY, HIGH);
    if (++RelayLEDCounter == 200) // 2 seconds
    {
      RelayLEDState = 0; // turn off next pass
      RelayLEDCounter = 0;
    }
  }
  else
    digitalWrite(RELAY, LOW);

  // heartbeat LED
  if (++HeartbeatLEDCounter == 100) // 1 second
  {
    digitalWrite(HEARTBEAT, HeartbeatLEDState);
    HeartbeatLEDState ^= 1;
    HeartbeatLEDCounter = 0;
  }
}

/**********************************************************************
   void WriteMax4822(uint8_t relay_coil, uint8_t onoff, bool update)
   Purpose   : Set or clear bit in local copy of relay registers then
               pass along to the MAX4822 chips
   Arguments : relay_coil : the RLYx id from schematic
               onoff : 0=de-energize coil, 1=energize coil
               update : update relays (true) or just update
               shadow registers (false)
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : if relay_coil and onoff are both -1, then skip the
               bit set/clear steps
   Tested    : 7-2024
 *********************************************************************/
void WriteMax4822(uint8_t relay_coil, uint8_t onoff, bool update)
{
  uint8_t bit_location, which_chip;

  if (relay_coil >= 1 && relay_coil <= 32) // skip this by setting relay_coil=-1
  {
    bit_location = rlyposition[relay_coil - 1][0]; // look up bit position
                                                   // in MAX4822 data word
    which_chip = rlyposition[relay_coil - 1][1];   // look up which MAX4822 chip

#ifdef RWYDEBUG
    Serial.printf("relay_coil=%d onoff=%d bit_location=%d which_chip=%d\r\n",
                  relay_coil, onoff, bit_location, which_chip);
#endif

    if (onoff == 1)
    {
      bitSet(Max8422Data[which_chip - 1], bit_location);
    }
    else if (onoff == 0)
    {
      bitClear(Max8422Data[which_chip - 1], bit_location);
    }
  }

  if (update == true) // it is possible to skip updating relay coils
  {
#ifdef RWYDEBUG
    for (uint8_t i = 0; i < 4; i++)
      Serial.printf("%02x ", Max8422Data[i]);
    Serial.write('\n');
#endif
    RelayLEDState = 1; // turn on next pass
    RelayLEDCounter = 0;
    // update relay via SPI bit-bang style
    digitalWrite(CSbar, LOW);
    for (uint8_t i = 0; i < 4; i++)
    {
      shiftOut(MOSI, SCK, MSBFIRST, 0x00); // address for coils is always 0
      shiftOut(MOSI, SCK, MSBFIRST, Max8422Data[i]);
    }
    digitalWrite(CSbar, HIGH);
    digitalWrite(MOSI, LOW);
    digitalWrite(SCK, LOW);
  }
}

/**********************************************************************
  void ConfigureMax4822(void)
   Purpose   : Force reset of MAX4822s and any other register
               programming done here.
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : deterined that the highest hold voltage of 70% is 
               insufficient to keep RF relay active, must use 100%
   Tested    : 7/2024
 *********************************************************************/
void ConfigureMax4822(void)
{
  uint8_t address, data;

  digitalWrite(CSbar, HIGH);
  // needs minimum pulse width of 70ns
  // this will be much longer!
  digitalWrite(RESET, LOW);
  digitalWrite(RESET, HIGH);

  // must ooperate voltage is 80% of VCC which is no problem as
  // the full VCC is applied to close a relay
  // Not specified is the hold voltage whill need to be determined
  // by testing. Start with a hold of 70% of VCC for an estimated
  // current per relay of i = (0.7*5)/237 = 14.8mA vs a full 21.1mA
  //
  // address = 0x01
  // data = 0x01
  // four MAX4822 are daisychained so the 16 bit value 0x0101 will
  // need to be sent out 4 times while CS- is low
  // not using built in SPI hardware
  //
  // 7/2024 determined that some RF relays won't hold at 70% so all
  // must operate at 100%
  address = 0x01;
  data = 0x00; // power save off
  digitalWrite(CSbar, LOW);
  for (uint8_t i = 0; i < 4; i++)
  {
    shiftOut(MOSI, SCK, MSBFIRST, address);
    shiftOut(MOSI, SCK, MSBFIRST, data);
  }
  digitalWrite(CSbar, HIGH);

  // data word
  // MSB                         LSB
  // D7  D6  D6  D4  D3  D2  D1  D0
  // x   x   x   x   x   PS0 PS1 PS2
  //
  // PS0  PS1  PS2
  //  0    0    0     power-save disabled (default)
  //  0    0    1     Vout to 70% after tps
  //  0    1    0     Vout to 60% after tps
  //  0    1    1     Vout to 50% after tps
  //  1    0    0     Vout to 40% after tps
  //  1    0    1     Vout to 30% after tps
  //  1    1    0     Vout to 20% after tps
  //  1    1    1     Vout to 10% after tps
}

/**********************************************************************
  void BadCommand(void)
   Purpose   : Indicate bad command via response and LEDs
   Arguments : none
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     :
   Tested    : 7/2024
 *********************************************************************/
void BadCommand(void)
{
  Serial.println(F("BAD COMMAND"));
  ErrorLEDCounter = 0;
  ErrorLEDState = 1;
}

/**********************************************************************
  uint8_t valueinarray(uint8_t val, uint8_t *array)
   Purpose   : Check if value exists in an array of uint8_t's
   Arguments : val : value to for testing
               *array : pointer to array of values to test
   Modifies  :
   Returns   : none
   Calls     : none
   Notes     : Because all relays live in the same set of registers
               but we are only setting either TX or RX relays at a time
               it speeds up the process to skip over those relays that
               are not part of TX or RX when setting the opposite path
   Tested    : 7/2024
 *********************************************************************/
uint8_t valueinarray(uint8_t val, uint8_t *array)
{
  uint8_t retval = 0;

  // size of array known to be 15 (0 to 14)
  for (uint8_t i = 0; i < 15; i++)
  {
    if (val == array[i])
    {
      retval = 1;
      break;
    }
  }
  return (retval);
}