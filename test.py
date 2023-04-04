#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:39:19 2020

@author: acroper
"""

from Mendel import Mendel



Cad = Mendel()
#Cad.setCadnanoBpTurn()
Cad.setDraft()
Cad.SetHoneyComb()


#Cad.RectUp(20,4)
Cad.Add(10)
Cad.UpY()
Cad.Add(10)
Cad.UpY()
Cad.Add(10)
#Cad.UpY()
#Cad.Add(10)


Cad.writeCadnano("/tmp/test.json")
#Cad.RenderRibbons()
Cad.Stats()



