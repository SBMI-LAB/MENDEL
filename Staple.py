import bpy
from math import radians
import math


class Staple():
    
    Rod1 = None
    Rod2 = None
    
    r1 = -1
    r2 = -1
    
    First_1 = None
    Last_1 = None
    
    First_2 = None
    Last_2 = None
    
    LengthFirst_1 = 0
    LengthLast_1 = 0
    
    LengthFirst_2 = 0
    LengthLast_2 = 0
    
    Crossing = -1
    
    Turn1 = -1
    Turn2 = -1
    
    TouchingFirst_1 = None
    TouchingLast_1 = None
    
    TouchingFirst_2 = None
    TouchingLast_2 = None
    
    FirstStrand = None
    SecondStrand = None
    
    Recursive1 = False
    Recursive2 = False
    
    
    Conflicts = None

    Enabled = False

    Ignored = False
    

    def setIgnored (this):
        this.Ignored = True

    def isIgnored(this):
        return this.Ignored

    def isEnabled(this):
        return this.Enabled

    def getFirstStrand(this):
        return this.FirstStrand
    
    def getSecondStrand(this):
        return this.SecondStrand
    
    
    def setRelations(this, rod1, rod2):
        this.Rod1 = rod1
        this.Rod2 = rod2
        this.FirstStrand = []
        this.SecondStrand = []

    def getRod1(this):
        return this.Rod1
    
    def getRod2(this):
        return this.Rod2

    
    def setStaple (this, cross, row1, row2) : 
        this.Crossing = cross
        
        Exito = True
        
        ### First and last is defined in terms of the orientation
        ### This gives a more control about the geometry
        
        bp_11 = row1[cross]
        bp_12 = row1[cross+1]
        
        bp_21 = row2[cross]
        bp_22 = row2[cross+1]
        
        caso = False
        
        if bp_11.getOz() == 0 or bp_11.getOz() == 360:
            caso = not caso
        
        if caso:
            this.First_1 = bp_21
            this.Last_1  = bp_11
            
            this.First_2 = bp_12
            this.Last_2  = bp_22
        else:
            this.First_1 = bp_11
            this.Last_1  = bp_21
            
            this.First_2 = bp_22
            this.Last_2  = bp_12                                 
        
        try:

            this.Conflicts = []
            if bp_11.getStaple() != None :
                this.Conflicts.append(bp_11.getStaple())
            if bp_12.getStaple() != None :
                this.Conflicts.append(bp_12.getStaple())
            if bp_21.getStaple() != None :
                this.Conflicts.append(bp_21.getStaple())
            if bp_22.getStaple() != None :
                this.Conflicts.append(bp_22.getStaple())


            if bp_11.getStaple() != None or bp_12.getStaple() != None or bp_21.getStaple() != None or bp_22.getStaple() != None :
                Exito = False           
            else:
                this.r1 = this.First_1.getRod()
                this.r2 = this.Last_1.getRod()
                
                this.FirstStrand.append(this.First_1)
                this.FirstStrand.append(this.Last_1)
                
                this.SecondStrand.append(this.First_2)
                this.SecondStrand.append(this.Last_2)
                
                bp_11.setStaple(this)
                bp_21.setStaple(this)
                
                bp_12.setStaple(this)
                bp_22.setStaple(this)
            
        except: 
            Exito = False
        
        this.Enabled = Exito
        
        return Exito
        
    def hasConflicts(this):
        if len(this.Conflicts) > 0 :
            return True
        else:
            return False

    def getConflicts(this):
        return this.Conflicts

    def setTurn(this, turn1, turn2):
        this.Turn1 = turn1
        this.Turn2 = turn2
        
    def growStapleStep(this):
 
        
        ### Attempts to grow the staple. If it touches another
        ### It will mark the other as neighbor
        ## The neighbor staples can be used to decide merge or not
        
        ###  Remember HERE scaffold have opposite directions to staples
        
        if this.Enabled :
            P1 = this.growStrand (this.FirstStrand, this.First_1, this.Last_1, this.TouchingFirst_1, this.TouchingLast_1)
            this.First_1 = P1[0]
            this.Last_1 = P1[1]
            this.TouchingFirst_1 = P1[2]
            this.TouchingLast_1 = P1[3]  

            P2 = this.growStrand (this.SecondStrand, this.First_2, this.Last_2, this.TouchingFirst_2, this.TouchingLast_2)
            this.First_2 = P2[0]
            this.Last_2 = P2[1]
            this.TouchingFirst_2 = P2[2]
            this.TouchingLast_2 = P2[3]

            
    def growStrand (this, Elements, First, Last, TouchingFirst, TouchingLast):    

        bp1 = First.getNext()  ## Next BP in scaffold
        bp2 = Last.getPrev()   ## Prev BP in scaffold

        if bp1 != None and this.Recursive1 == False:
            
            stp1 = bp1.getStaple()
            
            ### Not in a turn
            ### Check if they don't have staple            
            
            if stp1 == None and bp1.getRod() == First.getRod():
                # ~ print("Growing")
                First = bp1
                bp1.setStaple(this)
                Elements.insert(0, First)
            else:
                if stp1 != this:
                    TouchingFirst = stp1 ### Touches other staple
                else:
                    #print("Recursive 1")
                    this.Recursive1 = True
                
        if bp2 != None and this.Recursive2 == False:            
            stp2 = bp2.getStaple()
            
        
            if stp2 == None and bp2.getRod() == Last.getRod() :
                # ~ print("Growing")
                Last = bp2
                bp2.setStaple(this)
                Elements.append(bp2)
            else:
                if stp2 != this :
                    TouchingLast = stp2    
                else:
                    #print("Recursive 2")
                    this.Recursive2 = True
        
        P = (First, Last, TouchingFirst, TouchingLast)
        return P
    
    
    def getFirst1(this):
        return this.First_1
    
    def getFirst2(this):
        return this.First_2
    
    def mergeNext(this):
        print("Looking touch")
        if this.TouchingLast_1 != None :
            #print("Looking touch2")
            ### Merge next element just in case
            Next = this.TouchingLast_1.getFirst2()
            Prev = Next.getNext()
            
            Test = this.Last_1
            
            if Prev == Test :
                Test.setNextStp(Next)
                Next.setPrevStp(Test)
                print("Merging...")

            Test = this.Last_2
            
            if Prev == Test :
                Test.setNextStp(Next)
                Next.setPrevStp(Test)
                print("Merging...")                
     
    
    def mergePrev(this):
        print("Looking touch")
        if this.TouchingLast_2 != None :
            print("Looking touch2")
            ### Merge next element just in case
            Next = this.TouchingLast_2.getFirst1()
            Prev = Next.getNext()
            
            Test = this.Last_1
            
            if Prev == Test :
                Test.setNextStp(Next)
                Next.setPrevStp(Test)
                print("Merging...")

            Test = this.Last_2
            
            if Prev == Test :
                Test.setNextStp(Next)
                Next.setPrevStp(Test)
                print("Merging...")            
                
        
    def mergeStaple(this, NextStaple):
        print ("Merging...")
        
        ### Attempts to merge the staples, and remove the other from 
        ### Whatever is controlling this.
        
    def applyStaple(this):
        # Set the configuration to the BP of the staples
        this.applyStrand(this.First_1, this.Last_1, this.FirstStrand)
        this.applyStrand(this.First_2, this.Last_2, this.SecondStrand)
        #print("Applying")
        
    
    def applyStrand(this, First, Last, Elements):    
        ## Set begining:

        if this.Enabled:

            First.setPrevStp(None)
            
            Previo = First
            
            for BP in Elements:
                if BP != Previo:
                    Previo.setNextStp(BP)
                    BP.setPrevStp(Previo)
                    Previo = BP
            
            ## Set ending:
            Last.setNextStp(None)
        
        
        
        
    def getLengthFirst(this):
        return this.LengthFirst
        
    def getLengthLast(this):
        return this.LengthLast
        
        
        
    
