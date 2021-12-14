clean_all;

% As propagation velocity is still uncertain, this will be one parameter
% space. To account for variable resistivity under different magnetic
% fields, another spec will be RRR

% Operating current [A] 
Io = 250;

% Total conductor diameter [mm]
d_cond = 0.82;  

% Cu-NbTi ratios
ratios = [0.6 0.8 1 1.2];

% Detection time [s]
tqds = 0:0.01:0.1;      

% RRRs and related resistivities
%   Ref.: https://www.copper.org/resources/properties/cryogenic/
rrrs = [25 50 100];
%rhos = [0.75 0.32 0.17]*1e-9;       % [Ohm.m]
rhos = copper_resistivity(4,rrrs);  % [Ohm.m]

% Quench propagation velocity [m/s]
vqs = [0.1 1 5 10 20 30 40 50]; 

%% Analysis for various ratios
vq = 5;

%ind_rrr = 3;

for ind_rrr = 1:length(rrrs)
    
    rho = rhos(ind_rrr);

    [s_scs, s_cus] = calc_area_sc_cu(d_cond*1e-3,ratios);

    figure(ind_rrr);

    vdet = zeros(length(tqds),length(ratios));
    vdet_ratio = zeros(length(tqds),length(ratios));

    for i = 1:length(s_cus)
        vdet(:,i) = calc_detection_voltage(vq,rho,tqds,Io,s_cus(i));
        vdet_ratio(:,i) = vdet(:,i)./vdet(:,1);
        semilogy(tqds, vdet(:,i));
        hold on;
    end
        
    leg = legend(split(num2str(ratios)));
    title(leg,'ratios');
    leg.Title.Visible = 'on';
    grid on;
    xlabel('Detection time [s]');
    ylabel('Detection voltage [V]');
    title("Detection analysis @ vq = " + vq + " m/s, RRR = " + rrrs(ind_rrr));
    set(gca,'FontSize',14);
    axis([0.01 0.1 1e-3 1]);

    max(vdet_ratio)
    min(vdet_ratio)
end

%% Analysis for various RRR
ratio = 1;
vq = 1;

[s_sc, s_cu] = calc_area_sc_cu(d_cond*1e-3,ratio);

figure();

vdet = zeros(length(tqds),length(rhos));

for i = 1:length(rhos)
    vdet(:,i) = calc_detection_voltage(vq,rhos(i),tqds,Io,s_cu);
    semilogy(tqds, vdet(:,i));
    hold on
end

leg = legend(split(num2str(rrrs)));
title(leg,'RRR');
leg.Title.Visible = 'on';
grid on;
xlabel('Detection time [s]');
ylabel('Detection voltage [V]');
%title('Detection analysis for Model 3 (B = 6 T)');
set(gca,'FontSize',14);
%axis([0.025 0.2]);

%% Analysis for various RRR
tqd = 0.075;
ratio = 0.6;
[s_sc, s_cu] = calc_area_sc_cu(d_cond*1e-3,ratio);

vqs = logspace(log10(0.1), log10(10), 20); 

figure();

vdet = zeros(length(vqs),length(rhos));

for i = 1:length(rhos)
    vdet(:,i) = calc_detection_voltage(vqs,rhos(i),tqd,Io,s_cu);
    semilogy(vqs, vdet(:,i));
    hold on
end

leg = legend(split(num2str(rrrs)));
title(leg,'RRR');
leg.Title.Visible = 'on';
grid on;
xlabel('Propagation velocity [m/s]');
ylabel('Detection voltage [V]');
%title('Detection analysis for Model 3 (B = 6 T)');
%set(gca,'FontSize',14);
%axis([0.025 0.2]);

%% Analysis for various RRR
tqd = 0.075;
ratio = 1;
[s_sc, s_cu] = calc_area_sc_cu(d_cond*1e-3,ratio);

vqs = logspace(log10(0.1), log10(10), 20); 

figure();

vdet = zeros(length(vqs),length(rhos));

for i = 1:length(rhos)
    vdet(:,i) = calc_detection_voltage(vqs,rhos(i),tqd,Io,s_cu);
    semilogy(vqs, vdet(:,i));
    hold on
end

leg = legend(split(num2str(rrrs)));
title(leg,'RRR');
leg.Title.Visible = 'on';
grid on;
xlabel('Propagation velocity [m/s]');
ylabel('Detection voltage [V]');
title("Detection analysis @ tqd = " + tqd*1000 + " ms, Cu/NbTi = " + ratio);
set(gca,'FontSize',14);
%axis([0.025 0.2]);

%%
%close all
ratio = 1;
[s_sc, s_cu] = calc_area_sc_cu(d_cond*1e-3,ratio);
vqs = logspace(log10(0.1), log10(10), 20);
vth = 1e-1;
    
figure();

for ind_rrr = 1:length(rhos)
    
    rho = rhos(ind_rrr);

    [VQS, TQDS] = meshgrid(vqs, tqds);

    VDETS = calc_detection_voltage(VQS,rho,TQDS,Io,s_cu);
    VDET_MIN = ones(size(VDETS))*1e-1;
    VDET_COLOR = ones(size(VDETS))*(4-ind_rrr);

    s = surf(VQS,TQDS,VDETS,VDET_COLOR,'FaceAlpha',1/(4-ind_rrr));
    s.EdgeColor = 'none';
    hold on
end

VDET_MIN = ones(size(VDETS))*vth;
VDET_MIN_COLOR = ones(size(VDETS))*0.1;
%mesh(VQS,TQDS,VDET_MIN,VDET_MIN_COLOR,'FaceAlpha',0.5);
s = surf(VQS,TQDS,VDET_MIN,'FaceAlpha',0.5,'FaceColor',[1 0.5 0.5]);
s.EdgeColor = 'none';


leg = legend([ append("RRR = ",split(num2str(rrrs))); ...
               {"Vth = " + vth*1e3 + " mV"} ] );
%title(leg,'RRR');
leg.Title.Visible = 'on';
xlabel('Propagation velocity [m/s]');
ylabel('Detection time [s]')
zlabel('Detection voltage [V]');
title("Detection analysis @ Cu/NbTi = " + ratio);
set(gca,'FontSize',14);
axis([0 10 0 0.1 0 0.9])

%%
%close all
ratio = 1;
[s_sc, s_cu] = calc_area_sc_cu(d_cond*1e-3,ratio);
vqs = logspace(log10(0.1), log10(10), 20);
vth = 1e-1;
    
figure();

for ind_rrr = 1:length(rhos)
    
    rho = rhos(ind_rrr);

    [VQS, TQDS] = meshgrid(vqs, tqds);

    VDETS = calc_detection_voltage(VQS,rho,TQDS,Io,s_cu);
    VDET_MIN = ones(size(VDETS))*1e-1;
    VDET_COLOR = ones(size(VDETS))*(4-ind_rrr);

    s = surf(VQS,TQDS,VDETS,VDET_COLOR,'FaceAlpha',1/(4-ind_rrr));
    s.EdgeColor = 'none';
    hold on
end

VDET_MIN = ones(size(VDETS))*vth;
VDET_MIN_COLOR = ones(size(VDETS))*0.1;
%mesh(VQS,TQDS,VDET_MIN,VDET_MIN_COLOR,'FaceAlpha',0.5);
s = surf(VQS,TQDS,VDET_MIN,'FaceAlpha',0.5,'FaceColor',[1 0.5 0.5]);
s.EdgeColor = 'none';


leg = legend([ append("RRR = ",split(num2str(rrrs))); ...
               {"Vth = " + vth*1e3 + " mV"} ] );
%title(leg,'RRR');
leg.Title.Visible = 'on';
xlabel('Propagation velocity [m/s]');
ylabel('Detection time [s]')
zlabel('Detection voltage [V]');
title("Detection analysis @ Cu/NbTi = " + ratio);
set(gca,'FontSize',14);
axis([0 10 0 0.1 0 0.9])