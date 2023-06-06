% Script to take VNA data.

% Input cable number
cable_num = input('Cable number: ','s');

% Create folder for cable
newSubFolder = ['Cable_' cable_num];
if ~exist(newSubFolder, 'dir')
  mkdir(newSubFolder);
end

% Input file name
filename = input('Assign base file name: ','s');
filename = ['R:\BEAN_GRP\4portvnadata\' newSubFolder '\' filename '.vna.txt'];

x = input('Connect cables. Press return when done.');

fileID = fopen(filename, 'at');
if fileID == -1
    disp('ERROR: Failed to open file. Early exit!');
    return;
end
disp('Saving data to');
fprintf('\t%s\n', filename);

% Open serial port
% Note: 'serial' will be removed in a future release; we should update to use 'serialport'.
sport = serial('COM4');
sport.BaudRate = 57600;
sport.Terminator = 'LF';
sport.Timeout = 10;
sport.InputBufferSize = 100000; % make a nice big input buffer!
sport.OutputBufferSize = 10000;

% linefeed must terminate all commands to VNA
LF = 10;
SweepDelay = 2;
DataDelay = 2;

fopen(sport);
config_gpib;
config_vna;

s1x; % s11, s12, s13, s14
s2x;
s3x;
s4x;

MMSDD(sport, fileID, 'mm1p12', SweepDelay);
MMSDD(sport, fileID, 'mm1p13', SweepDelay);
MMSDD(sport, fileID, 'mm1p23', SweepDelay);
MMSDD(sport, fileID, 'mm1p14', SweepDelay);
MMSDD(sport, fileID, 'mm1p24', SweepDelay);
MMSDD(sport, fileID, 'mm1p34', SweepDelay);

% Close all the things.
fclose(sport);
fclose(fileID);
fclose('all');

fprintf("\nAll VNA tests are complete!\n");
