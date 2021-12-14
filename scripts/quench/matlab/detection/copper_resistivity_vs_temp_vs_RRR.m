clear all; close all; clc;

T = logspace(log10(4),log10(300),1000);

rrrs = [10,20,50,100,200];

figure();

for i = 1:length(rrrs)
    rhos = copper_resistivity(T,rrrs(i));
    loglog(T,rhos);
    hold on;
end

leg = legend(split(num2str(rrrs)));
title(leg,'RRR');
leg.Title.Visible = 'on';
grid on;
xlabel('Temperature [K]');
ylabel('Resistivity [Ohm.m]');

%ylabel('Resistivity [10^{-8} Ohm.m]');
%axis([4,300,2e-4,2])
