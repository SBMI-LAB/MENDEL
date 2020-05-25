#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:39:19 2020

@author: acroper
"""

from Mendel import Mendel
import time

t = time.time()

W = 200 # Width of the cage
T = 3 # Thikness of the cage

T = T-1
Cad = Mendel()
#Cad.setDraft()
X = 40
print("Start")
Cad.StartAt(0)

Cad.RectDown(5,2)
Cad.RectUp(5,2)


Cad.writeCaDNAno("Tests.json")

Cad.Stats()

elapsed = time.time() - t
print(elapsed)



