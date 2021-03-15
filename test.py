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



W = 210

Cad = Mendel()

Cad.Growth("Z+")
Cad.Add(50)
Cad.RectUp(W-100,1)
Cad.Add(W-100)



Cad.DownY()
Cad.Growth("Y+")
Cad.RectDown(W,1)

Cad.Growth("Z+")
Cad.DownZ()
Cad.RectDown(W,1)
Cad.Growth("Y+")
Cad.RectDown(W,1)
Cad.Growth("Z-")
#Cad.DownZ()
Cad.RectDown(W,1)
Cad.Growth("Y+")
Cad.DownZ()
Cad.RectUp(W,1)

Cad.UpY()
Cad.Growth("Z+")
Cad.RectUp(W,2)
Cad.UpY()
Cad.Add(W)
Cad.UpZ()
Cad.Add(80)




#Cad.Clean()

#Cad.writeCadnano("cadnano/testbench3_B.json")
Cad.writeCadnano("cadnano/test1B3.json")



#Cad.RenderRibbons()
Cad.Stats()



