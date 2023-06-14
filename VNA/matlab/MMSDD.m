function MMSDD(sport, fileID, headerstring, sweepdelay)

LF = 10;
datadelay = 2;
a = headerstring(5);
b = headerstring(6);
hstring = sprintf("S-PARAMETERS SSD balanced port pair %s:%s", a, b);

fprintf(sport, '++auto 0');

fprintf("%s :\n", hstring);
fprintf(sport, ['tin' LF]);
fprintf(sport, ['ch1;dsp' LF]);
fprintf(sport, ['mmsdd' LF]);
fprintf(sport, [headerstring LF]);
fprintf(sport, ['rim' LF]); %rim
fprintf(sport, ['trs' LF]);
pause(sweepdelay);
fprintf("   autoscaling...\n");
fprintf(sport, ['asc' LF]);
pause(sweepdelay);

VNA_OTXT(sport, fileID, hstring, sweepdelay);

return
