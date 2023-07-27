clear;

version = '1.0';
fprintf("Reprocess Python Data for Zdiff Estimateion\n");
fprintf("     Version %s\n\n", version);

runagain = true;
while runagain
    close;
    clc;

    %
    % get one of the .vna_#.s2p files from previously Python processed data
    % PPP data
    %
    fprintf("Navigate to subdirectory of PPP data and select S2P file.\n");
    temp = 'R:\BEAN_GRP\4portvnadata\VNA_analysis\Data';
    if ~exist(temp, 'dir')
        temp = '*.s2p';
    else
        temp = strcat(temp, '\*.s2p');
    end
    [file, pathname] = uigetfile(temp);
    if isequal(file, 0)
        fprintf("\nUser selection canceled.");
        fprintf("\nEarly exit.\n");
        return;
    end
    [folder, baseFilenameNoExt, extension] = fileparts(file); %#ok<*ASGLU>
    folder = pathname;

    fprintf("\nReading PPP files...");
    rootname = extractBefore(baseFilenameNoExt, '.vna_');
    fn1 = strcat(folder, rootname, '.vna_0.s2p');
    fn2 = strcat(folder, rootname, '.vna_1.s2p');
    fn3 = strcat(folder, rootname, '.vna_2.s2p');
    fn4 = strcat(folder, rootname, '.vna_3.s2p');

    %
    % read in S1x, S2x, S3x and S4x data
    %
    S1 = sparameters(fn1);
    S2 = sparameters(fn2);
    S3 = sparameters(fn3);
    S4 = sparameters(fn4);

    %
    % extract frequencies and parameters to be repackaged
    %
    freq = S1.Frequencies;
    s1 = S1.Parameters;
    s2 = S2.Parameters;
    s3 = S3.Parameters;
    s4 = S4.Parameters;

    fprintf("\nGenerate new S4P file...");
    x1 = reshape(s1,[1,4,401]);
    x2 = reshape(s2,[1,4,401]);
    x3 = reshape(s3,[1,4,401]);
    x4 = reshape(s4,[1,4,401]);
    newS = [x1; x2; x3; x4]; % repackage for S4P file
    S = rfdata.network('Type','S', 'Freq',freq,'Data',newS, 'Z0',50);
    S = sparameters(S);
    %
    % write out new S4P file
    %
    new_s_filename = strcat(folder,rootname,'.s4p');
    rfwrite(S,new_s_filename, 'Format', 'MA', 'ForceOverwrite',true);

    %
    % process the new S4P file
    %
    keeprunningsamefile = true;
    while keeprunningsamefile
        close; % close any open figure(s)
        fprintf("\nProcessing new S4P file...");
        filename = new_s_filename;
        newS = sparameters(filename); % read s4p file
        connection_type = 0;
        fprintf("\nEnter connection type for PPP data:\n");
        while ((connection_type ~= 1) && (connection_type ~= 2))
            fprintf("   Enter 1 for SDD pairs 1:3 vs 2:4\n");
            fprintf("   Enter 2 for SDD pairs 1:2 vs 3:4\n");
            connection_type = input('Connection type [1, 2]: ', 's');
            connection_type = str2num(connection_type); %#ok<ST2NM>
        end
        %
        % process differential into single-ended
        %
        fprintf("Connection type: %d", connection_type);
        SDD = s2sdd(newS.Parameters, connection_type);
        SDD11 = squeeze(SDD(1,1,:));
        freq = newS.Frequencies;
        %
        % model and get step response
        %
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

        %
        % simple statistics
        %
        startns = 2;
        stopns = 5;
        meanstart = fix(startns * 1e-9 / Ts); % 400
        meanstop = fix(stopns * 1e-9 / Ts); % 1000
        avg = mean(tdrzdiff(meanstart:meanstop)); % compute mean 2ns to 5ns
        stddev = std(tdrzdiff(meanstart:meanstop));
        annstr = sprintf('avg = %0.1fΩ (%d)\nσ = %0.1f', ...
            avg, connection_type, stddev);
        annpos = [.15 .86 .070 .052]; % place answer on plot

        %
        % generate plots
        %
        figure(1);
        tiledlayout(2,1);

        [filepath, name, ext] = fileparts(filename);
        if isempty(filepath)
            filepath = '.';
        end
        plotfilename = strcat(filepath, '\', name, ...
            '_con',string(connection_type), '.png');

        %
        % plot an extra 0.5 ns on either side of area of interest
        %
        plotstart = startns - 0.5; % ns
        plotstop = stopns + 0.5; % ns
        nexttile;
        plot(time,tdrzdiff,'b','LineWidth',2);
        title(name, "Interpreter", 'none');
        ylabel('TDR (Ohm)');
        xlabel('Time (ns)');
        annotation('textbox', annpos, 'String', annstr, 'FitBoxToText','on');
        line([startns, stopns],[avg,avg]); % line through average Z
        line([startns,startns],[avg-5,avg+5]); % tics to indicate where
        line([stopns,stopns],[avg-5,avg+5]);   % stats calculated
        legend('Calculated TDR');
        zoomupper = ceil((avg + 50)/10)*10;
        zoomlower = ceil((avg - 50)/10)*10;
        ylim([zoomlower zoomupper]);
        xlim([plotstart plotstop]);

        %
        % plot full data set
        %
        nexttile;
        plot(time, tdrzdiff, 'r', 'LineWidth', 2);
        title(name, 'Interpreter','none');
        ylabel('TDR (Ohm)');
        xlabel('Time (ns)');
        legend('Calculated TDR');

        %
        % save plot
        %
        exportgraphics(gcf, plotfilename);
        fprintf("\nPNG of plot saved.");

        %
        % add to an XLS file with results
        %
        try
            excel = 'R:\BEAN_GRP\4port_tdr\processed_summary.xls';
            if exist(excel,'file') == 0
                % file doesn't exist?
                data_to_save = {"data source", "date time", "average Ω", ...
                    "stddev Ω", "connection"}; %#ok<CLARRSTR>
                writecell(data_to_save,excel, 'WriteMode', 'Append', ...
                    'Filetype', 'spreadsheet');
            end
            % append new data to end to end
            data_to_save = {name, datetime('now'), avg, stddev, ...
                connection_type};
            writecell(data_to_save, excel, 'WriteMode', 'Append', ...
                'Filetype', 'spreadsheet')
        catch
            fprintf(2,"\n\n*** Problem appending to 'processed_summary.xls'");
            fprintf(2,"\n*** File may be in use.");
            fprintf(2,"\n*** Close file and re-run analysis.\n");
        end
        runagaintemp = 'z';
        while ((runagaintemp ~= 'y') && (runagaintemp ~= 'n'))
            runagaintemp = lower(input("\n   run SAME file again [y/n]? ", "s"));
        end
        if runagaintemp == 'y'
            keeprunningsamefile = true;
        else
            keeprunningsamefile = false;
        end
    end % keeprunningsamefile

    runagaintemp = 'z';
    while ((runagaintemp ~= 'y') && (runagaintemp ~= 'n'))
        runagaintemp = lower(input("\n   run NEW file [y/n]? ", "s"));
    end
    if runagaintemp == 'y'
        runagain = true;
    else
        runagain = false;
    end
end % runagain