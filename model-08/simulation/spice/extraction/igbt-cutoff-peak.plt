[Transient Analysis]
{
   Npanes: 1
   {
      traces: 3 {524292,2,"V(Vpsoutp)*Ix(U1:C)+V(N002)*Ix(U1:G)+V(VE1)*Ix(U1:E)"} {524290,0,"V(vpsoutp)-V(ve1)"} {336592899,1,"Ix(U1:C)"}
      X: ('m',2,0.046,9e-005,0.047)
      Y[0]: (' ',0,0,70,620)
      Y[1]: (' ',0,0,30,240)
      Volts: (' ',0,0,0,0,70,620)
      Amps: (' ',0,0,0,0,30,240)
      Units: "W" ('K',0,0,0,0,2000,35000)
      Log: 0 0 0
      Text: "W" 1 (0.272445019404916,266.666666666667) ;Power dissipation
      Text: "W" 13 (0.0239543726235741,264.583333333333) ;IGBT 
      Text: "W" 4 (0.0182509505703422,129.166666666667) ;Qres
      Text: "W" 12 (0.131178707224335,77.0833333333333) ;Freewheel diode
   }
}
