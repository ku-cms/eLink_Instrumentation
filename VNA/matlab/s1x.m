% set collect the S parameter data!
headerstring = "single port pairs s11, s12, s13, s14";

fprintf(sport, '++auto 0');
fprintf("Taking data for %s :\n", headerstring);
fprintf(sport, ['tin' LF]);
fprintf(sport, ['ch1;s11;rim' LF]);
fprintf(sport, ['ch2;s12;rim' LF]);
fprintf(sport, ['ch3;s13;rim' LF]);
fprintf(sport, ['ch4;s14;rim' LF]);

pause(SweepDelay);
fprintf("   autoscaling...\n");
fprintf(sport, '++auto 0');
fprintf(sport, ['ch1;asc;ch2;asc;ch3;asc;ch4;asc' LF]);
pause(SweepDelay);

VNA_OTXT(sport, fileID, headerstring, SweepDelay);

return
