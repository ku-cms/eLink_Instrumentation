# assign firmware file name (bit file)
set first_bit_file "C:/Users/Public/Documents/cable_tests/cable_test_705.bit"

# go to the project directory
cd "C:/Users/Public/Documents/cable_tests/"

# start the GUI so we can see pretty pictures
start_gui

# start the hardware manager and open target
open_hw_manager
connect_hw_server
set my_hw_target [get_hw_targets *]
current_hw_target $my_hw_target
open_hw_target

# program the first bit file that sets the 128MHz reference clock
set first_hw_device [lindex [get_hw_devices] 0]
current_hw_device $first_hw_device
set_property PROGRAM.FILE $first_bit_file $first_hw_device
program_hw_devices $first_hw_device

refresh_hw_device [lindex [get_hw_devices xc7k325t_0] 0]

# setup links
set xil_newLinks [list]
set xil_newLink [create_hw_sio_link -description {Link 0} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLinkGroup [create_hw_sio_linkgroup -description {Link Group 0} [get_hw_sio_links $xil_newLinks]]
unset xil_newLinks

# assign link settings
set_property TXPRE {0.00 dB (00000)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
set_property TXPOST {0.00 dB (00000)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

set_property TXDIFFSWING {741 mV (0111)} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

set_property TX_PATTERN {PRBS 7-bit} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
set_property RX_PATTERN {PRBS 7-bit} [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]

# the commit_hw_sio command is only required once at the end to apply the link settings
commit_hw_sio -non_blocking [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/TX->localhost:3121/xilinx_tcf/Digilent/210203A3CE0EA/0_1_0/IBERT/Quad_117/MGT_X0Y8/RX}]
