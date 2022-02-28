#!/usr/bin/env python

from readVNADataSKRF import plot

# WARNING:
# Write file names ending in .vna
# Do not include .txt (do not use .vna.txt)

options = [
            #['Redo_VNA', 'TP_1p4m_35_ChD0.vna'],
            #['Redo_VNA', 'TP_1p4m_35_ChD1_redo_v1.vna'],
            #['Redo_VNA', 'TP_1p4m_35_ChCMD_redo_v1.vna'],

            #['Redo_VNA', 'TP_35cm_60_ChD0_redo.vna'],
            #['Redo_VNA', '082820_TP_60_35cm_ChD1_KA.vna'],
            #['Redo_VNA', 'TP_35cm_60_ChCMD_redo.vna'],
            
            # using Cu calibration plate
            #['data', '9_feb_2021_test1_1.vna'],
            #['data', '9_feb_2021_test1_2.vna'],
            #['data', '9_feb_2021_test1_3.vna'],
            #['data', '9_feb_2021_test1_4.vna'],
            #['data', '9_feb_2021_test1_5.vna'],
            
            # cable 100
            #['data', 'TP_35cm_100_test1_1.vna'],
            
            # calibration
            #['data', 'calibration_test.vna'],
            #['data', 'small_SMA.vna'],
            #['data', 'straight_SMA.vna'],
            
            # cable 129
            #['data', 'TP_0p35m_129_ChCMD.vna'],
            #['data', 'TP_0p35m_129_ChD0.vna'],
            #['data', 'TP_0p35m_129_ChD1.vna'],
            #['data', 'TP_0p35m_129_ChD2.vna'],
            #['data', 'TP_0p35m_129_ChD3.vna'],

            # cable 100
            # CMD_v1: CMD on 33pin conenctions: VNA 1 to CMD_P (12), VNA 2 to CMD_N (13)
            # CMD_v2: CMD on 33pin conenctions: VNA 1 to CMD_D (13), VNA 2 to CMD_P (12)
            #['data', 'TP_35cm_100_33pin_CMD_v2.vna'],
            #['data', 'TP_35cm_100_33pin_D0.vna'],
            #['data', 'TP_35cm_100_33pin_D1.vna'],
            #['data', 'TP_35cm_100_33pin_D2.vna'],
            #['data', 'TP_35cm_100_33pin_D3.vna'],

            # John's cable number 1
            # loopback cable, 45 pin
            #['data', 'loopback_45pin_36tpi_27tpi.vna'],
            #['data', 'loopback_45pin_18tpi_9tpi.vna'],
            
            # John's cable number 2
            # 33 pin to 45 pin: 0, 2, 4, 6, 8 twists per inch
            #['data', 'TP_trial2_0tpi.vna'],
            #['data', 'TP_trial2_2tpi.vna'],
            #['data', 'TP_trial2_4tpi.vna'],
            #['data', 'TP_trial2_6tpi.vna'],
            #['data', 'TP_trial2_8tpi.vna'],
            #['data', 'TP_JohnCable2_0tpi_run1.vna'],
            #['data', 'TP_JohnCable2_0tpi_run2.vna'],
            #['data', 'TP_JohnCable2_0tpi_run3.vna'],
            #['data', 'TP_JohnCable2_2tpi_run1.vna'],
            #['data', 'TP_JohnCable2_2tpi_run2.vna'],
            #['data', 'TP_JohnCable2_2tpi_run3.vna'],
            #['data', 'TP_JohnCable2_4tpi_run1.vna'],
            #['data', 'TP_JohnCable2_4tpi_run2.vna'],
            #['data', 'TP_JohnCable2_4tpi_run3.vna'],
            #['data', 'TP_JohnCable2_6tpi_run1.vna'],
            #['data', 'TP_JohnCable2_6tpi_run2.vna'],
            #['data', 'TP_JohnCable2_6tpi_run3.vna'],
            #['data', 'TP_JohnCable2_8tpi_run1.vna'],
            #['data', 'TP_JohnCable2_8tpi_run2.vna'],
            #['data', 'TP_JohnCable2_8tpi_run3.vna'],
            
            # John's cable number 3
            # Length: 2 m
            # Channels: 4, 4*, 8, 8*, 16
            #['data', 'johncable3_2m_4.vna'],
            #['data', 'johncable3_2m_4star.vna'],
            #['data', 'johncable3_2m_8.vna'],
            #['data', 'johncable3_2m_8star.vna'],
            #['data', 'johncable3_2m_16.vna'],

            # John's cable number 4
            # Length: 1 m
            # Channels: 4J, 4B, 8, 16, 24
            #['data', 'johncable4_Bill4tpi.vna'],
    
            # Cable 120 (Before Lashing)
            ['TP_0.8m_120_M1CMD.vna',       'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M1CMD_run2.vna',  'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M1D0.vna',        'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M1D1.vna',        'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M2CMD.vna',       'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M2D0.vna',        'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M2D1.vna',        'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M2D1_run2.vna',   'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M3CMD.vna',       'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M3D0.vna',        'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            ['TP_0.8m_120_M3D1.vna',        'data/Cable_120_beforeLashing', 'plots/Cable_120_beforeLashing'],
            
            # Cable 120 (After Lashing)
            ['TP_0.8m_120_M1CMD.vna',       'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M1D0.vna',        'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M1D1.vna',        'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M2CMD.vna',       'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M2D0.vna',        'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M2D1.vna',        'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M3CMD.vna',       'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M3CMD_run2.vna',  'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M3D0.vna',        'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            ['TP_0.8m_120_M3D1.vna',        'data/Cable_120_afterLashing', 'plots/Cable_120_afterLashing'],
            
            # Cable 158 (Before Lashing)
            ['TP_1p6m_158_CMD.vna',             'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_CMD_swap12.vna',      'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_CMD_1to2_3to4.vna',   'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D0.vna',              'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D0_swap12.vna',       'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D0_1to2_3to4.vna',    'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D1.vna',              'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D1_run2.vna',         'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D1_swap12.vna',       'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D2.vna',              'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D2_run2.vna',         'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D2_swap12.vna',       'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D3.vna',              'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            ['TP_1p6m_158_D3_swap12.vna',       'data/Cable_158_beforeLashing', 'plots/Cable_158_beforeLashing'],
            
            # testing breaks (3, 4 disconnected; 1, 2, 3, 4 disconnected)
            #['break_34.vna',   'data', 'plots'],
            #['break_1234.vna', 'data', 'plots'],
            
]

for opt in options:
    basename        = opt[0]
    data_directory  = opt[1]
    plot_directory  = opt[2]
    plot(basename, data_directory, plot_directory)

