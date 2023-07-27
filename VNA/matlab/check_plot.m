% take data from VNA
% compute a TDR based on the S4P file
% generate plots

version = "1.0";
close;
clc;
fprintf("Anritsu VNA Check Plot\n");
fprintf("   Version %s\n\n", version);

%
% open the serial port
%
sport = serialport('COM4', 57600, 'Timeout', 10);
configureTerminator(sport,'LF')
LF = 10;
SweepDelay = 2;
DataDelay = 2;

%
% configure GPIB
%
writeline(sport, '++mode 1'); %controller mode
writeline(sport, '++addr 6'); % vna address
writeline(sport, '++auto 0'); % do not automatically query data back
writeline(sport, '++ver'); % check connection by reading GPIB2USB version
ver = readline(sport);
disp(ver);
while sport.NumBytesAvailable > 0
    ver = readline(sport);
    disp(ver);
end

%
% configure VNA
%
writeline(sport, 'beep0'); %turn off annoying VNA error beep
writeline(sport, 'wide'); %use all of display
writeline(sport, 'rstcol'); %use all of display
writeline(sport, 'mof'); %turn off markers
writeline(sport, 'srt 10mhz'); %100MHz start F
writeline(sport, 'stp 3ghz'); %3GHz stop F
writeline(sport, 'swp'); % normal sweep mode
writeline(sport, 'np401'); % maximum is 401 data points
writeline(sport, 'fma'); % ascii output
writeline(sport, 'd14'); %display 4 plots
writeline(sport, 'tin');


%
% do s1x
%
fprintf("Taking data...");
writeline(sport, '++auto 0');
writeline(sport, 'tin');
writeline(sport, 'ch1;s11;smi');
writeline(sport, 'ch2;s22;smi');
writeline(sport, 'ch3;s33;smi');
writeline(sport, 'ch4;s44;smi');
%pause(SweepDelay);
%fprintf("   Autoscaling...\n");
%writeline(sport,'++auto 0');
%writeline(sport, 'ch1;asc;ch2;asc;ch3;asc;ch4;asc');
%pause(2*SweepDelay);


clear sport;
fclose('all');
