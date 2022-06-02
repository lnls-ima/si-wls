%% Comparison between Nb-Ti specific heat from different references
%
%   References: 
%
%   [1] Akbar and Keller. "Thermal Analysis and Simulation of the
%       Superconducting Magnet in the SpinQuestExperiment at Fermilab"
%
%   [2] Russenschuck, S., "Field Computation for Accelerator Magnets",
%   Appendix A, Wiley, 2010. Found at:
%       https://onlinelibrary.wiley.com/doi/pdf/10.1002/9783527635467.app1
%
%   [3] Bychkov, Y., "Thermal conductivity and electrical resistivity of
%   Nb-Ti alloys at low temperatures"
%

clear all; close all; clc;

T = 4:300;
%% Ref [1]: 
%
% "Figure 18 shows the thermal conductivity of the Nb-Ti superconductor at
% 1 < T < 10 Kelvin from both references and the average value of them. We
% fitted the average thermal conductivity and the value can be approximated
% by...". 
%
%   Data points obtained from page 69 using the web tool:
%       https://apps.automeris.io/wpd/
%   
%  k [W/m.K]:

k1 = -0.0004.*T.^3 + 0.0085.*T.^2 + 0.00004.*T + 0.0671;

%% Ref [1]: 
%
% Reference 1 from Table 2
%   
%  k [W/m.K]:

p2 = [-5e-14 1.5e-11 6e-9 -3e-6 3e-4 4.56e-2 6.6e-2];
k2 = polyval(p2,T);

%% Ref [1]: 
%
% Reference 1 from Table 2
%   
%  k [W/m.K]:

p3 = [-8.9e-4 1.67e-2 -4.48e-2 6.81e-2];
k3 = polyval(p3,T);

%% Ref [2]: 
%   
%   Equation A.20
%
%   Cp [J/Kg.K]:
k4 = 6.6e-2 + 4.56e-2.*T + 3e-4.*T.^2 -3e-6.*T.^3 + 6e-9.*T.^4 + ...
     1.5e-11.*T.^5 -5e-14.*T.^6;

%% Ref [3]: 
%
% "Specific heat for Nb 51 Ti 49". Data points obtained from page 69 using
% the web tool https://apps.automeris.io/wpd/
%   
%   Cp [J/Kg.K]:
x = load('nb35ti65_thermal_conductivity_bychkov2.csv');
T5 = x(:,1);
k5 = x(:,2);
clear x;
 
x = load('nb45ti55_thermal_conductivity_bychkov.csv');
T6 = x(:,1);
k6 = x(:,2);
clear x;

figure();
loglog(T,k1,T,k2,'x',T,k3,T,k4,T5,k5,T6,k6);
grid on
xlabel('Temperature [K]');
ylabel('Thermal conductivity [W/m.K]');
title('Nb-Ti thermal conductivity');
legend('[1]: Fermilab paper Average', ... 
       '[1]: Fermilab paper Ref 1', ... 
       '[1]: Fermilab paper Ref 2', ... 
       '[2]: Russenschuck', ...
       '[3] Bychkov Nb_{35}Ti_{65}',...
       '[3] Bychkov Nb_{45}Ti_{55}',...
       'Location','Southeast')
set(gca,'FontSize',14)
%axis([T(1) T(end) 0 40])