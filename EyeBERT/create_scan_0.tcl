remove_hw_sio_scan [get_hw_sio_scans {SCAN_0}]



set xil_newScan [create_hw_sio_scan -description {Scan 0} 2d_full_eye  [lindex [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX] 0 ]]

set_property VERTICAL_INCREMENT {10} [get_hw_sio_scans $xil_newScan]