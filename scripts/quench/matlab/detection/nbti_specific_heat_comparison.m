%% Comparison between Nb-Ti specific heat from different references
%
%   References: 
%
%   [1] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti
%
%   [2] "Thermal Analysis and Simulation of the Superconducting Magnet in 
%        the SpinQuestExperiment at Fermilab."
%
%   [3] "Specific Heat of Some Solids". Material provided by Davide (CERN)
%   found at:
%       https://indico.cern.ch/event/1032945/contributions/4338010/attachments/2236574/3791024/Specific%20heat.pdf
%
%   [4] Russenschuck, S., "Field Computation for Accelerator Magnets",
%   Appendix A, Wiley, 2010. Found at:
%       https://onlinelibrary.wiley.com/doi/pdf/10.1002/9783527635467.app1


clear all; close all; clc;

T = 4:0.1:9.2;
B_0 = 0;
B_6 = 6;

%% Ref [1]: 
% 
% "At low temperatures in the normal conducting state"
%
%   Cp(T < 10 K) for Nb-46.5 wt% Ti [J/g.K]:

Cp1_1 = 1.61e-4.*T + 2.711e-6.*T.^3;

%% Ref [1]:
%
% "An approximate expression for the heat capacity in the superconducting
% state at 6 T"
%
%   Cp(6T, T < Tc) [J/g.K]:

Cp1_2 = 1.228e-5.*T.^3;

%% Ref [1]: 
%
% "Specific heat of NbTi calculated from the Debye function with electronic
% component and with the same correction factor ..."
%
%   Cp [J/g.K]:

T1_3 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, ...
      220, 240, 260, 280, 300, 320, 340];
Cp1_3 = [0.00432, 0.0246, 0.0685, 0.124, 0.176, 0.219, 0.253, 0.279, 0.300, ...
       0.317, 0.341, 0.357, 0.369, 0.378, 0.385, 0.391, 0.396, 0.400, ...
       0.404, 0.407, 0.410, 0.413];

%% Ref [2][4]: Both references produce the same curves
%
% [2]: "Specific heat of the Nb-Ti superconductor depends on the magnetic
% field and under 9 Kelvin can be approxiamted as ..."
%
%   Cp(T < 9 K) [J/Kg.K]:

Cp2_0T = 0.0082.*T.^3 + 0.011.*B_0.*T;
Cp2_6T = 0.0082.*T.^3 + 0.011.*B_6.*T;

% [4]: "In the superconducting state, the VHC of Nb–Ti depends on the
% temperature and applied magnetic flux density"
%
% In this case, the volumetric heat capacity (VHC) was converted to
% specific heat dividing it by provided density
%
%   Cp(T < 9 K) [J/Kg.K]:

desty = 6000;   % [kg/m³]

Cp4_0T = (49.1.*T.^3 + 64.*T.*B_0)/desty;
Cp4_6T = (49.1.*T.^3 + 64.*T.*B_6)/desty;

%% Ref [3]: 
%
% "Specific heat for Nb 51 Ti 49". Data points obtained from page 69 using
% the web tool https://apps.automeris.io/wpd/
%   
%   Cp [J/Kg.K]:

x = load('nbti_specific_heat_davide.csv');
T3 = x(:,1);
Cp3 = x(:,2);
clear x;

%% Plot

T_zoom = 10;

set(0, 'DefaultLineLineWidth', 2);

figure();
sgtitle('Comparison between Nb-Ti specific heat from different references', ...
        'FontWeight','bold');

% Zoom up to T_zoom
subplot(1,2,1);
set(gca,'DefaultLineLineWidth',2)
plot( T, Cp1_1 * 1e3, T, Cp1_2 * 1e3, ...
      T1_3(find(T1_3 <= T_zoom)), Cp1_3(find(T1_3 <= T_zoom)) * 1e3, ...
      T, Cp2_0T, T, Cp2_6T, ...
      T3(find(T3 <= T_zoom)), Cp3(find(T3 <= T_zoom)), ...
      T, Cp4_0T, 'o', T, Cp4_6T,'x');

legend('[1]: MIITS table, normal conducting state', ...
       '[1]: MIITS table, superconducting state, B = 6 T', ...
       '[1]: MIITS table, calculated from Debye function', ...
       '[2]: Fermilab paper, T < 9 K, B = 0 T', ...
       '[2]: Fermilab paper, T < 9 K, B = 6 T', ...
       '[3]: Compilation provided by CERN', ...
       '[4]: Russenschuck, superconducting state, B = 0 T',...   
       '[4]: Russenschuck, superconducting state, B = 6 T',...
       'Location', 'Northwest');
  
xlabel('Temperature [K]');
ylabel('Nb-Ti specific heat [J/kg.K]');
set(gca,'FontSize',14)
grid minor;

% Full plot
subplot(1,2,2);
loglog( T, Cp1_1 * 1e3, T, Cp1_2 * 1e3, T1_3, Cp1_3 * 1e3, T, Cp2_0T, ...
      T, Cp2_6T, T3, Cp3);

% legend('[1]: MIITS table, normal conducting state', ...
%        '[1]: MIITS table, superconducting state, 6T', ...
%        '[1]: MIITS table, calculated from Debye function', ...
%        '[2]: Fermilab paper, T < 9 K, B = 0 T', ...
%        '[2]: Fermilab paper, T < 9 K, B = 6 T', ...
%        '[3]: Compilation provided by CERN', ...
%        '[4]: B = 0 T',...   
%        '[4]: B = 6 T',...
%        'Location', 'Southeast');
axis([4, 300, 1e-1, 500]);
xlabel('Temperature [K]');
ylabel('Nb-Ti specific heat [J/kg.K]');
set(gca,'FontSize',14)
grid on;