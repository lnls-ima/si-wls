function [ratio_cu_sc, s_cu] = calc_ratio_cu_sc(d_cond, s_sc)

s_cond = pi*(d_cond/2)^2;

s_cu = s_cond - s_sc;

ratio_cu_sc = s_cond/s_sc - 1;
