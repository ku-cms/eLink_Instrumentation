import serial
import serial.tools.list_ports
import time
from colorama import Fore, init
import sys

init(convert=True) # for colorama to work correctly

class Keithley2000DMMControl:


    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.timeout = 1

    def __del__(self):
        self.ser.close()

    def FindDMM(self) :
        port_to_use = None
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports) :
            #print("{}: {} [{}]".format(port,desc,hwid))
            # change hwid string to match that of the USB to
            # serial adapter in use on the Keithley dmm
            if hwid == "USB VID:PID=0403:6001 SER=FTAJPEZEA" :
                port_to_use = port
                break
         
        return port_to_use

    def initialize(self) :
        # try and find instand of serial
        port_to_use = self.FindDMM()
        if port_to_use != None :
            print(Fore.GREEN + "Keithley 2000 DMM found on port {}".format(port_to_use))
            self.ser.port = port_to_use
            try :
                self.ser.open()
                # clear buffers of stale data
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                bytes = b"*ID\r\n"
                self.ser.write(bytes)
                id_string = self.ser.readline().decode()
                id_string = id_string.replace("OK","")
                print(Fore.RESET + id_string)
                bytes = b":system:frswitch?\r\n"
                self.ser.write(bytes)
                sw_string = self.ser.readline().decode()
                if int(sw_string) == 1 :
                    print("FRONT selected")
                else :
                    print("Change input switch to FRONT.")
                retval = True
            except Exception as e:
                print(Fore.RED + f"\tException occured opening {port_to_use}")
                print(Fore.RED + f"\t{e}")
                retval = False
        else :
            print(Fore.RED + "\tKeithley 2000 DMM not found.")
            retval = False

        if retval == True :
            bytes = b"*rst\r\n"
            self.ser.write(bytes)
            bytes = b":format:data ascii\r\n"
            self.ser.write(bytes)
            bytes = b":configure:fresistance\r\n"
            self.ser.write(bytes)
            #bytes = b":fres:nplc 1\r\n"
            #self.ser.write(bytes)
            bytes = b":fres:range 0\r\n"
            self.ser.write(bytes)

        return retval


    def reading(self) :
        # Important:
        # You must sleep (say 100 ms) before reading a value to wait for the relays to stop bouncing!
        # If you do not sleep, you may read infinite resistance!
        time.sleep(.1)
        bytes = b"read?\r\n"
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(bytes)
        read_string = self.ser.readline().decode()
        read_float = float(read_string)
        return read_float

#
# test code
#
# create instance & continue if relay board found
#eb = Keithley2000DMMControl()
#if eb.initialize() == False :
#    print("Terminating code 1")
#    sys.exit(1)

#val = eb.reading()
#print(val)
