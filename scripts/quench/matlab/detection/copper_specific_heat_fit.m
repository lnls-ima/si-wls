% Polynomial fit for specific heat of copper from graph provided by Davide
% Tomasini. Works well up to 50 K.

clear all; close all; clc

% Data points from graph
x = [4 10 22 50];
y = [0.1 1 10 100];

T = 4:300;

n = length(x);

loglog(x,y,'LineWidth',2)
hold on;

for i = n:n
    p = polyfit(x,y,i)
    y_est = polyval(p,T);
    loglog(T,y_est,'x');
end
grid on
axis([1 300 0.1 1000])
