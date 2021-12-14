function [s_sc, s_cu] = calc_area_sc_cu(d_cond, ratio_cu_sc)

s_cond = pi.*(d_cond/2).^2;
s_sc = s_cond./(ratio_cu_sc + 1);
s_cu = s_cond - s_sc;
