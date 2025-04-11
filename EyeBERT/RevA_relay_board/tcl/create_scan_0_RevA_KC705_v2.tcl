remove_hw_sio_scan [get_hw_sio_scans {SCAN_0}]

# Set the TXDIFFSWING setting:

# Setting for manual 
# set TXDIFFSWING to "741 mV (0111)"
#set_property TXDIFFSWING {741 mV (0111)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
#commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

# Setting for Rev A relay board
# set TXDIFFSWING to "1018 mV (1100)"
set_property TXDIFFSWING {1018 mV (1100)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

# Set TX Pre-Cursor setting:

# Set TX Pre-Cursor to "0.00 dB (00000)"
set_property TXPRE {0.00 dB (00000)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
commit_hw_sio -non_blocking [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]

# Set TX Pre-Cursor to "4.44 dB (10000)"
#set_property TXPRE {4.44 dB (10000)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#commit_hw_sio -non_blocking [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]

# Set TX Pre-Cursor to "6.02 dB (11111)"
#set_property TXPRE {6.02 dB (11111)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#commit_hw_sio -non_blocking [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]

# Create new scan 
set xil_newScan [create_hw_sio_scan -description {Scan 0} 2d_full_eye  [lindex [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CFC8A/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX] 0 ]]
set_property VERTICAL_INCREMENT {10} [get_hw_sio_scans $xil_newScan]
