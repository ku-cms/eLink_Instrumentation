# EyeBertAutomation.py
#
# Developed by the KU CMS group.
#
# Authors:
# - Rob Young
# - Nora Manolescu
# - Caleb Smith
#
# Used for the following measurements for twisted pair electrical links (e-links):
#
# 1. Performs 4-point DC resistance measurements of all e-link channels (both positive and negative wires)
#    using a Keithley, relay boards, SMA cables, and adapter boards.
#    Saves 4-point DC resistance measurement results.
#    Includes functionality for calibrating 4-point DC resistance for every e-link channel.
#
# 2. Performs "Eye BERT" area measurements (including eye-diagram template analysis) of all e-link channels (each differential pair)
#    using pyautogui to control the Vivado "Eye BERT" program, where the hardware setup is a KC705, relay boards, SMA cables, and adapter boards.
#    Saves eye-diagram and template analysis plots and records open area, height, and template analysis results.
#
# To Do : Add appending to XLS file with various cable info
#       : Get cable specifics from operator
#       : repeat tests as needed
#       : much better error recovery & data validation!

version = 1.11

from template_analysis_windows import EyeBERTFile, Reference
from colorama import Fore, Back, Style, init

init(convert=True)
print(Fore.GREEN + "KU-CMS KC705 EyeBERT Automated Test")
print(f"Version {version:.2f}")
print(Fore.RESET + "Loading libraries...")

import pyautogui as pygui
import csv
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import datetime
import os
import shutil
import time
import sys
import ctypes
from pathvalidate import is_valid_filename
import eyebertserial
import dmmserial
import json

def main():
    # parameters
    verbose = False
    RUN_4PT_DC_RES_CALIBRATION  = True
    RUN_4PT_DC_RES              = False
    RUN_EYE_BERT_AREA           = False
    pygui.PAUSE = 0.5
    test_results = {}

    #
    # The e-link connection mapping is defined by a dictionary
    # - Define e-link mappings as needed
    # - Use the desired e-link mapping
    #

    # SMA cables: testing in loopback mode
    mapping_SMA_test = {
        "name" : "example",
        "cmd" : {"tx" : "0", "rx" : "0"},
        "d0"  : {"tx" : "3", "rx" : "3"}
    }

    # Type 1 e-links
    mapping_type1 = {
        "name" : "type 1 tfpix",
        "cmd" : {"tx" : "7", "rx" : "7"},
        "d0"  : {"tx" : "0", "rx" : "0"},
        "d1"  : {"tx" : "1", "rx" : "1"},
        "d2"  : {"tx" : "2", "rx" : "2"},
        "d3"  : {"tx" : "3", "rx" : "3"}
    }

    # Type 5 e-links
    mapping_type5 = {
        "name" : "type 5 tbpix",
        "cmd" : {"tx" : "7", "rx" : "7"},
        "d0"  : {"tx" : "0", "rx" : "0"},
        "d1"  : {"tx" : "1", "rx" : "1"},
        "d2"  : {"tx" : "2", "rx" : "2"},
        "d3"  : {"tx" : "3", "rx" : "3"}
    }

    # Choose e-link mapping:
    cable_mapping = mapping_type5
    print(Fore.GREEN + "Mapping Dictionary : " + Fore.RED + 
        cable_mapping["name"] + Fore.GREEN + " selected.")

    #
    # open serial control of relay board
    #
    eb = eyebertserial.EyeBERTRelayControl()
    if eb.initialize() == False :
        print(Fore.RED + "Terminating code 1 eyebert relay init")
        sys.exit(1)
    eb.Blinky(5)

    #
    # open dmm
    # 
    dmm = None
    if RUN_4PT_DC_RES or RUN_4PT_DC_RES_CALIBRATION:
        dmm = dmmserial.Keithley2000DMMControl()
        if dmm.initialize() == False :
            print(Fore.RED + "Terminating code 1 DMM init")
            sys.exit(1)

    #
    # get operator name/initials
    #
    operator = input(Fore.RED + "Enter operator name: " + Fore.GREEN)
    operator = operator.strip()
    while operator == "" :
        operator = input(Fore.RED + "Enter operator name: " + Fore.GREEN)
        operator = operator.strip()

    #operator = operator.upper()

    #
    # get a valid cable name to use as directory and root filename
    #
    file_path = "C:/Users/Public/Documents/automation_results"
    r_file_path = "R:/BEAN_GRP/EyeBERTAutomation/automation_results"
    is_valid = False
    while is_valid == False :
        filename = input(Fore.RED + "Enter cable name: " + Fore.GREEN)
        is_valid = is_valid_filename(filename)
        if is_valid == False :
            print(Fore.RED + f"{filename} cannot be used as a directory or filename. Re-enter.")

    # Assume that the filename is the cable number
    cable = filename
    
    #
    # get ready to use this as our destination path
    #
    cable_path = file_path + "/" + filename
    r_cable_path = r_file_path + "/" + filename
    isExist = os.path.exists(cable_path)
    if isExist == False :
        # create the path
        os.makedirs(cable_path)

    isExist = os.path.exists(r_cable_path)
    if isExist == False :
        #create the path
        os.makedirs(r_cable_path)
        
    #
    # get serial number of test boards
    #
    left_serialnumber = input(Fore.RED + "Enter SN of left board: " + Fore.GREEN)
    left_serialnumber = left_serialnumber.strip()
    while left_serialnumber == "" :
        left_serialnumber = input(Fore.RED + "Enter SN of left board: " + Fore.GREEN)
        left_serialnumber = left_serialnumber.strip()

    right_serialnumber = input(Fore.RED + "Enter SN of right board: " + Fore.GREEN)
    right_serialnumber = right_serialnumber.strip()
    while right_serialnumber == "" :
        right_serialnumber = input(Fore.RED + "Enter SN of right board: " + Fore.GREEN)
        right_serialnumber = right_serialnumber.strip()
        
    left_serialnumber = left_serialnumber.upper()
    right_serialnumber = right_serialnumber.upper()
        
    #
    # brief operator notes
    #
    operator_notes = input(Fore.RED + "Operator notes: " + Fore.GREEN)

    #
    # guarantee caps lock is off
    #
    if ctypes.WinDLL("User32.dll").GetKeyState(0x14) :
        print(Fore.RED + "CAPSLOCK is on - turning off." + Fore.RESET)
        pygui.press('capslock')

    keys = list(cable_mapping.keys())

    if RUN_4PT_DC_RES_CALIBRATION:
        print("")
        print("Running 4-point DC resistance calibration.")
        print("")
    elif RUN_4PT_DC_RES or RUN_EYE_BERT_AREA:
        print("")
        print(f"Taking data for cable {cable}.")
        print("")
    else:
        print("")
        print("Nothing to do (based on run flags)...")
        print("")

    # 4-point DC resistance calibration
    if RUN_4PT_DC_RES_CALIBRATION:
        print("--------------------------------------------")
        print("Beginning 4-point DC resistance calibration.")
        print("--------------------------------------------")

        calibration_data = {}
        calibration_file = "4_point_DC_Calibration_v1.json"

        print(f"Calibration data will be saved to {calibration_file}. This file will be overwritten.")
        
        # Confirm that user wants to continue
        user_accept = input(Fore.RED + "Would you like to continue? [y/n]: " + Fore.GREEN)
        if user_accept.lower() == "y":
            print("Proceeding with calibration. Please connect through lines for each channel as instructed.")
        else:
            print("Exiting...")
            print(Fore.RED + "Terminating code 3: exit based on user input.")
            sys.exit(3)
        
        for key in keys :
            # skip key if it is "name"
            if key == "name" :
                continue
            # otherwise, we assume that the key is the channel
            else:
                channel = str(key)

            # get TX and RX paths from cable mapping
            txpath = b"tx " + bytes(cable_mapping[key]['tx'], 'utf-8')
            rxpath = b"rx " + bytes(cable_mapping[key]['rx'], 'utf-8')

            # pause for user to connect through lines (P to P and N to N) for channel
            print(Fore.RED + f"Please connect through lines (P to P and N to N) for channel {key}: txpath = {txpath.decode()} and rxpath = {rxpath.decode()}." + Fore.GREEN)
            user_ready = input(Fore.RED + f"Press enter when ready. " + Fore.GREEN)

            # take measurements; do not subtract anything
            eb.connection(txpath+b"\r\n")
            eb.connection(rxpath+b"\r\n")
            eb.LED(2,"ON")
            eb.MODE(b"MODE DMM +\r\n")
            print(f" - path {key}",end="")
            positive = round(dmm.reading(),2)
            eb.MODE(b"MODE DMM -\r\n")
            negative = round(dmm.reading(),2) 
            print(" DMM + ", end="")
            print("%.2f" % positive, end="")
            print(" DMM - ", end="")
            print("%.2f" % negative)

            # save data
            calibration_data[key + "_p"] = positive
            calibration_data[key + "_n"] = negative

        # Save calibration data to json file
        print(f"Saving calibration data to {calibration_file}.")
        with open(calibration_file, "w") as write_file:
            json.dump(calibration_data, write_file, indent=4)
        
        print("The calibration is complete!")
        print("Exiting...")
        sys.exit(4)

    # 4-point DC resistance measurements
    if RUN_4PT_DC_RES:
        print("---------------------------------------------")
        print("Beginning 4-point DC resistance measurements.")
        print("---------------------------------------------")

        calibration_data = {}
        calibration_file = "4_point_DC_Calibration_v1.json"

        print(f"Using the calibration file {calibration_file}.")
        
        # Load calibration data from json file
        with open(calibration_file, "r") as read_file:
            calibration_data = json.load(read_file)

        #pos_path = +1.05040543 # quick single point cal of cables + relay paths
        #neg_path = +1.01958215 # quick single point cal of cables + relay paths
        #pos_path = 1.05 # rounded 2 places
        #neg_path = 1.02 # rounded 2 places
        
        for key in keys :
            # skip key if it is "name"
            if key == "name" :
                continue
            # otherwise, we assume that the key is the channel
            else:
                channel = str(key)
            
            # get calibration data for channel (for both P and N lines)
            pos_path = calibration_data[key + "_p"]
            neg_path = calibration_data[key + "_n"]
            
            # get TX and RX paths from cable mapping
            txpath = b"tx " + bytes(cable_mapping[key]['tx'], 'utf-8')
            rxpath = b"rx " + bytes(cable_mapping[key]['rx'], 'utf-8')

            # take measurements and subtract calibration values
            # just reporting results to screen for now
            eb.connection(txpath+b"\r\n")
            eb.connection(rxpath+b"\r\n")
            eb.LED(2,"ON")
            eb.MODE(b"MODE DMM +\r\n")
            print(f" - path {key}",end="")
            positive = round(dmm.reading(),2) - pos_path
            eb.MODE(b"MODE DMM -\r\n")
            negative = round(dmm.reading(),2) - neg_path
            print(" DMM + ", end="")
            print("%.2f" % positive, end="")
            print(" DMM - ", end="")
            print("%.2f" % negative)

    # Eye BERT area measurements
    if RUN_EYE_BERT_AREA:
        print("-------------------------------------")
        print("Beginning Eye BERT area measurements.")
        print("-------------------------------------")

        eb.MODE(b"MODE KC705\r\n")
        for key in keys :
            # skip key if it is "name"
            if key == "name" :
                continue
            # otherwise, we assume that the key is the channel
            else:
                channel = str(key)
            temp_name = filename + "_" + str(key) # change for looping version
            test_name = temp_name.replace(" ", "_")
            txpath = b"tx " + bytes(cable_mapping[key]['tx'], 'utf-8')
            rxpath = b"rx " + bytes(cable_mapping[key]['rx'], 'utf-8')
            
            print(Fore.GREEN + Style.BRIGHT + f"{test_name}" + Style.NORMAL)
            print(Fore.GREEN + f"\ttxpath = {txpath.decode()}")
            print(Fore.GREEN + f"\trxpath = {rxpath.decode()}")

            eb.connection(txpath+b"\r\n")
            eb.connection(rxpath+b"\r\n")
            eb.LED(2,"ON")

            # if old temp.csv exists, erase
            if os.path.exists(file_path+"/temp.csv") :
                os.remove(file_path+"/temp.csv")

            # makes assumption that EyeBERT KC704 (Vivado) is already running
            # with bitstream loaded
            # guarantee it is maximized and has focus
            try :
                pygui.getWindowsWithTitle("Vivado 2020.2")[0].maximize()
                time.sleep(0.5)
                pygui.getWindowsWithTitle("Vivado 2020.2")[0].activate()
                time.sleep(0.5)
                # send F5 to reset layout of Vivado
                pygui.press('f5')
            except :
                print(Fore.RED + "Vivado 2020.2 and EyeBert bitstream not running")
                print(Fore.RED + "Terminating code 2" + Fore.RESET)
                sys.exit(2)

            # create custom "source eye_and_save.tcl" with the cable name & path included
            eye_and_save = "C:/Users/Public/Documents/cable_tests/eye_and_save.tcl"
            with open (eye_and_save, 'w') as f :
                f.write("source create_scan_0.tcl\r\n")
                f.write(f"set_property DESCRIPTION {test_name} [get_hw_sio_scans SCAN_0]\r\n")
                f.write("run_hw_sio_scan [lindex [get_hw_sio_scans {SCAN_0}] 0]\r\n")
                f.write("wait_on_hw_sio_scan [lindex [get_hw_sio_scans {SCAN_0}] 0]\r\n")
                f.write('write_hw_sio_scan -force "C:/Users/Public/Documents/automation_results/temp.csv" [get_hw_sio_scans {SCAN_0}]\r\n')

            # send tcl "source eye_and_save.tcl"
            result = pygui.locateCenterOnScreen('tcl_console.png', grayscale=True)
            if result == None :
                result = pygui.locateCenterOnScreen('light_tcl_console.png', grayscale=True)

            if result == None :
                # handle error
                print(Fore.RED + "Unable to locate TCL Console tab.")
                sys.exit(9)

            pygui.click(result) # bring tab to focus
            time.sleep(0.25)
            pygui.press('tab') # move focus to text entry box of tab
            time.sleep(0.25)

            # launch the test via TCL script
            pygui.write("source eye_and_save.tcl\n", interval = 0.01)

            # wait a bit
            print(Fore.GREEN + "Pausing to allow EyeBERT to complete...")
            time.sleep(15)

            # loop looking for temp.csv
            print(Fore.GREEN + "Waiting for data file from Vivado...")
            time_to_wait = 20
            time_counter = 0
            while not os.path.exists(file_path+"/temp.csv") :
                time.sleep(1)
                time_counter += 1
                if time_counter > time_to_wait : break

            eb.LED(2,"OFF")

            # get data
            print(Fore.GREEN + "Parsing CSV file for test results...")
            open_area = -999.9
            with open(file_path+"/temp.csv", 'r') as file :
                csvreader = csv.reader(file, delimiter=',')
                # find the Open Area
                for row in csvreader :
                    if row[0] == "Open Area" :
                        open_area = int(row[1])
                        break

            with open(file_path+"/temp.csv", 'r') as file :
                search = list(csv.reader(file)) # convert to a list we can index through
                # find the top of eye
                top_of_eye = -999.9 # nonsense values
                # use column AH, start at row 22
                for r in range(21, 45, 1) :
                    value = float(search[r][33])
                    if value < 2.0e-7 : 
                        # we have found it
                        top_of_eye = float(search[r-1][0])
                        break
                # find the bottom of eye
                bottom_of_eye = 999.9
                for r in range(44, 20, -1) :
                    value = float(search[r][33])
                    if value < 2.0e-7 :
                        # we found it!
                        bottom_of_eye = float(search[r+1][0])
                        break

            print(Fore.GREEN + Style.BRIGHT + f" - Open area = {open_area}")
            print(Fore.GREEN + f" - top_of_eye = {top_of_eye}")
            print(Fore.GREEN + f" - bottom_of_eye = {bottom_of_eye}" + Style.NORMAL)

            src = file_path+"/temp.csv"
            dest = cable_path + "/" + test_name + ".csv"
            # check if destionation already exists
            counter = 2
            while os.path.exists(dest) == True :
                dest = cable_path + "/" + test_name + "_" + str(counter) + ".csv"
                counter = counter + 1

            os.rename(src,dest)

            # Copy data csv file to R drive
            copyfilename = dest.replace(file_path+"/","")
            newdest = r_file_path + "/" + copyfilename
            if verbose:
                print(f"data path (1): {dest}")
                print(f"data path (2): {newdest}")
            shutil.copyfile(dest, newdest)
            
            # EyeBERT Template Analysis

            reference_template_file = "reference_template_v2.csv"
            print(f"Using this reference template data file: {reference_template_file}")
            
            # Create EyeBERTFile object, cleaning user input, to read data from file
            eyebert = EyeBERTFile(cable.replace(" ", ""), channel.replace(" ", "").lower(), file_path)
            # Call analyze method to obtain graphs and properties
            analysis = eyebert.analyze()

            # Warning: .getPath() must be called AFTER .analyze()
            refPath = eyebert.getPath()

            analysis.setPath(refPath)

            if analysis.verify(): # Only continue if template passes verifcation

                template = analysis.createTemplate()

                ref = Reference("540", "CMD", reference_template_file, refPath)
                refTemp = ref.createTemplate()
                
                # EDIT: reference needs to be a template object
                template.plot(refTemp) 
                print("\n")
                
                # Get template analysis results
                num_zeros   = template.getZeros()
                num_ones    = template.getOnes()
                out_points  = template.getOutCounts()
                in_points   = template.getInCounts()
            else:
                print(f"Error for cable {cable} and channel {channel.upper()}: Template failed verification step.")

            # Make the screen capture
            print(Fore.GREEN + "Creating screen capture...")
            pygui.moveTo(355,800)
            pygui.click()
            screenshot = cable_path + "/" + test_name + ".png"
            counter = 2
            while os.path.exists(screenshot) == True :
                screenshot = cable_path + "/" + test_name + "_" + str(counter) + ".png"
                counter = counter + 1

            # Save original screenshot 
            pygui.screenshot(screenshot,(360,190,1300,540))

            # Copy screenshot to the R drive
            copyfilename = screenshot.replace(file_path+"/","")
            newdest = r_file_path + "/" + copyfilename
            if verbose:
                print(f"screenshot path (1): {screenshot}")
                print(f"screenshot path (2): {newdest}")
            shutil.copyfile(screenshot, newdest)

            # Copy template plot to the R drive
            oldTemplatePath = refPath + "template_plots.pdf"
            endPath = oldTemplatePath.split("/automation_results/")[-1]
            newTemplatePath = r_file_path + "/" + endPath 
            if verbose:
                print(f"template plot path (1): {oldTemplatePath}")
                print(f"template plot path (2): {newTemplatePath}")
            shutil.copyfile(oldTemplatePath, newTemplatePath)
            
            # add results to dataset for future write
            now = datetime.datetime.now()
            channel_name = key
            test_results.update(
                {key : 
                {"test_name"    : test_name.replace("_"+channel_name,""),
                "channel"       : channel_name,
                "date"          : now.strftime("%Y-%m-%d"),
                "time"          : now.strftime("%H:%M:%S"),
                "open_area"     : open_area, 
                "top_eye"       : top_of_eye, 
                "bottom_eye"    : bottom_of_eye,
                "num_zeros"     : num_zeros,
                "num_ones"      : num_ones,
                "out_points"    : out_points,
                "in_points"     : in_points,
                "operator"      : operator,
                "left_SN"       : left_serialnumber, 
                "right_SN"      : right_serialnumber,
                "notes"         : operator_notes}
                }
            )
        #end keys loop

        # update XLS file, create new entries as needed
        wb = Workbook()
        file_name = "EyeBERTautomation.xlsx"
        path = "R:/BEAN_GRP/EyeBertAutomation/"
        keep_trying = True
        while keep_trying :
            try :
                os.rename(path + file_name, path + file_name)
                keep_trying = False
            except OSError:
                pygui.getWindowsWithTitle("Vivado 2020.2")[0].minimize()
                print(Fore.RED + "EyeBERTautomation.xlxs summary file is open. Please close")
                x=input(Fore.RED + "Press ENTER when ready to retry" + Fore.GREEN)
                keep_trying = True

        isExist = os.path.exists(path + file_name)
        if isExist == False :
            # create file
            print(Fore.LIGHTRED_EX + "\tXLSX summary file does not exist. Creating file.")
            ws = wb.active
            newdata = ["cable name", "channel", "date", "time", "open_area", "top_eye",
                       "bottom_eye", "num_zeros", "num_ones", "out_points", "in_points",
                       "operator", "left_SN", "right_SN", "notes"]
            ws.append(newdata)
            col = get_column_letter(1)
            ws.column_dimensions[col].bestFit = True
            wb.save(path + file_name)
        else :
            # load existing copy
            print(Fore.GREEN + "Opening XLSX summary file")
            wb = load_workbook(filename = path + file_name)
            ws = wb.active

        print(Fore.GREEN + "Adding data...")
        cablename = test_name
        keys = list(test_results)
        for key in keys :
            newdata = [test_results[key]["test_name"],
                    test_results[key]["channel"],
                    test_results[key]["date"],
                    test_results[key]["time"],
                    test_results[key]["open_area"],
                    test_results[key]["top_eye"],
                    test_results[key]["bottom_eye"],
                    test_results[key]["num_zeros"],
                    test_results[key]["num_ones"],
                    test_results[key]["out_points"],
                    test_results[key]["in_points"],
                    test_results[key]["operator"],
                    test_results[key]["left_SN"],
                    test_results[key]["right_SN"],
                    test_results[key]["notes"]]
            ws.append(newdata)
        col = get_column_letter(1)
        ws.column_dimensions[col].bestFit = True
        wb.save(path + file_name)

        pygui.getWindowsWithTitle("Vivado 2020.2")[0].minimize()
        print(Fore.GREEN + Style.BRIGHT + "Done!" + Fore.RESET + Style.RESET_ALL)

        #excel_start_return = os.system('start "excel" ' + path + file_name)

if __name__ == "__main__":
    main()
