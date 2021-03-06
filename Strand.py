Blender = False
try:
    import bpy
    Blender = True
except:
    None
    
from math import radians
import math


class Strand():

    First = None
    Last = None

    LengthFirst = -1
    LengthLast = -1

    Crossing = -1

    TouchingFirst = None
    TouchingLast = None

    Enabled = False

    staple = None

    CurrentStrand = None


    def setStrand(this, Lista, stp):
        this.CurrentStrand = Lista
        this.staple = stp


    def growStep(this):
        if this.CurrentStrand != None and this.staple != None:
            if len(this.CurrentStrand) > 0:
                #print("Grow strand")
                this.growFirst()
                this.growLast()

    def setLine(this):
        print("Converting to line")
        for BP in this.CurrentStrand:
            BP.setStaple(None)

        this.CurrentStrand.clear()
        this.CurrentStrand.append(this.First)
        this.growStep()

    def growFirst(this):
        #print("Growing first")
        Exito = False

        First = this.First = this.CurrentStrand[0]
        if First != None :
            #Next = this.First.getNext()
            Next = this.First.getNextRod()
            if Next != None and Next != First:
                dx = abs(Next.getX() - First.getX())
                stp = Next.getStaple()
                if stp == None:
                    #print("Growing first: " + str(dx))
                    #if Next.getRod() == First.getRod() and dx == 1:
                    if Next.getRod() == First.getRod() and dx <= 1:
                        this.First = Next
                        Next.setStaple(this.staple)
                        this.CurrentStrand.insert(0,Next)
                        Exito = True
                else:
                    if stp != this.staple:
                        this.TouchingFirst = stp

        return Exito


    def growLast(this):
        #print("Growing last")
        Exito = False

        Last = this.Last = this.CurrentStrand[-1]

        if Last != None :
            #Next = this.Last.getPrev()
            Next = this.Last.getPrevRod()
            if Next != None and Next != Last:

                dx = abs(Next.getX() - Last.getX())
                stp = Next.getStaple()
                if stp == None:
                    #if Next.getRod() == Last.getRod() and dx == 1:
                    if Next.getRod() == Last.getRod() and dx <= 1:
                        this.Last = Next
                        Next.setStaple(this.staple)
                        this.CurrentStrand.append(Next)
                        Exito = True
                else:
                    if stp != this.staple:
                        this.TouchingLast = stp
        return Exito


    def growEnd(this):

        #this.growStep()
        #print("Growing")

        if True: 
            
            if this.First != None:
                if len(this.CurrentStrand) > 0:
                    Pase = True
                    while Pase :
                        #print(this.First.getX())
                        Pase = this.growFirst()
            
            this.growStep()
            
            if this.Last != None:
                if len(this.CurrentStrand) > 0:
                    Pase = True
                    while Pase :
                        Pase = this.growLast()
                        
                        
   
  



    def tryFuse(this):
        
        print("Try fuse")

        First = this.CurrentStrand[0]
        for BP in this.CurrentStrand:
            BP.setStaple(None)

        this.CurrentStrand.clear()

        this.CurrentStrand.append(First)

        First.setStaple(this.staple)
        
        #this.growStep()

    

    
