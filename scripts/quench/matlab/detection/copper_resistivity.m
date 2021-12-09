function [rho] = copper_resistivity(T,RRR)

% Ref.: M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti "

rho = ( 1.545./RRR + 1./( 2.32547*1e9 ./ T.^5 + ...
                          9.57137*1e5 ./ T.^3 + ...
                          1.62735*1e2 ./ T) )*1e-8;