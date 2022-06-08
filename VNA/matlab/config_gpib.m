% Turn off read-after-write feature
fprintf(sport, '++mode 1'); %CONTROLLER mode
fprintf(sport, '++addr 6'); %VNA GPIB address
fprintf(sport, '++auto 0'); %do not automatically query data back
fprintf(sport, '++ver');    %confirm connection to GPIB2USB device
ver = fgets(sport);
disp(ver);

return;
