%function Y = calc_v_correction_factor(

y = -10:0.001:0.999;

b = (1-2.*y)./sqrt(1-y);

figure();

plot(y,b)
grid on