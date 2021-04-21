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
    
    InitialFolding = None
    EndingFolding = None
    
    Rod = None
    
    StapleList = None
    
    PrevStaple = None
    
    HelixRodList = None
    
    RodList = None
    RodCount = None
    
    RodStapleList = None
    
    NumRods = 0
    
    def SetInitial (this, n, BP):
        this.Initial = n
        
        this.Rod = BP.getRod()
        
        P = BP.getPrev()
        if P != None:
            if P.getRod() != BP.getRod():
                this.InitialRod = P.getRod()
            else:
                P = BP.getNext()
                if P != None:
                    if P.getRod() != BP.getRod():
                        this.InitialRod = P.getRod()
        
        
        
    
    def SetEnd (this, n, BP):
        this.Ending = n
        
        P = BP.getNext()
        if P != None:
            if P.getRod() != BP.getRod():
                this.EndingRod = P.getRod()
            else:
                P = BP.getPrev()
                if P != None:
                    if P.getRod() != BP.getRod():
                        this.EndingRod = P.getRod()
        
        
        
    def AddStp (this, Stp):
        if this.StapleList == None:
            this.StapleList = []
        this.StapleList.append(Stp)
    
    
    def AddToRodList(this, R):
        
        if R != this.Rod and R != None:
            CR = R.currentRod
            if not (CR in this.RodList) :
                this.RodList.append(CR)
                this.RodCount.append(1)
                this.NumRods += 1
                this.HelixRodList.append(R)
            else:
                n = list.index(this.RodList,CR)
                this.RodCount[n] += 1
                
        
    def AddToRodList_Old(this, R):
        
        if R != this.Rod and R != None:
            if not (R in this.RodList) :
                this.RodList.append(R)
                this.RodCount.append(1)
                
            else:
                n = list.index(this.RodList,R)
                this.RodCount[n] += 1
                
    
    def genRodList (this):
        this.HelixRodList = []
        this.RodList = []
        this.RodCount = []
        this.RodStapleList = []
        print("Generating list...")
        if this.StapleList != None:
            for staple in this.StapleList:
                #R1 = staple.getRod1()
                #R2 = staple.getRod2()
                R1 = this.getStapleRod(staple)
                
                this.AddToRodList(R1)
                this.RodStapleList.append(R1.currentRod)
                #this.AddToRodList(R2)

        #print(this.RodCount)    
    def getStapleRod(this, staple):
        R1 = staple.getRod1()
        R2 = staple.getRod2()
        if R1 != None and R1 != this.Rod:
            return R1
        if R2 != None and R2 != this.Rod:
            return R2
        
    
    
    def searchExtremeEssentials(this):
        
        ### It will look for folding (initial rod, ending rod)
        ## And determine the staples in the opposite site
        ## And mark it
        
        if this.StapleList == None:
            return
        
        RodLocal = this.Rod.currentRod
        
        RodSearch = this.RodList.copy()
        
        RodStaples = this.RodStapleList.copy()
        
        stapleList = this.StapleList.copy();
        
        
        ## Search for start staple
        
        InitStaple = None
        EndStaple = None
        
        Pend = this.EndingRod
        
        PIni = this.InitialRod
        
        if Pend == PIni:
            return
        
        pos = []
        
        if Pend != None:
            ### Search the first staple to that rod
            for InStaple in stapleList:
                if  this.getStapleRod(InStaple).currentRod == Pend :
                    InitStaple = InStaple
                    InitStaple.Essential = True
                    InitStaple.Required = True
                    InitStaple.setVote(200)
                    
                    cc = InitStaple.getCrossing()
                    
                    if abs(cc - this.Initial) < 3:
                        InitStaple.IsCornerStrand = True
                        InitStaple.ForceCross = this.Initial
                    
                    pos.append(cc)
                    
                    break
        
        ## Search for ending staple
        
        stapleList.reverse()
        
        if PIni != None:
            ### Search the first staple to that rod
            for InStaple in stapleList:
                if  this.getStapleRod(InStaple).currentRod == PIni :
                    EndStaple =InStaple
                    EndStaple.Essential = True
                    EndStaple.Required = True
                    EndStaple.setVote(200)
                    
                    cc = EndStaple.getCrossing()
                    if abs(cc - this.Ending) < 3:
                        EndStaple.IsCornerStrand = True
                        EndStaple.ForceCross = this.Ending
                    
                    pos.append(EndStaple.getCrossing())
                    break
        
        print("Essentials done")
        
        
    
    
    
    def searchEssentials(this):
        #### Will search through all staples
        ### And select the essentials
        ### This should try to 
        
        if this.StapleList == None:
            return
        
        MinD = 12
        
        LastEssentialRemoved = -1
        
        LStaple = this.StapleList[0]
        LRod = this.RodList[0]
        
        RodLocal = this.Rod.currentRod
        
        RodSearch = this.RodList.copy()
        
        RodStaples = this.RodStapleList.copy()
        
        RodZessentials = []
        RodZpositions = []
        #print("RodSearch: " + str(len(RodSearch)))
        iteracion = 0
        lastRemove = 0
        
        recovery = False
        
        multRods = True
        if len(RodSearch) == 1 or len(RodSearch) == 0:
            multRods = False
        #if LStaple.NonEssential == False:
        #    LStaple.Essential = True
        
        for staple in this.StapleList:
            #if staple != LStaple :}
            iteracion += 1
            if iteracion-lastRemove > 10:
                recovery = True
                
            NRod = this.getStapleRod(staple).currentRod    
            if staple.NonEssential == False:
                NRod = this.getStapleRod(staple).currentRod
                
                if staple.Essential == True :
                    
                    #if staple != LStaple and staple.Required == False :
                    if staple != LStaple :
                        
                        
                        
                        C1 = staple.getCrossing()
                        C2 = LStaple.getCrossing()
                        D = abs(C1-C2)
                        
                        
                        if D < 7:
                            
                            
                            
                            
                            LS_Rod = this.getStapleRod(LStaple).currentRod
                            
                            
                            
                            
                            if LS_Rod == LastEssentialRemoved or LStaple.Required == True:
                            ### Don't remove, instead, remove the other
                                if staple.Required == False:    
                                    staple.Essential = False
                                    staple.NonEssential = True
                                    staple.setVote(-500)
                                    
                                    LastEssentialRemoved = NRod
                            
                            else:
                                ### The previous was wrong chosen
                                if LStaple.Required == False:
                                    LStaple.Essential = False
                                    LStaple.setVote(-500)
                                    LStaple.NonEssential = True
                                    
                                    #RodSearch = this.RodList.copy()  ## Restore the RodSearch
                                    RodSearch.clear()
                                    RodSearch.append(LRod)  ### Force the next that was erased!
                                    
                                    LastEssentialRemoved = LS_Rod
                                    
                                    if len(RodZessentials) > 0:
                                        RodZessentials[-1] = NRod
                                    else:
                                        RodZessentials.append(NRod)
                        else:
                                                    
                            RodZessentials.append(NRod)
                        
                        #RodZessentials.append(NRod)
                        lastRemove = iteracion
                        LStaple = staple
                        LRod = NRod
                        if NRod in RodSearch:
                            RodSearch.remove(NRod)
                            #LStaple.setVote(100)
                        if len(RodSearch) == 0:
                            RodSearch = this.RodList.copy()
                else:
                    
                    if len(RodSearch) == 0 or recovery:
                        RodSearch = this.RodList.copy()
                        if multRods and recovery == False:
                            RodSearch.remove(LRod)
                        recovery = False
                        print("Rebuild RodSearch")
                    #if NRod != LRod:
                    print("Rod Search: " + str(len(RodSearch)) + " | " + str(len(this.RodList)) + " | "   +str(len(this.StapleList)))
                    #print(RodSearch)
                    if NRod in RodSearch:
                        C1 = staple.getCrossing()
                        C2 = LStaple.getCrossing()
                        D = abs(C1-C2)
                        
                        if D > MinD :
                            LStaple = staple
                            LStaple.Essential = True
                            LRod = NRod
                            staple.setVote(500)
                            RodZessentials.append(NRod)
                            RodZpositions.append(C1)
                            RodSearch.remove(NRod)
                            lastRemove = iteracion
                            #if len(RodSearch) == 0:
                            #    RodSearch = this.RodList.copy()
                            #    RodSearch.remove(NRod)
                            #    print("Rebuild RodSearch")
                            
                        else:
                            staple.NonEssential = True
                            staple.setVote(-100)
                    else:
                        staple.NonEssential = True
                    #else:
                        #if len(RodSearch) == 1:
                    #    print("Wow")
        print("Next")
                    
            

    
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
        Umbral = 4
        #staple.removeStaple()
        #Extreme corner
        if D1 < Umbral or D2 < Umbral:
            
            if D1 < D2 and (T == this.InitialRod or this.InitialRod == None):
                staple.setVote(3)
            
            if D1 > D2 and (T == this.EndingRod or this.EndingRod == None):
                staple.setVote(3)
            
            staple.setVote(-10)
            #None
        Umbral = 5
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
                
                if this.PrevStaple.getVote() > staple.getVote() and staple.Essential != True:
                    this.PrevStaple.setVote(10)
                    staple.removeStaple()
                    staple = this.PrevStaple
                #else:
                #    staple.setVote(10)
                #    this.PrevStaple.removeStaple()
                
            
        this.PrevStaple = staple
        
        None
        
    
    def CleanStaples(this):
        # Follow some rules to reduce the staples
        if this.StapleList != None:
            print(len(this.StapleList))
            for staple in this.StapleList:
                #clean umbral
                VoteUmbral = 10
                if staple.getVote() < VoteUmbral:
                    staple.removeStaple()
                