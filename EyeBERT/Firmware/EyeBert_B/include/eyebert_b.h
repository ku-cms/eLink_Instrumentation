/**********************************************************************
 * Project Name : KU-CMS REV B EyeBERT Relay Mux Board Controller
 * Description  : Set various RF relays to route test signals for
 *                KU-CMS EyeBERT test of cables
 * Sponsor      : A. Bean
 * Device       : Arduino Pro-Mini 5V
 * Compiler     : platformIO Core 6.1.15
 *              : Visual Studio Code 1.91.1
 * Module name  : eyebert_b.h
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
#pragma once

#include "Arduino.h"
#include "stdio.h"
#include "stdlib.h"
#include "SPI.h"

#include "CmdBuffer.hpp"
#include "CmdCallback.hpp"
#include "CmdParser.hpp"
#include "TimerOne.h"

#include "tables.h"

/* fuses 
 * L 0xFF
 * H 0xDE
 * E 0xFD
 * LB 0xFF
 */

#undef RWYDEBUG // enables some debug routines

/* inline NOPs -- last resort for fixing timings */
#define NOP __asm__("nop\n\t")
#define NOP5 __asm__("nop\n\tnop\n\tnop\n\tnop\n\tnop\n\t")
#define NOP10 __asm__("nop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\t")

// check if bit at pos in val is set
#define CHECK_BIT(var,pos) (((var)>>(pos)) & 1)

/*
 * who are you?
 */
const char NAME[] = "EyeBERTRelay";
const char SN[] = "0001";
const char FW[] = "0.5";
const char HW[] = "B";

/*
 * pins
 */
#define MOSI 11
#define MISO 12
#define SCK 13
#define CSbar 3
#define RESET 2
#define DMM_4RLY 4
#define HEARTBEAT 7
#define ERROR 6
#define RELAY 5

// led states and timing
uint8_t HeartbeatLEDState, RelayLEDState, ErrorLEDState;
uint16_t HeartbeatLEDCounter, RelayLEDCounter, ErrorLEDCounter;

// relay coil states
uint8_t Max8422Data[4];

/*
 * command parsing
 */
CmdCallback<5> cmdCallBack; 
CmdBuffer<32> myBuffer;
CmdParser myParser;
void cmdID(CmdParser *myParser);
void cmdRST(CmdParser *myParser);
void cmdTX(CmdParser *myParser);
void cmdRX(CmdParser *myParser);
void cmdMODE(CmdParser *myParser);

void blink(void);

void WriteMax4822(uint8_t relay_coil, uint8_t value, bool update);
void ConfigureMax4822(void);

void BadCommand(void);

