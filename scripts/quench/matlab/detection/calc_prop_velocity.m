function prop_vel = calc_prop_velocity(Jo, C, rho, k, Tjoule, Top, method)

v = Jo./C.*sqrt(rho.*k./(Tjoule-Top));

if method == "adiabatic"
	prop_vel = v;
   
elseif method == "cooled"
    corr_factor = 0;
    prop_vel = corr_factor*v;
else
    prop_vel = 5;
end
