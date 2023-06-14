% set collect the S parameter data!
headerstring = "single port pairs s41, s42, s43, s44";

fprintf(sport, '++auto 0');
fprintf("Taking data for %s :\n", headerstring);
fprintf(sport, ['tin' LF]);
fprintf(sport, ['ch1;s41;rim' LF]);
fprintf(sport, ['ch2;s42;rim' LF]);
fprintf(sport, ['ch3;s43;rim' LF]);
fprintf(sport, ['ch4;s44;rim' LF]);

pause(SweepDelay);
fprintf("   autoscaling...\n");
fprintf(sport, '++auto 0');
fprintf(sport, ['ch1;asc;ch2;asc;ch3;asc;ch4;asc' LF]);
pause(SweepDelay);

VNA_OTXT(sport, fileID, headerstring, SweepDelay);

return
