import bpy
from math import radians
import math


class HelixRod():
    
    currentRod = 0
    ispair = True
    row = []
    
    y = 0
    z = 0
    
    #### Interaction with other Helix Rods:
    ###
    ##           YN
    ##      ZN  This   ZP
    ##           YP
    ##
    
    
    YP = None
    YN = None
    ZP = None
    ZN = None
    
    YPS = None
    YNS = None
    ZPS = None
    ZNS = None
    
    YPSa = None
    YNSa = None
    ZPSa = None
    ZNSa = None   
    
    maxStaple = 0 
    
    def getYPS(this):
        return this.YNS
    def getYNS(this):
        return this.YPS
    def getZPS(this):
        return this.ZNS
    def getZNS(this):
        return this.ZPS
        
    def getYPSa(this):
        return this.YNSa
    def getYNSa(this):
        return this.YPSa
    def getZPSa(this):
        return this.ZNSa
    def getZNSa(this):
        return this.ZPSa  
    
    
    def setStaple(this, pos, OtherHelix):
        # ~ print("Adding: " + str(pos));
        
        if OtherHelix == this.YN:
            this.YNS.append(pos)
            # ~ print("YNS")
        if OtherHelix == this.ZP:
            this.ZPS.append(pos)
            # ~ print("ZPS")
        if OtherHelix == this.ZN:
            this.ZNS.append(pos)
            # ~ print("ZNS")
        if OtherHelix == this.YP:
            this.YPS.append(pos)
            # ~ print("YPS")            
            
        
        this.maxStaple += 1  
        

    def setStapleNew(this, pos, OtherHelix):
        ### This new concept will create a staple object instead
        ### of just the list of positions.
        ### 

        #print("Rod: " + str(this.currentRod))
        
        SObj = Staple()
        SObj.setRelations(this, OtherHelix)
        K = SObj.setStaple(pos, this.getRow(), OtherHelix.getRow())
        

        if K == False:
            if SObj.hasConflicts():
                OtherStaple = SObj.getConflicts()[0]
                
                R1 = OtherStaple.getRod1()
                R2 = OtherStaple.getRod2()

                R1a = this
                R2a = OtherHelix 



                if (R1 == R1a and R2 == R2a ) or (R1 == R2a and R2 == R1a):
                    ### Has the same rods in conflict, so, this should be ignored
                    SObj.setIgnored()
                    #print("Ignoring: " + str(this.currentRod )  + "  R1: " + str(R1.getNumber()) + " R2: " + str(R2.getNumber())  )



        if SObj.isIgnored() == False:
        
            if OtherHelix == this.YN:
                this.YNS.append(SObj)
                
            if OtherHelix == this.ZP:
                this.ZPS.append(SObj)
                
            if OtherHelix == this.ZN:
                this.ZNS.append(SObj)
                
            if OtherHelix == this.YP:
                this.YPS.append(SObj)
                      
            
        
        #if K: 
        return SObj
        #else:
        #    return False

        # ~ this.maxStaple += 1  
        

    def ReduceStaples(this, minSize):
        Listas = [ this.YNS, this.YPS, this.ZNS, this.ZPS ]
        
        for Lista in Listas:
            if Lista != None:
                for Elem in Lista:
                    if Elem != None :
                        try:
                            Elem.tryFuseStaple(minSize)
                            #Elem.tryMergeStaples()
                        except:
                            None

        ## Repeat to reduce lines                            
    def ReduceStaplesLines(this):
        Listas = [ this.YNS, this.YPS, this.ZNS, this.ZPS ]
        for Lista in Listas:
            if Lista != None:
                for Elem in Lista:
                    if Elem != None :
                        try:
                            Elem.tryMergeSingleLines()
                            #print("")
                        except:
                            None

        ## Repeat to reduce lines   
                                 
    def ReduceStaplesCrossings(this):
        Listas = [ this.YNS, this.YPS, this.ZNS, this.ZPS ]
        for Lista in Listas:
            if Lista != None:
                crossingInd = []
                crossingStp = []
                crossingVote = []
                for staple in Lista:
                    cs = staple.getCrossing()
                    if cs != -1 :
                        crossingInd.append(cs)
                        crossingStp.append(staple)
                        crossingVote.append(0)
                
                ## here the crossings are now ready, so, we need to choose which of them 
                ## are going to be preserved or which are going to be history
                print("Reducing crossings..." + str(len(crossingVote)))
                ### All data is in crossingInd and according to them, choose to preserve or not in crossingStp
                if len(crossingVote) > 2 :
                    crossingVote[0] = -4
                    crossingVote[-1] = -4

                    for k in range(1,len(crossingInd)-1) :
                        k2 = len(crossingInd)-1-k
                        d1 = abs(crossingInd[k] - crossingInd[k-1])
                        d2 = abs(crossingInd[k] - crossingInd[k-2])

                        X1 = min((d1,d2)) - 0.5 * crossingVote[k-1]


                        d3 = abs(crossingInd[k2] - crossingInd[k2-1])
                        d4 = abs(crossingInd[k2] - crossingInd[k2-2])

                        X2 = min((d3,d4)) - 0.5 * crossingVote[k2+1]

                        crossingVote[k] = X1
                        if k != k2:
                            crossingVote[k2] = X2
                    

                    ## Once finished the votings, we can select them, which are maximum and then erase the others
                    maximus = max(crossingVote)
                    print(crossingInd)
                    print(crossingVote)
                    for k in range(0,len(crossingInd)) :
                        if crossingVote[k] < maximus:
                            print("Merge into lines " + str(crossingVote[k]))
                            crossingStp[k].tryFuseStaple(14)

                    



                    
                    


                                              

    def checkConflicts(this):
        #print("Checking conflicts...")
        this.solveConflicts(this.YNS)
        this.solveConflicts(this.YPS)
        this.solveConflicts(this.ZNS)
        this.solveConflicts(this.ZPS)

    def solveConflicts(this, Lista):
        ## This function will perform two basic things:
        ## 1. Solve conflicts
        ## 2. Decide which elements are preserved after conflicts

        ### Lista is one of the lists generated by during association.
        ### each has the staples associated by between two rods
        ### each staple has information of the other staple associated
        ### and can be checked

        """
            ______..____
            ______||____

        """
        if Lista != None:
        ### First case: detect conflict
            Total = len(Lista)
            Actives = 0
            n = 0
            for Elem in Lista:
                if Elem != None :
                    if Elem.hasConflicts() == True :
                        n += 1
                    if Elem.isEnabled() :
                        Actives += 1
            #if Total == 0:
            #    print("Rod: "+str(this.currentRod)+") Conflicting staples " + str(n) + " Active staples :" + str(Actives) + " Total: " + str(Total))  

          
    
    def getStapleListBP (this):
        ### Generate List of BP for staples
        Lista = []
        
        for k in this.YNS:
            if k != -1:
                BP1 = this.row[k]
                BP2 = this.YN.getRow()[k]
                P = (BP1, BP2)
                Lista.append(P)
        for k in this.YPS:
            if k != -1:
                BP1 = this.row[k]
                BP2 = this.YP.getRow()[k]
                P = (BP1, BP2)
                Lista.append(P)
        for k in this.ZNS:
            if k != -1:
                BP1 = this.row[k]
                BP2 = this.ZN.getRow()[k]
                P = (BP1, BP2)
                Lista.append(P)
        for k in this.ZPS:
            if k != -1:
                BP1 = this.row[k]
                BP2 = this.ZP.getRow()[k]
                P = (BP1, BP2)
                Lista.append(P)                                   
                
        return Lista





    def analyzeStaple(this):
        ### It's a function that analyzes the staples and take a decision
        ### To approve or remove staple
        
        if this.YNS == None:
            this.YNS = []
        if this.YPS == None:
            this.YPS = []
            
        if this.ZNS == None:
            this.ZNS = []
        if this.ZPS == None:
            this.ZPS = []
            
        YNS = this.YNS
        YPS = this.YPS
        ZNS = this.ZNS
        ZPS = this.ZPS            
            
        
        print(len(YPS))
        
        maxim = max(len(YNS),len(YPS),len(ZNS),len(ZPS))
        print ("Maximo: " + str(maxim) + " out of " + str(this.maxStaple))
        
        ### Analize all of them
        
        ### Recorrer la helice item por item, incremental.
        ### Tomar en cuenta de la distancia del ultimo elemento agregado.
        ### Dar una opcion de aprobación o desaprobación (sumar y restar)
        ### Finalmente dar la decisión en otra estructura después del análisis
        
        pYN = -1
        pYP = -1
        pZN = -1
        pZP = -1
        
        mYN = -1
        mYP = -1
        mZN = -1
        mZP = -1
        
        MinDistance = 7
        
        Low = 4
        
        DYN = 0
        DYP = 0
        DZP = 0
        DZN = 0
        
        
        for k in range (1,maxim):
            
            ### YNS
            """
            if k < len(this.YNS) :
                if k == 1:
                    pYN = this.YNS[0]
                    mYN = this.YNS[-1]
                
                pD = DYN
                DYN = abs(this.YNS[k] - pYN)
                pYN = this.YNS[k]
                DF = abs (mYN - this.YNS[k])
                
                D1 = abs(pYN - pYP)
                D2 = abs(pYN - pZN)
                D3 = abs(pYN - pZP)
                
                Cal = 0
                
                if DYN > MinDistance:
                    Cal +=1
                if pD > 2*MinDistance:
                    Cal += 2
                
                if DF > MinDistance: 
                    Cal += 1
                else:
                    Cal -= 2
                    
                if D1 < Low or D2 < Low or D3 < Low:
                    Cal -= 2
                
                if len(this.YNSa) < k+1:
                    this.YNSa.append(Cal)
                else:
                    this.YNSa[k] += Cal

            ### YPS
            if k < len(this.YPS) :
                if k == 1:
                    pYP = this.YPS[0]
                    mYP = this.YPS[-1]
                
                pD = DYP
                DYP = abs(this.YPS[k] - pYP)
                pYP = this.YPS[k]
                DF = abs (mYP - this.YPS[k])
                
                D1 = abs(pYN - pYP)
                D2 = abs(pYP - pZN)
                D3 = abs(pYP - pZP)
                
                
                Cal = 0
                if DYP > MinDistance:
                    Cal +=1
                if pD > 2*MinDistance:
                    Cal += 2
                
                if DF > MinDistance: 
                    Cal += 1
                else:
                    Cal -= 2   
                
                if D1 < Low or D2 < Low or D3 < Low:
                    Cal -= 2
                
                # ~ this.YPSa.append(Cal)
                if len(this.YPSa) < k+1:
                    this.YPSa.append(Cal)
                else:
                    this.YPSa[k] += Cal
                
            ### ZNS
            if k < len(this.ZNS) :
                if k == 1:
                    pZN = this.ZNS[0]
                    mZN = this.ZNS[-1]
                
                pD = DZN
                DZN = abs(this.ZNS[k] - pZN)
                pZN = this.ZNS[k]
                DF = abs (mZN - this.ZNS[k])
                
                D1 = abs(pZN - pZP)
                D2 = abs(pZN - pZN)
                D3 = abs(pZN - pZP)
                
                Cal = 0
                
                if DZN > MinDistance:
                    Cal +=1
                if pD > 2*MinDistance:
                    Cal += 2
                
                if DF > MinDistance: 
                    Cal += 1
                else:
                    Cal -= 2
                    
                if D1 < Low or D2 < Low or D3 < Low:
                    Cal -= 2
                
                # ~ this.ZNSa.append(Cal)
                if len(this.ZNSa) < k+1:
                    this.ZNSa.append(Cal)
                else:
                    this.ZNSa[k] += Cal
                
            ### ZPS
            # ~ if k < len(this.ZPS) :
                # ~ if k == 1:
                    # ~ pZP = this.ZPS[0]
                    # ~ mZP = this.ZPS[-1]
                
                # ~ pD = DZP
                # ~ DZP = abs(this.ZPS[k] - pZP)
                # ~ pZP = this.ZPS[k]
                # ~ DF = abs (mZP - this.ZPS[k])
                
                # ~ D1 = abs(pZN - pZP)
                # ~ D2 = abs(pZP - pZN)
                # ~ D3 = abs(pZP - pZP)
                
                
                # ~ Cal = 0
                # ~ if DZP > MinDistance:
                    # ~ Cal +=1
                # ~ if pD > 2*MinDistance:
                    # ~ Cal += 2
                
                # ~ if DF > MinDistance: 
                    # ~ Cal += 1
                # ~ else:
                    # ~ Cal -= 2   
                
                # ~ if D1 < Low or D2 < Low or D3 < Low:
                    # ~ Cal -= 2
                
                
                # ~ if len(this.ZPSa) < k+1:
                    # ~ this.ZPSa.append(Cal)
                # ~ else:
                    # ~ this.ZPSa[k] += Cal   
            """
            
            pYN = this.analyzeRod(k,this.YNS, this.YNSa, DYN, pYP, pZP, pZN)
            pYP = this.analyzeRod(k,this.YPS, this.YPSa, DYP, pYN, pZP, pZN)
            pZN = this.analyzeRod(k,this.ZNS, this.ZNSa, DZN, pYN, pZP, pYP)
            pZP = this.analyzeRod(k,this.ZPS, this.ZPSa, DZP, pYN, pYP, pZN)
                            
        
    def analyzeRod(this, k, ZPS, ZPSa, DZP, D1,D2,D3):
        
        MinDistance = 20
        RealMin = 7
        Low = 4
        
        pZP = -1
        
        if k < len(ZPS) :
            pZP = ZPS[0]    ### First staple
            mZP = ZPS[-1]   ### Last staple
            
            pD = DZP                    ## Distance of previous staple
            DZP = abs(ZPS[k] - pZP)     ## Distance from the first edge
            pZP = ZPS[k]                ##  Update position for returning values        
            DF = abs (mZP - ZPS[k])     ##  Distance from the last edge
            
            D1 = abs(pZP - D1)
            D2 = abs(pZP - D2)
            D3 = abs(pZP - D3)
            
            
            Cal = 0
            if DZP > MinDistance:
                Cal +=1
            else:
                Cal -= 2
                
            if DZP < RealMin: 
                Cal -= 5
            
            if pD > MinDistance:
                Cal += 2
            
            if DF > MinDistance: 
                Cal += 1
            else:
                Cal -= 2   
            
            if D1 < Low or D2 < Low or D3 < Low:
                Cal -= 2
            else:
                Cal += 1
  
            if len(ZPSa) < k+1:
                ZPSa.append(Cal)
            else:
                ZPSa[k] += Cal  
            
        return pZP
            
          
                
    def checkApprobal(this, lista, objeto):
        if len(lista) > 0:
            maximum = max(lista)
            print("Max contest: " + str(maximum))
            
            for k in range(0,len(lista)):
                if lista[k] < maximum :
                    objeto[k] = -1
            
            print(objeto)
            print(lista)
            print("Lista: " + str(len(lista)) + "   Objeto: " + str(len(objeto)))

    def approbalStaple(this):
        ### This is executed after the first round and set the qualifications
        
        this.checkApprobal(this.YNSa,this.YNS)
        this.checkApprobal(this.YPSa,this.YPS)
        this.checkApprobal(this.ZNSa, this.ZNS)
        this.checkApprobal(this.ZPSa, this.ZPS)
        
            
        
    
    
    def setRelation(this, OtherHelix):
        ### Be careful, check 
        if this.YNSa == None:
            this.YNSa = []
        if this.YPSa == None:
            this.YPSa = []
        if this.ZNSa == None:
            this.ZNSa = []
        if this.ZPSa == None:
            this.ZPSa = []
        
        
        if this != OtherHelix :
            
            #print("Creating relationship")
            
            
            y = OtherHelix.getY()
            z = OtherHelix.getZ()
            
            if y-this.y == 1 and z == this.z :
                this.YP = OtherHelix
                #print("YPS")
                if this.YPS == None:
                    if this.YP.getYPS() == None:
                        this.YPS = []
                    else:
                        this.YPS = this.YP.getYPS()
                        this.YPSa = this.YP.getYPSa()
                    
                 
            if this.y - y == 1 and z == this.z:
                this.YN = OtherHelix
                #print("YNS")
                if this.YNS == None:
                    if this.YN.getYNS() == None:
                        this.YNS = []
                    else:
                        this.YNS = this.YN.getYNS()     
                        this.YNSa = this.YN.getYNSa()     
                                   
            
            
            if z - this.z == 1 and y == this.y:
                this.ZP = OtherHelix
                if this.ZPS == None:
                    if this.ZP.getZPS() == None:
                        this.ZPS = []
                    else:
                        this.ZPS = this.ZP.getZPS()
                        this.ZPSa = this.ZP.getZPSa()
                # ~ if len (this.ZPS) == 0:
                    # ~ this.ZPS = this.ZP.getZPS()
            
            if this.z - z == 1 and y == this.y:
                this.ZN = OtherHelix
                if this.ZNS == None:
                    if this.ZN.getZNS() == None:
                        this.ZNS = []
                    else:
                        this.ZNS = this.ZN.getZNS()  
                        this.ZNSa = this.ZN.getZNSa()  
                # ~ if len (this.ZNS) == 0:
                    # ~ this.ZNS = this.ZN.getZNS()
    
        
    
    
    def getY(this):
        return this.y
    
    def getZ(this):
        return this.z
    
    def getNumber(this):
        return this.currentRod
    
    def setRodN(this,n):
        this.currentRod = n
        this.isEmpty()
        #print("Rod: " + str(n) + " Pair: " + str(this.ispair) )
    
    def isEmpty(this):
        empty = True
        for BP in this.row:
            if type(BP) != type([]):
                empty = False
                BP.setR(this.currentRod)

        return empty
    
    def getRow(this):
        return this.row
    
    def setRow(this, nrow):
        this.row = nrow
    
    
    def config(this,y,z):
        p1 = y+z

        this.y = y
        this.z = z

        if p1/2 == round(p1/2):
            this.ispair = True
        else:
            this.ispair = False    

    def isPair(this):
        return this.ispair


