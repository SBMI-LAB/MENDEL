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
        
        # ~ print (this.YPS)
        # ~ print (this.YNS)
        
        
        # ~ print ( str(this.currentRod) + ") YPS: " +  str(len(this.YPS)) + ", YNS: "+ str(len(this.YNS))  +" out of : " + str(this.maxStaple) )
        # ~ print(this.YNS)
          
    
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
        
        for k in range (1,maxim):
            
            ### YNS
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
            if k < len(this.ZPS) :
                if k == 1:
                    pZP = this.ZPS[0]
                    mZP = this.ZPS[-1]
                
                pD = DZP
                DZP = abs(this.ZPS[k] - pZP)
                pZP = this.ZPS[k]
                DF = abs (mZP - this.ZPS[k])
                
                D1 = abs(pZN - pZP)
                D2 = abs(pZP - pZN)
                D3 = abs(pZP - pZP)
                
                
                Cal = 0
                if DZP > MinDistance:
                    Cal +=1
                if pD > 2*MinDistance:
                    Cal += 2
                
                if DF > MinDistance: 
                    Cal += 1
                else:
                    Cal -= 2   
                
                if D1 < Low or D2 < Low or D3 < Low:
                    Cal -= 2
                
                # ~ this.ZPSa.append(Cal)   
                if len(this.ZPSa) < k+1:
                    this.ZPSa.append(Cal)
                else:
                    this.ZPSa[k] += Cal             
        
        # ~ print ( "YPSA: " + str(len(this.YPSa)))
        # ~ this.analyzeStapleHelix(this.YN, this.YNS, this.YNSa)
        # ~ this.analyzeStapleHelix(this.YP, this.YPS, this.YPSa)
        # ~ this.analyzeStapleHelix(this.ZN, this.ZNS, this.ZNSa)
        # ~ this.analyzeStapleHelix(this.ZP, this.ZPS, this.ZPSa)        
        
    
    # ~ def analyzeStapleHelix(this, Helix, Lista, Approval):
        # ~ ### check each list and decide which elements are accepted or not
        # ~ dist = []
        
        # ~ if len(Lista) > 0:
            # ~ pK = Lista[0]
            # ~ for k in range (1, len(Lista)):
                # ~ d = abs(Lista[k] - pK)
                # ~ dist.append(d)
                
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
            
            print("Creating relationship")
            
            
            y = OtherHelix.getY()
            z = OtherHelix.getZ()
            
            if y-this.y == 1 and z == this.z :
                this.YP = OtherHelix
                print("YPS")
                if this.YPS == None:
                    if this.YP.getYPS() == None:
                        this.YPS = []
                    else:
                        this.YPS = this.YP.getYPS()
                        this.YPSa = this.YP.getYPSa()
                    
                 
            if this.y - y == 1 and z == this.z:
                this.YN = OtherHelix
                print("YNS")
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




class ExportCad():
    filename = "output.json"
    
    Last = None
    Initial = None
    
    ElementList = []
    
    Rods = []
    
    Helices = []
    
    maxPosition = 0

    tailLen = 20
    
    # The Rods are the list of elements organized in 3D
    # There should exist a list of lists so that they can be
    # Accesed, and indexed correctly
    # That's the reason they are accesed from the initial
    
    def setTailLen(this, n):
        this.tailLen = n



    def growStaples(this):

        for f in range (this.tailLen):
            
            for k in range (len(this.ElementList)):
                
                k1 = len(this.ElementList)-k-1

                BP = this.ElementList[k]
                P = BP.getPrevStp()
                N = BP.getNextStp()

                if N != None:
                    if N.getNextStp() == None:
                        if N.getPrev() != None:
                            if N.getPrev().getRod() == N.getRod() and N.getPrev().getPrevStp() == None and N.getPrev().getNextStp() == None :
                                N.setNextStp(N.getPrev())
                                N.getPrev().setPrevStp(N)
                
                    



                BP = this.ElementList[k1]
                P = BP.getPrevStp()
                N = BP.getNextStp()

                if P != None:
                    if P.getPrevStp() == None:
                        if P.getNext() != None:
                            if P.getNext().getRod() == P.getRod() and P.getNext().getNextStp() == None and P.getNext().getPrevStp() == None :
                                P.setPrevStp(P.getNext())
                                P.getNext().setNextStp(P)

            



    def eraseStaple(this, BP):
        ### This function should erase the staple (whole staple) assigned to the BP
        

        #print("Erasing staple")

        ## Delete forward
        Sig = BP.getNextStp()
        while Sig != None :
            P = Sig.getNextStp()
            Sig.setNextStp(None)
            Sig = P

        BP.setNextStp(None)

        ## Delete backward
        Sig = BP.getPrevStp()
        while Sig != None :
            P = Sig.getPrevStp()
            Sig.setPrevStp(None)
            Sig = P

        BP.setPrevStp(None)


        return None


    def cleanSmallStaple(this):
        ### This function should find staples whose size is certain smaller than an umbral
        ### Then, erase them

        print ("Checking small staples")

        umbral = 2
        

        for BP in this.ElementList:
            k = 0
            
            N = BP.getNextStp()
            
            T = 0
            while N != None :
                k = k+1
                N = N.getNextStp()
                
                T = T+1
                if T > len(this.ElementList):
                    N = None
                    print("Listas cerradas")

            N = BP.getPrevStp()
            T = 0
            while N != None :
                k = k+1
                N = N.getPrevStp()
                
                T = T+1
                if T > len(this.ElementList):
                    N = None
                    print("Listas cerradas")


            if k < umbral :
                this.eraseStaple(BP)




        return None

    def completeStrands(this):
        ### This function should search missing strands, and fill the structure
        return None

    def cleanStapleinTurn(this):
        ### This function should go through all the structure, and identify
        ### if one staple is created in the same location of a turn
        ### which is invalid. Then proceed to erase it

        print("Check if there is staple at turn")

        for BP in this.ElementList:

            ## Identify if has a turn
            N = BP.getNext()

            if N != None :
                if N.getRod() != BP.getRod() :
                    ## It's a turn!
                    NS = BP.getNextStp()
                    #PS = BP.getPrevStp()
                    if NS != None: 
                        if NS.getRod() != BP.getRod() :
                            ### It's a crossover!!!
                            this.eraseStaple(BP)




        return None



    def CreateStapleTail(this,B1, sense):
        ### Create a small tail

        

        TB1 = B1
        if sense:
            TP1 = B1.getNext()
            #TP1 = TP1.getNext()
        else:
            TP1 = B1.getPrev()
            #TP1 = TP1.getPrev()

        for k in range(1):

            if sense:

                if TB1.getPrevStp() == None and TP1.getNextStp() == None :
                    TB1.setPrevStp(TP1)
                    TP1.setNextStp(TB1)
                else:
                    break
            else:
                if TB1.getNextStp() == None and TP1.getPrevStp() == None:
                    TB1.setNextStp(TP1)
                    TP1.setPrevStp(TB1)
                else:
                    break

            TB1 = TP1

            if sense: 
                TP1 = TB1.getNext()
            else:
                TP1 = TB1.getPrev()


    ## Method compares B1 and B2, set the staple and tries to identify 
    ## the sense of the staple.
    ## 
    def SetStaple (this, B1, B2):
        ## Fist step: simply mark staple

        #B1.setNextStp (B1.getNext())
        #B1.getNext().setPrevStp(B1)

        #B2.setNextStp (B2.getNext())
        #B2.getNext().setPrevStp(B2)

        ### Obtain the order for staples

        R1 = B1.getOz()
        R2 = B2.getOz()

        P1 = B1
        P2 = B2
        
        x1 = P1.getXYZ()[0]
        x2 = P2.getXYZ()[0]
        
        print("Creating staple in X: "+ str(x1) + ", X2: " + str(x2))
        
        if P1.getNextStp() != None or P2.getNextStp() != None or P1.getPrevStp() != None or P2.getPrevStp() != None : 
            print ("Error, staple existed")
        else:
            if R1 != R2 :
                ### Run when they are different
                if R2 == 0 or R2 == 360:
                    ## Switch places
                    P1 = B1
                    P2 = B2
              
                #this.CreateStapleTail(P1, False)
                #this.CreateStapleTail(P2.getPrev(), False)

                P1.setPrevStp(P2)
                P2.setNextStp(P1)

                #this.CreateStapleTail(P1.getNext(), True)
                #this.CreateStapleTail(P2, True)

                P1.getNext().setNextStp( P2.getPrev() )
                P2.getPrev().setPrevStp(P1.getNext())

            #P1.setNextStp(P2)
            #P2.setPrevStp(P1)
            #B1.setPrevStp(B2)
            #B2.setNextStp(B1)


		
		

    ## Method AnalyzeStaples will look for staples possible location
    ## and mark them into the system
    def OldAnalyzeStaples(this):

        umbral = 0.9 ### Maximum distance allowed to determine if a crossover is possible

        for BP in this.ElementList:
            ## perform whole route through each BP
            for BP2 in this.ElementList:
                ### Second time 
                if  BP != BP2:
                    if BP.getNextStp() == None and BP.getPrevStp() == None and BP2.getNextStp() == None and BP2.getPrevStp()== None:
                        ### Compare if the coordinates match
                        P1 = BP.getPosStp()
                        P2 = BP2.getPosStp()
                        ## P1 and P2 are vectors
                        
                        D = (P1-P2).length
                        
                        #D = this.getDistance(P1,P2)

                        if D < umbral :
                            ## Set the crossover
                            ## It is required to know which is the orientation 
                            ## also, it is required to MAKE TWO at the same time
                            this.SetStaple(BP, BP2)
                            
        

        this.cleanStapleinTurn()
        this.growStaples()
        this.cleanSmallStaple()
        this.growStaples()
        
    
    def CleanStaple(this):
        ### Clean bad staples
        print ("Checking bad staples")
        for BP in this.ElementList:
            # Fix next stp
            NS = BP.getNextStp()         
            if NS != None:
                NSP = NS.getPrevStp()
                if NSP != BP:
                    print("Error in staple")
                    
            # Fix prev stp
            NS = BP.getPrevStp()         
            if NS != None:
                NSP = NS.getNextStp()
                if NSP != BP:
                    print("Error in staple")      
                    
                 
        print ("Something else to check")
        
        
        

    def DecideStaples(this, StapleLoc, StapleB1, StapleB2, StapleRod):
        ### Take decision of what to do with staples
        # First criteria: distance:
        
        
        
        if len(StapleRod) > 0:
            rods = max(StapleRod)   
            print("Relation: " + str(rods))
        
            ### All helices should have approved at least one.  Let's build the list:
            
            RodList = []
            
            for k in range(rods):
                Plist = []
                RodList.append(Plist)
            
            
            for k in range(0, len(StapleLoc)-1):
                k2 = StapleRod[k] -1
                
                Objeto = (StapleLoc[k],StapleB1[k], StapleB2[k])
                RodList[k2].append(Objeto)
       
            minDistance = 14
            approved = []
            
            
            
            for pList in RodList:
                pK = 0
                added = 0
                for k in range(1,len(pList)):
                    d = pList[k][0] - pList[pK][0] 
                    if d > minDistance:
                        approved.append(pList[k])
                        pK = k
                        added += 1
                        # ~ this.SetStaple(pList[k][1], pList[k][2])
                        
                    if k == len(pList)-1 and added == 0 and k > 1:
                        kn = k
                        kn = floor(k/2)
                        
                        ## Replace the last with current
                        # ~ approved.append(pList[kn])
                        
                        print("Added new : " + str(kn) + "  out of " + str(len(pList)))
                        print (d)
                        # ~ this.SetStaple(pList[kn][1], pList[kn][2])
                        # ~ print(pList)    
                    
                    
            
            for Objeto in approved:
                this.SetStaple(Objeto[1], Objeto[2])            
            
            
                        
            
            
        
            # ~ approved = []
            
            # ~ pK = 0
            
            # ~ for k in range(1, len(StapleLoc)):
                # ~ ### approving k and k-1
                # ~ ## preferible not approve the first and the last
                # ~ if StapleLoc[k] - StapleLoc[pK] > minDistance :
                    # ~ approved.append(k)
                    # ~ pK = k
                
            # ~ for k in approved:
                # ~ this.SetStaple(StapleB1[k], StapleB2[k])


    ### Method setLast will fill the list Element list
    ### With all basepairs that were created
    ### Reference is "The Last" and go backwards
    
    ## Method AnalyzeStaples will look for staples possible location
    ## and mark them into the system
    def AnalyzeStaples(this):

        umbral = 0.5 ### Maximum distance allowed to determine if a crossover is possible
        tlist =[]
        tempty = type(tlist)
        
        comp = 0
        tcomp = 0
        
        for K1 in range(0,len (this.Helices)) :
            
            
            Row1 = this.Helices[K1]
            Ry1 = Row1.getY()
            Rz1 = Row1.getZ()
            
            StapleLoc = []
            StapleRod = []
            StapleB1 = []
            StapleB2 = []
            
            Rod = 0
            
            
            # ~ print("What")
            
            for K2 in range(K1+1, len(this.Helices)) :
                Row2 = this.Helices[K2]
                Ry2 = Row2.getY()
                Rz2 = Row2.getZ()
                Dy = abs(Ry1-Ry2)
                Dz = abs(Rz1-Rz2)
                Dl = Dy*Dz
                DD = abs(Dy-Dz)
                
                
                
                if Row1.isEmpty() == False and Row2.isEmpty() == False:
                    if Dl == 0 and DD == 1: 
                        
                        Row1.setRelation(Row2)
                        Row2.setRelation(Row1)
                        
                        Rod += 1
                        
                        print("Comparing: (" + str(Ry1)  + "," + str(Rz1) +") with (" + str(Ry2)  + "," + str(Rz2) +")")
                        
                        ## Es una helice vecina
                        ###se hace analisis de vecindad
                        helix1 = Row1.getRow()
                        helix2 = Row2.getRow()
                        
                        if tcomp > comp:
                            comp = tcomp
                        tcomp = 0
                        
                        for x in range (0,len(helix1)-1):
                            
                            BP = helix1[x]
                            BP2 = helix2[x]

                            
                            if  BP != BP2 and type(BP) != tempty and type(BP2) != tempty:
                                if BP.getNextStp() == None and BP.getPrevStp() == None and BP2.getNextStp() == None and BP2.getPrevStp()== None:
                                    ### Compare if the coordinates match
                                    
                                    P1 = BP.getPosStp()
                                    P2 = BP2.getPosStp()
                                    ## P1 and P2 are vectors
                                    
                                    tcomp = tcomp + 1
                                    
                                    D = (P1-P2).length
                                    
                                    #D = this.getDistance(P1,P2)

                                    if D < umbral:
                                        
                                        ## Set the crossover
                                        ## It is required to know which is the orientation 
                                        ## also, it is required to MAKE TWO at the same time
                                        #this.SetStaple(BP, BP2)
                                        # ~ StapleLoc.append(x)
                                        # ~ StapleB1.append(BP)
                                        # ~ StapleB2.append(BP2)
                                        # ~ StapleRod.append(Rod)
                                        Row1.setStaple(x,Row2)
            
            # ~ print ("Next")
            # ~ this.DecideStaples(StapleLoc,StapleB1, StapleB2, StapleRod)                            
  
                        
        
        for Row in this.Helices :
            if Row.isEmpty() == False:
                Row.analyzeStaple()
        
        tt = 0
        
        for Row in this.Helices :
            if Row.isEmpty() == False:
                Row.approbalStaple()
                Lista = Row.getStapleListBP()
                tt = tt+1
                if tt < 5:
                    for P in Lista:
                        this.SetStaple(P[0], P[1])
                
        
        
        print ("comparaciones: " + str(comp))
        # ~ this.CleanStaple()
        this.cleanStapleinTurn()
        this.growStaples()
        # ~ this.cleanSmallStaple()
        # ~ this.growStaples()
        
                    




    ### Method setLast will fill the list Element list
    ### With all basepairs that were created
    ### Reference is "The Last" and go backwards    

    def setLast(this, theLast):
        
        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
        
        this.Last = theLast
        current = theLast
        k = 0
        while (current != None) :
            Initial = current
            pX = current.getXYZCenter()
            if this.maxPosition < pX[0]:
                this.maxPosition = round(pX[0])
            
            current = current.getPrev()
            
            
            k = k+1
        
        print("Total of " + str(k) + " elements")
        
        
        this.maxPosition = math.ceil(this.maxPosition/32)*32
        
        print("Max positions X: " + str(this.maxPosition))
        
        current = Initial
        
        while (current != None) :
            this.ElementList.append(current)   
            current = current.getNext()
        
    
    
    def buildRods(this):
        print("Building rods")
        for BP in this.ElementList:
            this.addBP(BP)
            
        ### asign rod numbers
        rod = 0
        pos = 0
        k = 0
        
        print("Rod status:")
        
        for sheet in this.Rods:
            print("Sheet["+str(k)+"]:"+str(len(sheet))+" rows") 
            k+=1
            for rows in sheet:
                pos = 0
                hel = HelixRod()
                this.Helices.append(hel)
                hel.setRow(rows)
                for BP in rows:
                    if type(BP) != type([]):
                        BP.setRod(rod,pos)
                        V = BP.getXYZCenter()
                        x,y,z=round(V[0]),round(V[1]/2),round(V[2]/2)
                        y = -y
                        hel.config(y,z)
                        
                    pos += 1
                rod += 1    
        
        
        pairs = 0
        impairs = 0
        
          
        for rows in this.Helices:
            #this.rowEmpty(rows.getRow())
            if (rows.isEmpty()==False):
                if rows.isPair():
                    rows.setRodN(pairs*2)
                    pairs += 1
                else:
                    rows.setRodN(impairs*2+1)
                    impairs += 1
                
                #print("Row: " + str(rows.getNumber()) + " Pair: " + str(rows.isPair()) + " y: " + str(rows.getY()) + " z: " + str(rows.getZ()) )
        
        for rows in this.Helices:
            rows.isEmpty()

        this.AnalyzeStaples()
        # ~ this.OldAnalyzeStaples()
        
    
    def addBP(this, BP):
        #print("Adding BP")
        V = BP.getXYZCenter()
        x,y,z=round(V[0]),round(V[1]/2),round(V[2]/2)
        y = -y
        # so far, only x,y,z can be positive
        if x<0 or y<0 or z<0 :
            print("Error, lower than zero")
        else:
            ## Search for the current position
            # x position is for elements in rods
            # z position is for the current sheet
            # y position is for the current row
            
            
            # first element should be z
            
            #print("Adding: " + str(z) + " | " + str(len(this.Rods)))
            
            if z >= len (this.Rods):
                #print ("Need add")
                for k in range(len(this.Rods),z+1):
                    #print ("Adding")
                    this.Rods.append([])
            
            #print("passed comparison")
            sheet = this.Rods[z]
            
            # next element, the row, that is y
            
            
            
            if y >= len (sheet):
                for k in range(len(sheet),y+1):
                    sheet.append([])   
                    #hel = HelixRod()
                    #hel.config(y,z)
                    #this.Helices.append(hel)  
                           

            row = sheet[y]
            
            
            
            # final element, the bp itself, is x
            
            if  len (row) < this.maxPosition:
                for k in range(len(row),this.maxPosition):
                    row.append([])

            
            # here add the BP
            row[x]=BP
            
            #this.Helices[y].setRow(row)
            
        
    
    
    def writeFile(this, name):
        filename=name
        print("Writing file: " + filename)
        
        filepath = bpy.path.abspath("//"+filename)
        
        Archivo = open(filepath, "w")
        
        firstVal = False

        x,y,z = 0,0,0
        
        Archivo.write('{"name":"'+filename+'","vstrands":[')
        
        cc = 0
        
        tlist =[]
        tempty = type(tlist)
        
        for helix in this.Helices:
            y = helix.getY()
            z = helix.getZ()
            #if z != 0:
            #        Archivo.write(',')
            
#            for row in helix.getRow():
            if True:
                row = helix.getRow()
                x=0
                
                if helix.isEmpty() == False:
                
                    #if y != 0:
                    #    Archivo.write(',')
                    if firstVal == True:
                        Archivo.write(',')
                    else:
                        firstVal = True
                    
                    Archivo.write('\n{')
                    Archivo.write('"num":'+str(helix.getNumber()))  
                    Archivo.write(',"stap_colors":[], "stapLoop":[]')
                    scafs = '"scaf":['  
                    staps = '"stap":['    
                    loops = '"loop":['
                    skips = '"skip":['
                            
                    for BP in row:

                        if x != 0:
                                scafs += ','
                                staps += ','
                                loops += ','
                                skips += ','
                                
                        if type(BP)==tempty :
                            scafs += '[-1,-1,-1,-1]'
                            staps += '[-1,-1,-1,-1]'
                        else:
                            
                            ## Scaffold analysis    

                            Prev = BP.getPrev()
                            Next = BP.getNext()
                            
                            scafs += '['
                            
                            if Prev == None:
                                scafs+= '-1,-1'
                            else:
                                scafs+= str(Prev.getRod())
                                scafs+=','
                                scafs+= str(Prev.getPos())
                            
                            scafs += ','
                            
                            if Next == None:
                                scafs+= '-1,-1'
                            else:
                                scafs+= str(Next.getRod())
                                scafs+= ','
                                scafs+= str(Next.getPos())
                                
                            scafs += ']'
                            ## End of Scaffold analysis
                            
                            ## Staple analysis    

                            Prev = BP.getPrevStp()
                            Next = BP.getNextStp()
                            
                            staps += '['
                            
                            if Prev == None:
                                staps+= '-1,-1'
                            else:
                                staps+= str(Prev.getRod())
                                staps+=','
                                staps+= str(Prev.getPos())
                            
                            staps += ','
                            
                            if Next == None:
                                staps+= '-1,-1'
                            else:
                                staps+= str(Next.getRod())
                                staps+= ','
                                staps+= str(Next.getPos())
                                
                            staps += ']'
                            ## End of staple analysis
   
                            
                        #staps += '[-1,-1,-1,-1]'




                        loops += '0'
                        skips += '0'
                        #end BP
                        x=x+1
                    
                    loops +=']'    
                    skips +=']' 
                    staps+=']'
                    scafs+=']'
                    nk = 10+y
                    Archivo.write(',"col": '+str(z+6)+','+ skips + ','+ staps + ',' + loops+ ',' +  scafs + ' ,"row":'+str(nk))
                    Archivo.write('}')
                    
                y=y+1
                cc = cc+1
                #end row
            z=z+1
            #end sheet
                    
                    

        Archivo.write(']}')
        
        Archivo.close()
        
        
    def rowEmpty(this, row):
        empty = True
        for BP in row:
            if type(BP) != type([]):
                empty = False
                
        #if empty == True:
        #    print("Fila vacia")
            
        return empty
                    
