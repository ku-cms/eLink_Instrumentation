function plot_vna_s4p(filename, connection_type)

    fprintf("\nCreating a plot, just a moment...\n");
    S = sparameters(filename);
    % connection type is either 1 or 2
    % 1 for SDD pairs 1:3 vs 2:4
    % 2 for SDD pairs 1:2 vs 3:4
    SDD = s2sdd(S.Parameters,connection_type);
    SDD11 = squeeze(SDD(1,1,:));
    Zodd = abs(50*( (1+SDD11) ./ (1-SDD11)));
    Zdiff = 2*Zodd;
    fig = figure();
    plot(S.Frequencies/1e9, abs(Zdiff));
    xlabel('Frequency - GHz');
    ylabel('Zdiff - Ω');
    [~,base,~] = fileparts(filename);
    title(base);
    fig.WindowState='maximized';
    shg;
    fprintf("\nmean of Zdiff = %0.3fΩ\n", mean(Zdiff));
    
end
