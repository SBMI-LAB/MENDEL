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
    
    TouchingFirstStrand = None
    TouchingLastStrand = None

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
                        Next.StapleStrand = this
                        #Next.setStaple(this)
                        this.CurrentStrand.insert(0,Next)
                        Exito = True
                else:
                    if stp != this.staple:
                        this.TouchingFirst = stp
                        this.TouchingFirstStrand = Next.StapleStrand

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
                        Next.StapleStrand = this
                        #Next.setStaple(this)
                        this.CurrentStrand.append(Next)
                        Exito = True
                else:
                    if stp != this.staple:
                        this.TouchingLast = stp
                        this.TouchingLastStrand = Next.StapleStrand
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
        
    def checkFuse(this):
        ### This should attempt a fuse with one touching
        ## Staple if both have a few count of bp
        ...
        
        """
        if len(this.CurrentStrand) < 18 and len(this.CurrentStrand) > 0:
            ### Check if the limits can be joined
            if this.TouchingFirstStrand != None:
                ### Check here                
                if len(this.TouchingFirstStrand.CurrentStrand) < 18:
                    ### Fuse!!!
                    for item in this.TouchingFirstStrand.CurrentStrand:
                        this.CurrentStrand.append(item)
                    
                    this.TouchingFirstStrand.CurrentStrand.clear()
                    
                    
        """            
                    
            
            
        
        #this.growStep()

    

    
