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

Cad.RectDown(10,4)
Cad.RectDown(30,4)
Cad.RectUp(10,8)


Cad.writeCaDNAno("Tests.json")


elapsed = time.time() - t
print(elapsed)



