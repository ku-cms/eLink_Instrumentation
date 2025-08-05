# Analysis

Use the Python script `analyzeElinkProduction.py` to create a cumulative e-link production plot.
Specify a start date (YYYY-MM-DD), an end date (YYYY-MM-DD), and an input file (.csv)
using the -a, -b, and -c flags, respectively.
```
cd Analysis
python3 python/analyzeElinkProduction.py -a START_DATE -b END_DATE -c INPUT_FILE
```

Here is an example using the start date `2024-04-01`, the end date `2025-07-31`,
and the input file `data/Harness_Serial_Number_2025_08_01.csv`.
```
cd Analysis
python3 python/analyzeElinkProduction.py -a 2024-04-01 -b 2025-07-31 -c data/Harness_Serial_Number_2025_08_01.csv
```

To create the input file (.csv), download the latest `Harness_Serial_Number.xlsx` Excel file
from our Microsoft Teams area (in `Documents > Cable production`).
You may rename the Excel file if desired (for example, adding a date and/or version number).
Move the Excel file to your working area (for example, `Analysis` or `Analysis/data`).
Open the Excel file and select the `Production` tab.
Then, use `Save As...` to export the `Production` tab as a Comma Separated Values (.csv) file.
You will receive a warning that the workbook cannot be saved as .csv because it contains multiple sheets.
Click OK to save only the active sheet to .csv.
Make sure to save (or move) the .csv to your working area (for example, `Analysis` or `Analysis/data`).

