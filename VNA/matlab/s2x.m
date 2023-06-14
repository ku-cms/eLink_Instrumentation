% set collect the S parameter data!
headerstring = "single port pairs s21, s22, s23, s34";

fprintf(sport, '++auto 0');
fprintf("Taking data for %s :\n", headerstring);
fprintf(sport, ['tin' LF]);
fprintf(sport, ['ch1;s21;rim' LF]);
fprintf(sport, ['ch2;s22;rim' LF]);
fprintf(sport, ['ch3;s23;rim' LF]);
fprintf(sport, ['ch4;s24;rim' LF]);

pause(SweepDelay);
fprintf("   autoscaling...\n");
fprintf(sport, '++auto 0');
fprintf(sport, ['ch1;asc;ch2;asc;ch3;asc;ch4;asc' LF]);
pause(SweepDelay);

VNA_OTXT(sport, fileID, headerstring, SweepDelay);

return
