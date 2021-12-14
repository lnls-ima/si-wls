clear all; close all; clc;

% Ref.: M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti

T = 0:0.1:10

Cp0 = 1.61e-4.*T;
Cp1 = 1.61e-4.*T + 2.711e-6.*T.^3 ;
Cp2 = 1.228e-5.*T.^3 ;

figure();
plot(T,Cp0*1e3,T,Cp1*1e3,T,Cp2*1e3);
grid on
legend('Cp0','Cp1','Cp2');
xlabel('Temperature [K]');
ylabel('Nb-Ti specific heat [J/kg.K]');
set(gca,'FontSize',14)
title('Ref.: M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti" ')