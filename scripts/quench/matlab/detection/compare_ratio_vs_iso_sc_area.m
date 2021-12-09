clear all; close all; clc;

d_total = 1.05;         % Total diameter [mm]

iso = 100:10:150;    	% Isolation thickness [um]

s_sc = 0.2:0.01:0.25;   % Superconductor area [mm²]

%%
% Conductors diameter
d_cond = zeros(length(iso),length(s_sc));

% Ratios Cu/Nb-Ti
ratios = zeros(length(iso),length(s_sc));

% Iterate for isolations ans SC areas
for i = 1:length(iso)
    for s = 1:length(s_sc)
        d_cond = d_total - 0.002*iso(i);
        ratios(i,s) = calc_ratio_cu_sc(d_cond, s_sc(s));
    end
    plot(s_sc, ratios(i,:));
    hold on
end

%% Plot results
leg = legend(split(num2str(iso)))
title(leg,'Isolation [um]')
leg.Title.Visible = 'on'
grid on
xlabel('Nb-Ti area [mm2]')
ylabel('Ratio Cu/Nb-Ti')
title('Ratio Cu/Nb-Ti Vs Isolation thickness and Nb-Ti area')

