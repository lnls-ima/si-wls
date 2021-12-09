clear all;
%close all;
clc;

%% Operation parameters
Iop = 250;              % Operating current [A]
Top = 4.2;              % Operating SC temperature [K]
Tc = 9.2;               % Critical temperature [K]
Tcs = 5.95;             % Current-sharing temperature [K]
Tjoule = (Tc + Tcs)/2;  % Transition temperature [k]

%% Wire parameters
RRR = 50;
ratio_cu_sc = [0.6 0.8 1 1.2];
d_cond = 0.82;          % Total conductor diameter [mm]

% Total conductor and composite areas [mm²]
s_cond = pi.*(d_cond/2).^2;                             
[s_sc, s_cu] = calc_area_sc_cu(d_cond, ratio_cu_sc);    

%% Materials properties

% Copper @ RRR = 100, Tjoule = 5 K
% Refs.: 
%   - https://www.copper.org/resources/properties/cryogenic/
%   - KN5010 Nº4 (Davide)
%   - M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"

f_cu = s_cu/s_cond;                         % Copper fraction
resty_cu = copper_resistivity(Tjoule,RRR);  % Resistivity [Ohm.m]
dsty_cu = 9000;                             % Density [kg/m³]
c_cu = 0.2;                                 % Specific heat [J/kg.K]
k_cu = 400;                                 % Thermal conductivity [W/m.K]

% Nb-Ti @ Tjoule
f_sc = s_sc/s_cond;                         % NbTi fraction
resty_sc = 1e-5;
dsty_sc = 6500;                             % Estimated density from 50-50% NbTi alloy [km/m³]
c_sc = 0.07*Tjoule; 
c_sc = 1.5;                                 % Estimated from M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
%c_sc = 10000;
k_sc = 0.5;                                 % Ref.: "Thermal Conductivity and Electrical Resistivity of NbTi Alloys at Low Temperatures"

%%
% Current density. During quench, all current goes to copper.
Jop = Iop.*1e6./s_cu;

% Composite volumetric specific heat
C_comp = f_cu.*dsty_cu.*c_cu + f_sc.*dsty_sc.*c_sc;
%C_comp = dsty_cu*c_cu;

% Composite resistivity
resty_comp = 1./(f_cu./resty_cu + f_sc./resty_sc);

% Composite thermal conductivity
k_comp = f_cu.*k_cu + f_sc.*k_sc;


%% Velocity estimation
method = 'adiabatic';
vqs = calc_prop_velocity(Jop, C_comp, resty_comp, k_comp, Tjoule, Top, method)

figure(1);
plot(ratio_cu_sc, vqs,'d:','MarkerSize',15);
hold on
%%
title('Estimated propagation velocity @ Iop = 250 A, Top = 4.2 K, Tc = 9.8 K, Tcs = 5.9K')
xlabel('Ratio Cu/Nb-Ti');
ylabel('Propagtion velocity [m/s]')
set(gca,'FontSize',14)
leg = legend(split(num2str([200 100 50])))
title(leg,'RRR')
leg.Title.Visible = 'on'
grid on
