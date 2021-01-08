#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:39:19 2020

@author: acroper
"""

from Mendel import Mendel
import time

T = 21
TH = 2

M = 8
b = 4
b2 = 2

Cad = Mendel()
#Cad.setDraft()
# Outise box, inside box rotated 90 degrees

##

Cad.StartAt(0)
Cad.RectDown(T,TH-1)
for k in range(2,M):
    if k == b+1:
        Cad.BP2End((b2)*T) 
    if k <= b+1:    
        Cad.RectDown(k*T,TH)
    else:
        Cad.RectDown((k-b2+1)*T,TH)

for k in range(2,M):
    if k == M-b:
        Cad.Add(b2*T) 
    if k < M-b:
        Cad.RectDown((M-k -b2 + 1 )*T,TH)
    else:
        Cad.RectDown((M-k)*T,TH)

# going up
Cad.Growth("Y-")

#Cad.Add(80)
Cad.RectUp(T,TH-1)


for k in range(2,M):
    if k == b+1:
        Cad.BP2End((b2)*T) 
    if k <= b+1:    
        Cad.RectUp(k*T,TH)
    else:
        Cad.RectUp((k-b2+1)*T,TH)
        
for k in range(2,M):
    if k == M-b:
        Cad.Add(b2*T) 
    if k < M-b:
        Cad.RectUp((M-k -b2 + 1 )*T,TH)
    else:
        Cad.RectUp((M-k)*T,TH)        



Cad.Add(6)



#Cad.Clean()
Cad.analyzeStructure()
Cad.writeCadnano("cadnano/design2c.json")

#Cad.RenderRibbons()
Cad.Stats()



