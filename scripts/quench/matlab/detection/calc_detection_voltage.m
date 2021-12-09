function vdet = calc_detection_voltage(vq,rho,tqd,Io,Acu)

vdet = vq.*tqd.*rho.*Io./Acu;