clear all;
close all;
clc;

rho = 0.3e-9;      % Copper resistivity for RRR = 50 (~RRR 200 @ 6T) [Ohm.m]
Acu = 0.288e-6;    % Copper area [m²]
Io = 250;       % Operating current [A] 

tqds = 0:0.01:0.2;      % Detection time [s]
vqs = [1 5 10 20 30 40 50];    % Quench propagation [m/s]

Jo = Io/Acu

figure();

% Iterate for isolations ans SC areas

% Voltage thresholds
vths = zeros(length(tqds),length(vqs));

for i = 1:length(vqs)
    vths(:,i) = vqs(i)*tqds*rho*Io/Acu;
    semilogy(tqds, vths(:,i));
    hold on
end

leg = legend(split(num2str(vqs)))
title(leg,'v_{q} [m/s]')
leg.Title.Visible = 'on'
grid on
xlabel('Detection time [s]')
ylabel('Detection voltage [V]')
title('Detection analysis for Model 3 (B = 6 T)')
set(gca,'FontSize',14)
%axis([0.025 0.2])