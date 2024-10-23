# WireLengthCalculator.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Wire Length Calculator
# Author:   Caleb Smith
# Date:     October 23, 2024
# -------------------------- #

import script_tools
from colorama import Fore, Back, Style, init

# Wire Length Calculator
class WireLengthCalculator:
    def __init__(self, wiring_type, length_type, loss, line_length):
        self.wiring_type    = wiring_type
        self.length_type    = length_type
        self.loss           = loss
        self.line_length    = line_length
        # set up cable info
        self.SetupCableInfo()
    
    # set up cable info
    def SetupCableInfo(self):
        # cable branches based on wiring type
        self.cable_branches = {
            "3.2" : ["A", "B", "C"],
            "2.2" : ["A", "C"],
            "2.3" : ["A", "B"],
            "1.3" : ["A"]
        }

        # number of channels per branch based on wiring type
        self.cable_channels_per_branch = {
            "3.2" : 3,
            "2.2" : 3,
            "2.3" : 4,
            "1.3" : 4
        }

        # cable lengths (mm) from Design B (Axel Filenius, March 1, 2024)
        self.cable_lengths = {
            # Ring 1 (R1)
            "2.3 R1_G1" : {"A" : 280, "B" : 280},
            "2.3 R1_G2" : {"A" : 275, "B" : 330},
            "1.3 R1_G3" : {"A" : 390},
            # Ring 2 (R2)
            "2.3 R2_G1" : {"A" : 200, "B" : 240},
            "2.3 R2_G2" : {"A" : 275, "B" : 330},
            "2.3 R2_G3" : {"A" : 275, "B" : 330},
            "2.3 R2_G4" : {"A" : 337, "B" : 377},
            # Ring 3 (R3)
            "3.2 R3_G1" : {"A" : 200, "B" : 215, "C": 310},
            "3.2 R3_G2" : {"A" : 365, "B" : 435, "C": 510},
            # Ring 4 (R4)
            "3.2 R4_G1" : {"A" : 190, "B" : 200, "C": 235},
            "3.2 R4_G2" : {"A" : 230, "B" : 275, "C": 315},
            "2.2 R4_G3" : {"A" : 360, "C" : 405},
        }

        # supported wiring types
        self.wiring_types = list(self.cable_branches.keys())

        # supported full types (wiring + length)
        self.full_types = list(self.cable_lengths.keys())

    # calculate wire length for one e-link
    def CalcWireLengthElink(self):
        wire_length_elink = -1
        full_type = ""
        branches = []
        branch_lengths = {}
        
        # check if wiring type is valid
        wiring_type_is_valid = script_tools.group_contains_element(self.wiring_types, self.wiring_type)
        if wiring_type_is_valid:
            # assign branches
            branches = self.cable_branches[self.wiring_type]
        else:
            # print error messages and return
            print(Fore.RED + f"ERROR: {self.wiring_type} is not a valid wiring type." + Fore.RESET)
            print(Fore.RED + f"Please enter a valid wiring type from this list:" + Fore.RESET)
            print(Fore.RED + f"{self.wiring_types}" + Fore.RESET)
            return wire_length_elink
        
        # get full type (wiring + length)
        full_type = "{0} {1}".format(self.wiring_type, self.length_type)
        
        # check if full type (wiring + length) is valid
        full_type_is_valid = script_tools.group_contains_element(self.full_types, full_type)
        if full_type_is_valid:
            # assign branch lengths
            branch_lengths = self.cable_lengths[full_type]
        else:
            # print error messages and return
            print(Fore.RED + f"ERROR: {full_type} is not a valid e-link type (defined by wiring and length)." + Fore.RESET)
            print(Fore.RED + f"Please enter a valid combination of e-link wiring and length types from this list:" + Fore.RESET)
            print(Fore.RED + f"{self.full_types}" + Fore.RESET)
            return wire_length_elink
        
        # get number of channels per branch
        n_channels_per_branch = self.cable_channels_per_branch[self.wiring_type]
        
        print(f" - full_type: {full_type}")
        print(f" - branches: {branches}")
        print(f" - n_channels_per_branch: {n_channels_per_branch}")
        print(f" - branch_lengths: {branch_lengths}")
        script_tools.printLine(self.line_length)

        # calculate wire length for one e-link
        wire_length_elink = 0
        for branch in branches:
            branch_length = branch_lengths[branch]
            length_to_add = n_channels_per_branch * (branch_length + self.loss)
            wire_length_elink += length_to_add
        return wire_length_elink

    # calculate wire length for a batch of n e-links
    def CalcWireLengthBatch(self, n_elinks, wire_length_elink):
        wire_length_batch = n_elinks * wire_length_elink
        return wire_length_batch

