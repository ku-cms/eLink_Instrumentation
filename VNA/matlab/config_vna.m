
% configure instrument

%reset VNA: WARNING! The reset deletes all saved calibrations!
%fprintf(sport, ['*rst' LF]); %reset VNA: WARNING, deletes all saved calibrations
%pause(10); %wait for reset to finish

fprintf(sport, ['beep0' LF]); %turn off annoying VNA error beep
fprintf(sport, ['wide' LF]); %use all of display
fprintf(sport, ['rstcol' LF]); %use all of display
fprintf(sport, ['mof' LF]); %turn off markers
fprintf(sport, ['srt 10mhz' LF]); %10MHz start F
fprintf(sport, ['stp 6ghz' LF]);
fprintf(sport, ['swp' LF]); % normal sweep mode
fprintf(sport, ['np401' LF]); % maximum is 401 data points
fprintf(sport, ['fma' LF]); % ascii output
fprintf(sport, ['d14' LF]); %display 4 plots
fprintf(sport, ['tin' LF]);

% testing gate parameters
%fprintf(sport, ['gst 9.0ns' LF]);
%fprintf(sport, ['gsp 19.0ns' LF]);

% test nonsense command
%fprintf(sport, ['goofymonkey 1.0ns' LF]);

return;
