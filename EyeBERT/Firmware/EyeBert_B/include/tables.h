/**********************************************************************
 * Project Name : KU-CMS REV B EyeBERT Relay Mux Board Controller
 * Description  : Set various RF relays to route test signals for
 *                KU-CMS EyeBERT test of cables
 * Sponsor      : A. Bean
 * Device       : Arduino Pro-Mini 5V
 * Compiler     : platformIO Core 6.1.15
 *              : Visual Studio Code 1.91.1
 * Module name  : tables.h
 * Last Revised : 7-July-2024
 *
 * Instrumentation Design Laboratory
 * Malott Hall, Room 6042
 * 1251 Wescoe Hall Drive, The University of Kansas
 * Lawrence, Kansas 66045
 *
 * Robert W. Young, Director, Design Engineer
 *
 * Notes        various tables of magic values needed by eyebert_b

 **********************************************************************/
#pragma once

#include "Arduino.h"

// subtract 1 from relay rly# designation
// on PCB to use as index into table
// the two values retrieved are the bit position
// within the 8 bit data word and which chip
// contains the relay
// {rly#, controlchip}
const uint8_t rlyposition[32][2] = {
    {0, 4},  // example rly1 (indexed as 0) is at bit position 0 of control chip 4
    {0, 2},  // rly2
    {4, 3},  // rly2
    {0, 3},  // rly4
    {4, 4},  // rly5
    {3, 2},  // rly6
    {1, 2},  // rly7
    {2, 2},  // rly8
    {1, 3},  // rly9
    {2, 3},  // rly10
    {5, 3},  // rly11
    {6, 4},  // rly12
    {2, 4},  // rly13
    {1, 4},  // rly14
    {4, 1},  // rly15
    {7, 2},  // rly16
    {5, 2},  // rly17
    {6, 2},  // rly18
    {4, 2},  // rly19
    {0, 1},  // rly20
    {3, 3},  // rly21
    {6, 3},  // rly22
    {7, 3},  // rly23
    {7, 4},  // rly24
    {5, 4},  // rly25
    {3, 4},  // rly26
    {5, 1},  // rly27
    {6, 1},  // rly28
    {7, 1},  // rly29
    {3, 1},  // rly30
    {2, 1},  // rly31
    {1, 1}}; // rly32

// magic words that represent path through relays
// to connect TXP# and TXN# to KC705 or DMM SMAs
const uint32_t tx2rly[] = {
    0x00000000, 0x00040000, 0x00080000, 0x00080040,
    0x08000000, 0x08000080, 0x08100000, 0x81000100,
    0x10000000, 0x10800000, 0x10400000, 0x10400800,
    0x30000000, 0x30000400, 0x10200000, 0x10200200};
// list of which bits are used for TX paths
const uint8_t listoftxrly[] = {3, 4, 5, 9, 10, 11, 12, 13, 14, 21, 22, 23, 24, 25, 26};

// magic words that represent path through relays
// to connect RXP# and RXN# to KC705 or DMM SMAs
const uint32_t rx2rly[] = {
    0x00000000, 0x00001000, 0x00002000, 0x00002001,
    0x01000000, 0x01000002, 0x01004000, 0x01004004,
    0x02000000, 0x02020000, 0x02010000, 0x02010020,
    0x06000000, 0x06000010, 0x06008000, 0x06008008};
// list of which bits are used for RX paths
const uint8_t listofrxrly[] = {6, 7, 8, 15, 16, 17, 18, 19, 20, 27, 28, 29, 30, 31, 32};

uint8_t valueinarray(uint8_t val, uint8_t *array);