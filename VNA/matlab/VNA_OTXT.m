function VNA_OTXT(sport, fileID, headerstring, sweepdelay)

LF = 10;
datadelay = sweepdelay;
datadelayu = 2;

fprintf("   GPIB trigger\n");
fprintf(sport, ['tibs' LF]);
fprintf(sport, ['*trg;*opc?' LF]);
pause(1);
fprintf(sport, '++auto 1');
fprintf("   waiting trigger complete\n");
count = 0;
timeout = 0;
while sport.BytesAvailable == 0
    pause(0.1);
    count = count + 1;
    if count == 1000 then
        timeout = 1;
        break;
    end
end

fprintf(sport, '++auto 0');

if timeout == 0
    res = fscanf(sport);
    if str2num(res) == 1
        fprintf("   data available\n");
        fprintf("   writing %s\n", headerstring);
        fprintf(fileID, '%s\t%s\n', headerstring, datestr(clock));
        fprintf(sport, ['otxt' LF]); % request data
        pause(datadelay);
        fprintf(sport, '++read eoi');
        
        count = 0;
        timeout = 0;
        while sport.BytesAvailable == 0
            pause(0.1);
            count = count + 1;
            if count == 1000 then
                timeout = 1;
                break;
            end
        end
        if timeout == 0
            res = fscanf(sport);
            while sport.BytesAvailable > 0
                dat = fgets(sport);
                fprintf(fileID, '%s', dat);
            end
        else
            fprintf("DEBUG:timed out waiting for OTXT\n");
        end
    else
        fprintf("ERROR:failed to collect %s\n", headerstring);
    end
else
    fprintf("DEBUG:timed out waiting for *trg;*opc?\n");
end

fprintf("   Done.\n\n");

fprintf(sport, ['tin' LF]);

end
