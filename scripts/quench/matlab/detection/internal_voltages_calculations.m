clear all; close all; clc;

L = 0.12;

Iop = 242;
Vmax = 600;

% Length ratio where quench occured
alpha = 0.3;


Rd = Vmax/Iop       % Dump resitor calculation
Rq = Rd/1000;       % Quench resistance

tau = L/(Rd+Rq)     % Time constant

% Inductance before and after quench
Lbq = alpha*L;
Laq = (1-alpha)*L;

dIdt = -Iop/tau

Vp = 0;
Vn = Vmax;

Vbq = -Lbq*dIdt
Vq = Rq*Iop
Vaq = -Laq*dIdt

x = [0 alpha-0.01 alpha+0.01 1];

plot(x,[Vp Vbq Vbq+Vq Vn]);
xlabel('Normalized coil length');
ylabel('Voltage distribution [V]');