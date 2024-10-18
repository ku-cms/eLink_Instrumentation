import serial
import serial.tools.list_ports
import time
from colorama import Fore, init
import sys

#
# sample connection dictionaries
#
typeV_45_15 = {
     "cmd" :{"tx" : "0", "rx" : "0"},
     "d0" : {"tx" : "1", "rx" : "1"},
     "d1" : {"tx" : "2", "rx" : "2"},
     "d2" : {"tx" : "3", "rx" : "3"},
     "d3" : {"tx" : "4", "rx" : "4"}
}

typeV_45_33 = {
     "cmd" :{"tx" : "0", "rx" : "0"},
     "d0" : {"tx" : "1", "rx" : "1"},
     "d1" : {"tx" : "2", "rx" : "2"},
     "d2" : {"tx" : "3", "rx" : "3"},
     "d3" : {"tx" : "4", "rx" : "4"},
     "d4" : {"tx" : "5", "rx" : "5"},
     "d5" : {"tx" : "6", "rx" : "6"}
}

# list of known EyeBert Rev A and EyeBert Rev B boards
list_of_FTDI = ["USB VID:PID=0403:6001 SER=B0026EF9A",
                "USB VID:PID=0403:6001 SER=B0039DXVA",
                "USB VID:PID=0403:6001 SER=B003NFE1A",
                "USB VID:PID=0403:6001 SER=BG001WSTA",
                "USB VID:PID=0403:6001 SER=B003NFDYA"]

init(convert=True) # for colorama to work correctly

class EyeBERTRelayControl:

    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.timeout = 1
        self.blinkOK = True
        self.verbose = True

    def __del__(self):
        self.ser.close()

    # USB VID:PID=0403:6001 SER=B0026EF9A
    # that's an example VID/PID and serial number of the
    # usb chip on the EyeBERT relay board
    # if a different chip is present, add the necessary hwid
    # string in list_of_FTDI
    #
    # if more than one EyeBert board is present, this
    # will return COM for first available board
    def FindEyeBERT(self) :
        port_to_use = None
        ports = serial.tools.list_ports.comports()
        if self.verbose:
            print("Searching serial ports for EyeBERT relay board...")
        for port, desc, hwid in sorted(ports) :
            if self.verbose:
                print(" - {}: {} [{}]".format(port,desc,hwid))
            if hwid in list_of_FTDI :
                port_to_use = port
                break
         
        return port_to_use
    
    def initialize(self) :
        # try and find instand of board
        port_to_use = self.FindEyeBERT()
        if port_to_use != None :
            print(Fore.GREEN + "EyeBERT relay board found on port {}".format(port_to_use))
            self.ser.port = port_to_use
            try :
                self.ser.open()
                # clear buffers of stale data
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                bytes = b"ID\r\n"
                self.ser.write(bytes)
                id_string = self.ser.readline().decode()
                id_string = id_string.replace("OK","")
                print(Fore.RESET + id_string)
                retval = True
            except Exception as e:
                print(Fore.RED + f"\tException occured opening {port_to_use}")
                print(Fore.RED + f"\t{e}")
                retval = False
        else :
            print(Fore.RED + "\tEyeBERT relay board not found.")
            retval = False

        return retval
    
    # blink the LEDs as a test
    # blocking function due to time.sleep()
    def Blinky(self,count=3) :
        if self.blinkOK == True :
            blinkcount = count
            if blinkcount < 2 :
                blinkcount = 2
            elif blinkcount > 10 :
                blinkcount = 10
            duration = 0.1
            #print("Blinking LEDs 2 & 3 {} times".format(blinkcount))
            on2 = b"LED 2 ON\r\n"
            off2 = b"LED 2 OFF\r\n"
            on3 = b"LED 3 ON\r\n"
            off3 = b"LED 3 OFF\r\n"
            self.ser.write(off2)
            self.ser.write(on3)
            for i in range(blinkcount) :
                self.ser.write(on2)
                self.ser.write(off3)
                time.sleep(duration)
                self.ser.write(off2)
                self.ser.write(on3)
                time.sleep(duration)
            self.ser.write(off2)
            self.ser.write(off3)
        else :
            pass

    # request a TX or RX connection
    # path contains a string such as "TX 0\r\n"
    def connection(self, path) :
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(path)
        
    def LED(self, whichled, ledstate) :
        if self.blinkOK == True :
            # error checking
            if (whichled == 2 or whichled == 3) and (ledstate.upper() == "ON" or ledstate.upper() == "OFF" )  :
                cmd = b"LED " + bytes(str(whichled), 'utf-8') + b" " + bytes(ledstate, 'utf-8') + b"\r\n"
                #print(cmd)
                self.ser.write(cmd)
        else :
            pass

    def MODE(self, modestr) :
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(modestr.upper());

#
# how to step through entries in connection dictionary
#
def testV_45_33(obj,type) :
    keys = list(type.keys())
    print(keys)
    for x in keys :
        print("Testing {} path".format(x))
        txpath = b"tx " + bytes(type[x]['tx'], 'utf-8') + b"\r\n"
        rxpath = b"rx " + bytes(type[x]['rx'], 'utf-8') + b"\r\n"
        obj.connection(txpath)
        time.sleep(0.1)
        obj.connection(rxpath)
        obj.LED(2,"ON")
        time.sleep(5) # actual testing occurs here, time delay is dummy
        obj.LED(2,"OFF")
    obj.LED(2,"OFF")

def main():
    #
    # test code
    # 
    print("Running test code...")

    # create instance & continue if relay board found
    eb = EyeBERTRelayControl()
    if eb.initialize() == False :
        print("Terminating code 1")
        sys.exit(1)

    # blink some LEDs
    print("Das Blinkin Lights!")
    eb.Blinky(5)

    # a sample test could be like this call
    print("Testing sample paths...")
    cmd = b"MODE DMM +\r\n"
    eb.MODE(cmd)
    testV_45_33(eb, typeV_45_33)

    print("Done.")

if __name__ == "__main__":
    main()
