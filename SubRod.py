Blender = False
try:
    import bpy
    Blender = True
except:
    from Staple import *
    
from math import radians
import math

class SubRod():
    
    Initial = -1
    Ending = -1
    
    InitialRod = None
    EndingRod = None
    
    Rod = None
    
    StapleList = None
    
    PrevStaple = None
    
    def SetInitial (this, n, BP):
        this.Initial = n
        
        this.Rod = BP.getRod()
        
        P = BP.getPrev()
        if P != None:
            if P.getRod() != BP.getRod():
                this.InitialRod = P.getRod()
        
        
        
    
    def SetEnd (this, n, BP):
        this.Ending = n
        
        P = BP.getNext()
        if P != None:
            if P.getRod() != BP.getRod():
                this.EndingRod = P.getRod()
        
        
        
    def AddStp (this, Stp):
        if this.StapleList == None:
            this.StapleList = []
        this.StapleList.append(Stp)
    
    
    def ReduceVote(this):
        # Vote for staples to reduce them
        # Eval some variables: starting from the length
        
        #Parameters for reduce/vote
        
        """
        |-------| Minimum distance to edge.
        """
        #L = this.Ending - this.Initial
        
        if this.StapleList != None:
            print(len(this.StapleList))
            for staple in this.StapleList:
                if staple.isEnabled():
                    this.VoteDistance(staple)
        
        
        None
        
    def VoteDistance(this, staple):
        
        ## Extreme corner, but can cross
        R1 = staple.getRod1()
        R2 = staple.getRod2()
        
        T = R1.getNumber()
        
        if R1.getNumber() == this.Rod:
            T = R2.getNumber()
            
        # this will check the staples and vote
        # if it is close to the end of the rod
        C = staple.getCrossing()
        D1 = C - this.Initial
        
        D2 = this.Ending - C
        
        print("D1: " + str(D1))
        print("D2: " + str(D2))
        
        #minimum
        Umbral = 2
        #staple.removeStaple()
        #Extreme corner
        if D1 < Umbral or D2 < Umbral:
            
            if D1 < D2 and (T == this.InitialRod or this.InitialRod == None):
                staple.setVote(3)
            
            if D1 > D2 and (T == this.EndingRod or this.EndingRod == None):
                staple.setVote(3)
            
            staple.setVote(-10)
            #None
        Umbral = 7
        #staple.removeStaple()
        if D1 < Umbral or D2 < Umbral:
            staple.setVote(-2)
        
        
        
        # T is the target cross
        if this.InitialRod == T and D1 == 0:
            # Save the crossing
            staple.setVote(10)
        
        if this.EndingRod == T and D2 == 0:
            # Save the crossing
            staple.setVote(10)
        
        
        ### PrevDistance
        
        
        if this.PrevStaple != None and this.PrevStaple != staple:
            C2 = this.PrevStaple.getCrossing()
            
            Umbral = 10
            D = abs(C-C2)
            if D < Umbral:
                ### Erase one of them, first vote
                this.PrevStaple.setVote(-5)
                staple.setVote(-5)
                
                if this.PrevStaple.getVote() > staple.getVote() :
                    this.PrevStaple.setVote(10)
                    staple.removeStaple()
                    staple = this.PrevStaple
                else:
                    staple.setVote(10)
                    this.PrevStaple.removeStaple()
                
            
        this.PrevStaple = staple
        
        None
        
    
    def CleanStaples(this):
        # Follow some rules to reduce the staples
        if this.StapleList != None:
            print(len(this.StapleList))
            for staple in this.StapleList:
                #clean umbral
                VoteUmbral = 0
                if staple.getVote() < VoteUmbral:
                    staple.removeStaple()
                