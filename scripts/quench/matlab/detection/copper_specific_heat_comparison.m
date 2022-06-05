%% Comparison between Copper specific heat from different references
%
%   References: 
%
%   [1] Bradley, P., Radebaugh, R., "Properties of Selected Materials at
%       Cryogenic Temperatures", NIST, 2013:
%       https://www.nist.gov/publications/properties-selected-materials-cryogenic-temperatures
%
%   [2] "Thermal Expansion Coefficient vs. Specific Heat vs. Temperature" 
%       graph from: 
%       https://www.copper.org/resources/properties/cryogenic/
%
%   [3] "Thermal Analysis and Simulation of the Superconducting Magnet in 
%        the SpinQuestExperiment at Fermilab.

clear all; 
%close all; 
clc;

%% Ref [1]:
%
%   Cp(Cu OFHC) [J/g.K]:

T1 = [4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0];
Cp1 = [0.09942, 0.2303, 0.4639, 0.8558, 1.47, 2.375, 3.64, 5.327, 7.491, 26.4, 57.63, 95.84, 135.2, 171.8, 203.8, 230.9, 253.5, 287.6, 311.6, 329.4, 343.4, 355, 364.7, 372.6, 378.6, 382.5, 384];

%% Ref [2]: 
%
% "The following information was compiled for the International Copper
% Association, Ltd. by C.A. Thompson, W. M. Manganaro and F.R. Fickett of
% the National Institute of Standards and Technology (NIST), Boulder,
% Colorado, July 1990"
%   
%   Cp [J/Kg.K]:

x = load('copper_specific_heat_copper_org.csv');
T2 = x(:,1);
Cp2 = x(:,2);
clear x;

%% Ref [3]: 
%
% "The specific heat of copper at low temperatures could also be
% approximates using polynomial fit as..."
%   
%   Cp [J/Kg.K]:

T3 = logspace(log10(4),log10(300),20);
Cp3 = -3.44e-6.*T3.^4 + 8.1e-4.*T3.^3 - 2.38e-4.*T3.^2 + 1.14e-2.*T3 - 2.86e-4;

%% Plot

T_zoom = 20;

set(0, 'DefaultLineLineWidth', 2);

figure();
sgtitle('Comparison between Copper specific heat from different references', ...
        'FontWeight','bold');

% Zoom up to T_zoom
subplot(1,2,1);
set(gca,'DefaultLineLineWidth',2)
plot( T1(find(T1 <= T_zoom)), Cp1(find(T1 <= T_zoom)), ...
      T2(find(T2 <= T_zoom)), Cp2(find(T2 <= T_zoom)), ...
      T3(find(T3 <= T_zoom)), Cp3(find(T3 <= T_zoom)));

legend('[1]: NIST publication, 2013', ...
       '[2]: copper.org, 1990', ...
       '[3]: Fermilab paper, fit equation for low temps', ...
       'Location', 'Northwest');
   
xlabel('Temperature [K]');
ylabel('Copper specific heat [J/kg.K]');
set(gca,'FontSize',14)
grid on;

% Full plot
subplot(1,2,2);
loglog(T1, Cp1, T2, Cp2, T3, Cp3);


axis([1, 300, 0, 400]);
xlabel('Temperature [K]');
ylabel('Copper specific heat [J/kg.K]');
set(gca,'FontSize',14)
grid on;