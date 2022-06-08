clc;
cable_num = input('Cable number: ','s');

% create folder for cable
newSubFolder = ['Cable_' cable_num];
if ~exist(newSubFolder, 'dir')
  mkdir(newSubFolder);
end

filename = input('Assign base filename : ','s');
filename = ['R:\BEAN_GRP\4portvnadata\' newSubFolder '\' filename '.vna.txt'];

x=input('connect cables, press return when done.');

fileID = fopen(filename, 'at');
if fileID == -1
    disp('failed to open file. Early exit!');
    return;
end
disp('Saving data to');
fprintf('\t%s\n', filename);

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

s1x; %s11, s12, etc test
s2x;
s3x;
s4x;

MMSDD(sport, fileID, 'mm1p12', SweepDelay);
MMSDD(sport, fileID, 'mm1p13', SweepDelay);
MMSDD(sport, fileID, 'mm1p23', SweepDelay);
MMSDD(sport, fileID, 'mm1p14', SweepDelay);
MMSDD(sport, fileID, 'mm1p24', SweepDelay);
MMSDD(sport, fileID, 'mm1p34', SweepDelay);

fclose(sport);
fclose(fileID);
fclose('all'); % belt and suspenders close of files!

fprintf("\n\nAll tests run.\n");
