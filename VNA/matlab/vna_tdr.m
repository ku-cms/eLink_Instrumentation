% take data from VNA
% compute a TDR based on the S4P file
% generate plots

version = "1.1";
close;
clc;
fprintf("Compute Zdiff using Anritsu 4-port VNA MS4623D\n");
fprintf("   Version %s\n\n", version);

% get cable number
cable_num = input('Cable number: ', 's');

% connection type is either 1 or 2
connection_type = 0;
while ((connection_type ~= 1) && (connection_type ~= 2))
    fprintf("Enter 1 for SDD pairs 1:3 vs 2:4\n");
    fprintf("Enter 2 for SDD pairs 1:2 vs 3:4\n");
    connection_type = input('Connection type [1, 2]: ', 's');
    connection_type = str2num(connection_type);
end
fprintf("Connection type: %d", connection_type);

% create folder for cable
newSubFolder = ['Cable_' cable_num];
if ~exist(newSubFolder, 'dir')
    mkdir(newSubFolder);
end

% data file name
fprintf('\n*** Attention *** Data file will be overwritten, NOT appended\n');
filename = input('Assign base file name: ', 's');
path = pwd;
filename = [path '\' newSubFolder '\' filename '.s4p'];

fprintf("Confirm cable for test is connected to VNA.\n");
x = input('Press ENTER when done.');

fileID = fopen(filename, 'wt'); % don't append, was 'at' use 'wt' for flush
if fileID == -1
    disp('ERROR: failed to open/create data file. Early exit!');
    return;
end
fprintf('Saving data to %s\n', filename);

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
%writeline(sport, 'srt 10mhz'); %10MHz start F
%writeline(sport, 'stp 6ghz');
writeline(sport, 'srt 100mhz'); %100MHz start F
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
writeline(sport, 'ch1;s11;rim');
writeline(sport, 'ch2;s12;rim');
writeline(sport, 'ch3;s13;rim');
writeline(sport, 'ch4;s14;rim');
pause(SweepDelay);
fprintf("   Autoscaling...\n");
writeline(sport,'++auto 0');
writeline(sport, 'ch1;asc;ch2;asc;ch3;asc;ch4;asc');
pause(2*SweepDelay);

writeline(sport, 'tibsb'); % was tibs
writeline(sport, '*trg;*opc?');
pause(1);
writeline(sport, '++auto 1');
count = 0;
timeout = 0;
while sport.NumBytesAvailable == 0
    pause(0.1);
    count = count + 1;
    if count == 1000
        timeout = 1;
        break;
    end
end
writeline(sport,'++auto 0');
if timeout == 0
    results = readline(sport);
    if str2double(results) == 1
        writeline(sport, 'os4p');
        long_delay = 20;
        fprintf("...pause %d seconds for measurement to complete...\n", ...
            long_delay);
        %pause(DataDelay);
        for i=1:long_delay
            fprintf("%3d ", i);
            if mod(i , 5) == 0
                fprintf("\n");
            end
            pause(1);
        end
        pause(DataDelay);
        writeline(sport,'++read eoi');
        count = 0;
        timeout = 0;
        while sport.NumBytesAvailable == 0
            pause(0.1);
            count = count + 1;
            if count == 300
                timeout = 1;
                break;
            end
        end
        if timeout == 0
            fprintf("   data available at %s\n", string(datetime("now")));
            results = readline(sport);
            %disp(results);
            while sport.NumBytesAvailable > 0
                results = readline(sport);
                fprintf(fileID, '%s', results);
            end
        else
            fprintf("DEBUG:timed out waitin for os4p\n");
        end
    else
        fprintf("ERROR: failed to collect data\n");
    end
else
    fprintf("DEBUG:timed out waiting for *trig;*opc?\n");
end
fprintf("Done.\n");
writeline(sport, 'tin');

clear sport;
fclose(fileID);
fclose('all');

fprintf("\nAll VNA tests are complete.\n");
fprintf("\nComputing TDR and generating plots...\n");

%
% compute impedance via a time domain model based on the
% 4 port VNA S parameters
%

S = sparameters(filename); % read s4p file
%connection_type = 1; % 1:3 vs 2:4
%connection_type = 2; %1:2 vs 3:4
SDD = s2sdd(S.Parameters, connection_type);
SDD11 = squeeze(SDD(1,1,:));
freq = S.Frequencies;

Vin = 1;
tdrfreqdata = Vin*(SDD11+1)/2;
tolerance = -35; % dB tolerance for rationalfit
npoles = [0 1000]; % allow up to 1000 poles in fitted model
warning('off','all');
[tdrfit, errdb] = rationalfit(freq,tdrfreqdata,'NPoles', npoles, ...
    'Tolerance', tolerance, 'WaitBar', true);
warning('on','all');

Ts = 5e-12; % 5ps
N = 4000; % Number of samples should be 20ns
Trise = 5e-11; % Define a step signal
[Vtdr,tdrT] = stepresp(tdrfit,Ts,N,Trise);
t11_row=(((2*Vtdr)-Vin)/Vin);
tdrz=50*((1+t11_row)./(1-t11_row)); % Zodd
tdrzdiff = tdrz .* 2; % Zodd to Zdiff
time = tdrT * 1e9; % plot in ns

% simple statistics
meanstart = fix(2e-9 / Ts); % 400
meanstop = fix(5e-9 / Ts); % 1000
avg = mean(tdrzdiff(meanstart:meanstop)); % compute mean between 2n and 5ns
annstr = sprintf('avg = %0.1fΩ',avg);
annpos = [.156 .850 .070 .052]; % place answer on plot

%
% generate plots
%
figure(1);
tiledlayout(2,1);

%
% plot between 1.5 and 5.5 ns
%
plotstart = 1.5; % ns
plotstop = 5.5; % ns
nexttile;
plot(time,tdrzdiff,'b','LineWidth',2);
title(filename, "Interpreter", 'none');
ylabel('TDR (Ohm)');
xlabel('Time (ns)');
annotation('textbox', annpos, 'String', annstr, 'FitBoxToText','on');
line([plotstart, plotstop],[avg,avg]); % line through average Z
legend('Calculated TDR');
ylim([50 150]);
xlim([plotstart plotstop]);

%
% plot full data set
%
nexttile;
plot(time, tdrzdiff, 'r', 'LineWidth', 2);
title(filename, 'Interpreter','none');
ylabel('TDR (Ohm)');
xlabel('Time (ns)');
legend('Calculated TDR');

%
% save plot
%
[filepath, name, ext] = fileparts(filename);
plotfilename = strcat(filepath, '\', name, '.png');
exportgraphics(gcf, plotfilename);
fprintf("\nPNG of plot saved.");

fprintf("\nEND\n");