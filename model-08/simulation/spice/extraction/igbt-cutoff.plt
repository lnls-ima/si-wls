[Transient Analysis]
{
   Npanes: 4
   {
      traces: 1 {524296,0,"V(Vpsoutp)*Ix(U1:C)+V(N002)*Ix(U1:G)+V(VE1)*Ix(U1:E)"}
      X: ('m',0,0.03,0.009,0.1)
      Y[0]: (' ',0,0,10,10)
      Y[1]: ('K',0,1e+308,2000,-1e+308)
      Units: "W" (' ',0,0,0,0,10,10)
      Log: 0 0 0
      Text: "W" 1 (0.272445019404916,266.666666666667) ;Power dissipation
      Text: "W" 13 (0.0239543726235741,264.583333333333) ;IGBT 
      Text: "W" 4 (0.0182509505703422,129.166666666667) ;Qres
      Text: "W" 12 (0.131178707224335,77.0833333333333) ;Freewheel diode
   },
   {
      traces: 3 {524290,0,"V(vpsoutp)-V(ve1)"} {524297,0,"V(ve1)-V(vmagnetp)"} {268959754,0,"V(vpsoutp)"}
      X: ('m',0,0.03,0.009,0.1)
      Y[0]: (' ',0,-60,60,600)
      Y[1]: (' ',2,1e+308,0.05,-1e+308)
      Volts: (' ',0,0,0,-60,60,600)
      Log: 0 0 0
   },
   {
      traces: 1 {336592902,0,"Ix(U1:C)"}
      X: ('m',0,0.03,0.009,0.1)
      Y[0]: ('m',0,0,0.05,0.05)
      Y[1]: (' ',0,1e+308,50,-1e+308)
      Amps: ('m',0,0,0,0,0.05,0.05)
      Log: 0 0 0
   },
   {
      traces: 3 {268959748,0,"V(swdelay)"} {268959749,0,"V(psdelay)"} {268959747,0,"V(igbtdriver)"}
      X: ('m',0,0.03,0.009,0.1)
      Y[0]: (' ',1,0,0.1,1.1)
      Y[1]: (' ',0,1e+308,50,-1e+308)
      Volts: (' ',0,0,0,0,0.1,1.1)
      Log: 0 0 0
   }
}
