function [rho,c,k] = copper_properties(T,RRR,B)

% Refs.: 
% [1] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
% [2] KN5010 Nº4 (Davide)
% [3] https://www.copper.org/resources/properties/cryogenic/ 
% 

% Resistivity [Ohm.m]
rho = ( 1.545./RRR + 1./( 2.32547*1e9 ./ T.^5 + ...
                          9.57137*1e5 ./ T.^3 + ...
                          1.62735*1e2 ./ T) )*1e-8;

% Specific heat [J/kg.K] - polynomial fit obtained for temperatures up to 50 K
P = [-0.000006646433277 0.001186241294937 -0.003070534537926 0.018727649162436 0];
c = polyval(P,T);
                      
% Thermal conductivity [W/m.K]
k = 

