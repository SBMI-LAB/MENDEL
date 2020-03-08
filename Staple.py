import bpy
from math import radians
import math


class Staple():
    
    Rod1 = None
    Rod2 = None
    
    First = None
    Last = None
    
    LengthFirst = 0
    LengthLast = 0
    
    Crossing = -1
    
    Turn1 = -1
    Turn2 = -1
    
    TouchingFirst = None
    TouchingLast = None
    
    
    def setRelations(this, rod1, rod2):
        this.Rod1 = rod1
        this.Rod2 = rod2
    
    def setStaple (this, cross, bp1, bp2) : 
        this.Crossing = cross
        
        ### First and last is defined in terms of the orientation
        ### This gives a more control about the geometry
        
        this.First = bp1
        this.Last = bp2
        
    def setTurn(this, turn1, turn2):
        this.Turn1 = turn1
        this.Turn2 = turn2
        
    def growStapleStep(this):
        print ("Growing")
        
        ### Attempts to grow the staple. If it touches another
        ### It will mark the other as neighbor
        ## The neighbor staples can be used to decide merge or not
        
    def mergeStaple(this, NextStaple):
        print ("Merging...")
        
        ### Attempts to merge the staples, and remove the other from 
        ### Whatever is controlling this.
        
    def getLengthFirst(this):
        return this.LengthFirst
        
    def getLengthLast(this):
        return this.LengthLast
        
        
        
    
