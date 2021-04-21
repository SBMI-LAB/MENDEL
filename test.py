#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:39:19 2020

@author: acroper
"""

from Mendel import Mendel



"""
Cad = Mendel()
#Cad.setDraft()
#Cad.Add(20)
T = 40
for k in range(3):
    Cad.RectDown(T,4)
for k in range(3):
    Cad.RectUp(T,4)

Cad.Growth("Z-")
Cad.RectUp(7*T,4)


Cad.writeCadnano("cadnano/test1.json")
"""

Cad = Mendel()

F = 14
TH = 2
T = TH*F

Cad.Add(40)
for k in range(4):
    Cad.RectUp(T,6, -20)
    
Cad.RectUp(40,2)
Cad.Add(40)
Cad.RectDown(4*T,2)
    
    


#
#F = 11
#
#TH = 2
#WH = 8
#
#T = TH*F
#W = WH*F
#
#H = 8
#HL = 4
#TT = 3
#
#
#Cad = Mendel()
#
#
#
#for L in range(1):
#    Cad.Add(40)
#    for k in range(H):
#        Cad.RectUp(T,TH)
#
#    Cad.Add(3*T)
#    Cad.DownY()
#    Cad.Add(3*T)
#    Cad.DownY()
#
#
#    Cad.RectDown(T,HL*TH-2)    
#    Cad.Growth("Y-")
#    Cad.RectDown((HL+4)*T, TH) # Touching bar
#
#    Cad.RectDown(T,0.5*H+2)
#
#
#    ## T
#    Cad.Growth("Y+")
#    Cad.Add(5*T)
#    Cad.RectUp(T, H*TH-2*TH+1)
#    Cad.Growth("Y-")
#
#    Cad.RectUp(TT*T,TH+1) # Original
#
#    Cad.Growth("Y+")
#    Cad.RectDown(2*TT*T, TH)
#    #Returning 
#
#    Cad.DownY()
#
#    Cad.Growth("Y+")
#    Cad.Add((TT+2)*T)
#    Cad.DownY()
#
#    Cad.RectDown(T,TH*(H-2))
#
#    Cad.Add(20)
#    Cad.DownY()
#    Cad.GotoX(0)
#    
#    if L == 0:
#        Cad.UpZ()



#Cad.Clean()

#Cad.writeCadnano("cadnano/testbench3_B.json")
Cad.writeCadnano("cadnano/test1R.json")



#Cad.RenderRibbons()
Cad.Stats()



