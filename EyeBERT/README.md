# Eye BERT

This directory contains the necessary files to run Eye BERT scans on e-links
using a KC705, SMA cables, and yellow e-link to SMA adapter boards.
The project is designed to run on Windows 10 using Vivado 2020.2.
However, the project should be able to run on Linux with some modifications.

## First Time Setup

TODO: Fix typos in the TCL file and test:
- Change "firt_bit_file" to "first_bit_file".
- Change "targu" to "my_hw_target".

First, download this repository.
```
git clone https://github.com/ku-cms/eLink_Instrumentation.git
```

Then, create a new directory on your computer for the Eye BERT Vivado project.
Copy these files from the "EyeBERT" directory to the new project folder that you created:
```
eLink_Instrumentation/EyeBERT/Bert_Icon_v1.ico
eLink_Instrumentation/EyeBERT/Bert_Icon_v2.ico
eLink_Instrumentation/EyeBERT/cable_test_705.bit
eLink_Instrumentation/EyeBERT/run_test.bat
eLink_Instrumentation/EyeBERT/run_test.tcl
```

The Windows batch file (.bat) that is used to load the Vivado project is "run_test.bat".
To run on Linux, a similar bash script (.sh) could be created.
Here are the contents of "run_test.bat":
```
cd C:\Users\Public\Documents\cable_tests

d:\vivado\2020.2\bin\vivado.bat -mode batch -source run_test.tcl
exit
```
The paths in "run_test.bat" should be modified and set to the correct paths for your computer.
The first path `C:\Users\Public\Documents\cable_tests` should be set to the directory for the project that you created
(where run_test.bat, run_test.tcl, cable_test_705.bit, etc. are located).
The second path `d:\vivado\2020.2\bin\vivado.bat` should be set to the path of the Vivado 2020.2 executable
(in Windows, this is also a bat file).

Next, the TCL file "run_test.tcl" is used to setup the Vivado project. 

In "run_test.tcl", the path in this line should be changed to point to the path of the "cable_test_705.bit" file;
this bit file is the KC705 firmware for the Eye BERT project.
```
set firt_bit_file "C:/Users/Public/Documents/cable_tests/cable_test_705.bit"
```

In "run_test.tcl", the path in this line should be set to the project directory.
```
cd "C:/Users/Public/Documents/cable_tests/"
```

Then if using Windows, create a shortcut to "run_test.bat" file. 
Move the shortcut to the desktop.
Rename the shortcut to "Eye BERT".
Modify the shortcut properties to set the icon image to one of these files (take your pick):
- Bert_Icon_v1.ico
- Bert_Icon_v2.ico

## Running the Eye BERT Program

To run the Eye BERT program, first connect a KC705 to the computer.
Turn on the KC705.
Connect the KC705 P/N transmit and receive SMA ports using either SMA cables only (to verify the setup)
or SMA cables, yellow SMA to e-link adapter board, and an e-link (see further documentation for connection information). 
Then, double click on the desktop shortcut that you created for the "run_test.bat" file.
This should start Vivado, load the project, program the KC705, setup the link, and apply the settings.
Check that the link is stable. 
If the link is not stable, first try reseting the link.
If needed, close Vivado, power cycle the KC705, and try again.

Once a stable link is established, you can create and run a new scan to get an "Eye BERT" plot and area measurement.
To test all e-link channels, repeat the e-link connection for the desired channel and then create and run a new scan.
The KC705 only needs to be programmed once (using the desktop shortcut) after being powered on.


