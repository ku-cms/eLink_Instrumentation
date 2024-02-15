source create_scan_0.tcl
set_property DESCRIPTION 551_d3 [get_hw_sio_scans SCAN_0]
run_hw_sio_scan [lindex [get_hw_sio_scans {SCAN_0}] 0]
wait_on_hw_sio_scan [lindex [get_hw_sio_scans {SCAN_0}] 0]
write_hw_sio_scan -force "C:/Users/Public/Documents/automation_results/temp.csv" [get_hw_sio_scans {SCAN_0}]
