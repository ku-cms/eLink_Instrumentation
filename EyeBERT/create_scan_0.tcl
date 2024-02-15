remove_hw_sio_scan [get_hw_sio_scans {SCAN_0}]

# copy paste test from Vivado... 
#set_property TXDIFFSWING {741 mV (0111)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#commit_hw_sio -non_blocking [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#set_property TXDIFFSWING {924 mV (1010)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#commit_hw_sio -non_blocking [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#set_property TXDIFFSWING {973 mV (1011)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]
#commit_hw_sio -non_blocking [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {Link_Group_0}]]

# Choose the TXDIFFSWING setting:

# set TXDIFFSWING to "741 mV (0111)"
#set_property TXDIFFSWING {741 mV (0111)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
#commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

# set TXDIFFSWING to "924 mV (1010)"
#set_property TXDIFFSWING {924 mV (1010)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
#commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

# set TXDIFFSWING to "973 mV (1011)"
set_property TXDIFFSWING {973 mV (1011)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

# set TXDIFFSWING to "1018 mV (1100)"
#set_property TXDIFFSWING {1018 mV (1100)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
#commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

set xil_newScan [create_hw_sio_scan -description {Scan 0} 2d_full_eye  [lindex [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203AE483DA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX] 0 ]]
set_property VERTICAL_INCREMENT {10} [get_hw_sio_scans $xil_newScan]
