#include <Arduino.h>
#include "stdlib.h"
#include "CmdBuffer.hpp"
#include "CmdCallback.hpp"
#include "CmdParser.hpp"
#include "TimerOne.h"

#undef DEBUG

/* inline NOPs -- last resort for fixing timings */
#define NOP __asm__("nop\n\t")
#define NOP5 __asm__("nop\n\tnop\n\tnop\n\tnop\n\tnop\n\t")
#define NOP10 __asm__("nop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\tnop\n\t")

#define MOSI 11
#define SCK 13
#define SCL 14
#define RCK 10
#define LED4 17

#define EXTERNAL1 2 /* 0=KC705 for EYEBERT test, 1=DMM for 4-wire resistance test*/
#define EXTERNAL2 3 /* controls + or - path into DMM*/

/*
 * who are you?
 */
const char NAME[] = "EyeBERTRelay";
const char SN[] = "0002";
const char FW[] = "0.3";
const char HW[] = "A";

const unsigned int rlymap[] = {
    0b0000000000010000, /* D0 */
    0b0000000000100000, /* D1 */
    0b0000000001000000, /* D2 */
    0b0000000000000001, /* D3 */
    0b0000000000001000, /* D4 */
    0b0000000000000010, /* D5 */
    0b0000000000000100, /* D6 */

    0b0001000000000000, /* D7 */
    0b0010000000000000, /* D8 */
    0b0100000000000000, /* D9 */
    0b0000000100000000, /* D10 */
    0b0000100000000000, /* D11 */
    0b0000001000000000, /* D12 */
    0b0000010000000000, /* D13 */
};
const int LED2 = 0b0000000010000000;
const int LED3 = 0b1000000000000000;
#define MAXIMUM_SMA 7
#define MINIMUM_SMA 0
// build up matrix giving the SMA index and which RLY bits to set
const int txmap[8][3] = {
    { 0, 1,-1}, /* T0 */
    { 0, 1, 2}, /* T1 */
    { 0,-1,-1}, /* T2 */
    { 0, 3,-1}, /* T3 */
    { 4,-1,-1}, /* T4 */
    { 4, 5,-1}, /* T5 */
    {-1,-1,-1}, /* T6 */
    { 6,-1,-1}  /* T7 */
};
const int rxmap[8][3] = {
    { 7, 8,-1}, /* R0 */
    { 7, 8, 9}, /* R1 */
    { 7,-1,-1}, /* R2 */
    { 7,10,-1}, /* R3 */
    {11,-1,-1}, /* R4 */
    {11,12,-1}, /* R5 */
    {-1,-1,-1}, /* R6 */
    { 13,1,-1}  /* R7 */
};

void Send595(uint16_t val);
void blinkLED(void);

/*
 * command parsing
 */
CmdCallback<6> cmdCallBack; //
CmdBuffer<32> myBuffer;
CmdParser myParser;
void cmdID(CmdParser *myParser);
void cmdRST(CmdParser *myParser);
void cmdTX(CmdParser *myParser);
void cmdRX(CmdParser *myParser);
void cmdLED(CmdParser *myParser);
void cmdMODE(CmdParser *myParser);
