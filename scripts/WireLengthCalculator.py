# WireLengthCalculator.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Wire Length Calculator
# Author:   Caleb Smith
# Date:     October 22, 2024
# -------------------------- #

class WireLengthCalculator:
    def __init__(self, wiring_type, length_type, loss):
        self.wiring_type    = wiring_type
        self.length_type    = length_type
        self.loss           = loss
        # set up cable info
        self.SetupCableInfo()

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

