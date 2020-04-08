import bpy
from math import radians
import math


class Staple():

    MinStaple = 1
    IdealStaple = 14
    
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

    Strand1 = None
    Strand2 = None
    
    Recursive1 = False
    Recursive2 = False
    
    
    Conflicts = None

    Enabled = False

    Ignored = False

    Merged = False

    Visited = False

    Lined = False

    Parallel = False
    
    def getCrossing(this):
        Retorno = -1
        if this.Lined == False:
            if len(this.FirstStrand) > 0 and len(this.SecondStrand) >  0 :
                Retorno = this.Crossing
        
        return Retorno

    def getMinLength(this):
        minLength = -1

        if this.isEnabled():
            # this.First_1 = this.FirstStrand[0]
            # this.Last_1 = this.FirstStrand[-1]
            # this.First_2 = this.SecondStrand[0]
            # this.Last_2 = this.SecondStrand[-1]
            # if len(this.FirstStrand) > 0:
            #     this.First_1 = this.FirstStrand[0]
            #     this.Last_1 = this.FirstStrand[-1]

            # if len(this.SecondStrand) > 0:
            #     this.First_2 = this.SecondStrand[0]
            #     this.Last_2 = this.SecondStrand[-1]

            try:
                
                this.First_1 = this.FirstStrand[0]
                this.Last_1 = this.FirstStrand[-1]
                this.First_2 = this.SecondStrand[0]
                this.Last_2 = this.SecondStrand[-1]

                D1 = this.LengthFirst_1 = abs( this.First_1.getX() - this.Crossing  )
                D2 = this.LengthFirst_2 = abs( this.First_2.getX() - this.Crossing  )
                D3 = this.LengthLast_1 = abs( this.Last_1.getX() - this.Crossing  )
                D4 = this.LengthLast_1 = abs( this.Last_2.getX() - this.Crossing  )


                #PT = (this.First_1.getX(), this.First_2.getX(), this.Last_1.getX(), this.Last_2.getX() )
                P = ( D1, D2, D3, D4 )
                #print(this.Crossing)
                #print(PT)
                #print(P)
                
                minLength = min ( P )
            except:
                print("No enabled")

        return minLength


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

    
    def setStaple (this, cross, row1, row2, Parallel) : 
        this.Crossing = cross
        
        Exito = True

        this.Strand1 = Strand()
        this.Strand2 = Strand()

        this.Strand1.setStrand(this.FirstStrand, this)
        this.Strand2.setStrand(this.SecondStrand,this)  
        
        ### First and last is defined in terms of the orientation
        ### This gives a more control about the geometry
        
        this.Crossing = cross

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

    def setStapleParallel (this, cross, row1, row2, Parallel) : 
        this.Crossing = cross

        this.Parallel = Parallel

        this.Strand1 = Strand()
        this.Strand2 = Strand()

        this.Strand1.setStrand(this.FirstStrand, this)
        this.Strand2.setStrand(this.SecondStrand,this)        
        
        Exito = True
        
        ### First and last is defined in terms of the orientation
        ### This gives a more control about the geometry

        #### Only one cross is assigned. The other will be just parallel
        ####
        """

        -----*-----
             \
        -----*-----

        """
        
        this.Crossing = cross

        bp_11 = row1[cross]
        bp_12 = row1[cross+1]
        
        bp_21 = row2[cross]
        bp_22 = row2[cross+1]
        
        caso = False
        
        if bp_11.getOz() == 0 or bp_11.getOz() == 360:
            caso = not caso
        
        if caso:
            this.First_1 = bp_22
            this.Last_1  = bp_11
            
            this.First_2 = bp_12
            this.Last_2  = bp_21
        else:
            this.First_1 = bp_22
            this.Last_1  = bp_11
            
            this.First_2 = bp_12
            this.Last_2  = bp_21                                 
        

        this.First_1 = bp_22
        this.Last_1  = bp_11
        
        this.First_2 = bp_22
        this.Last_2  = bp_22

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
                
                #this.SecondStrand.append(this.First_2)
                #this.SecondStrand.append(this.Last_2)
                
                bp_11.setStaple(this)
                bp_21.setStaple(this)
                
                #bp_12.setStaple(this)
                #bp_22.setStaple(this)
            
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
    
    
    def growEnd(this):
        if this.Strand1 != None:
            this.Strand1.growEnd()
        if this.Strand2 != None:
            this.Strand2.growEnd()


    def growStapleStep(this):
        if this.Parallel == True:
            #this.growStapleStep_2()
            print("Nada")
        else:
            if this.Strand1 != None:
                this.Strand1.growStep()
                if len(this.FirstStrand) > 0:
                    this.First_1 = this.FirstStrand[0]
                    this.Last_1 = this.FirstStrand[-1]

            if this.Strand2 != None:
                this.Strand2.growStep()
                if len(this.SecondStrand) > 0:
                    this.First_2 = this.SecondStrand[0]
                    this.Last_2 = this.SecondStrand[-1]

            

    def growStapleStepN(this):
        if this.Parallel == True:
            this.growStapleStep_2()
        else:
            this.growStapleStep_1()


    def growStapleStep_1(this):
 
        
        ### Attempts to grow the staple. If it touches another
        ### It will mark the other as neighbor
        ## The neighbor staples can be used to decide merge or not
        
        ###  Remember HERE scaffold have opposite directions to staples
        if len(this.FirstStrand) > 0 and len(this.SecondStrand) > 0 :
            this.getMinLength()
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


    def growStapleStep_2(this):
 
        
        ### Attempts to grow the staple. If it touches another
        ### It will mark the other as neighbor
        ## The neighbor staples can be used to decide merge or not
        
        ###  Remember HERE scaffold have opposite directions to staples
       
            #this.getMinLength()
        if this.Enabled :

            if len(this.FirstStrand) > 0 and this.Parallel == True:

                this.First_1 = this.FirstStrand[0]
                this.Last_1 = this.FirstStrand[-1]

                P1 = this.growStrand (this.FirstStrand, this.First_1, this.Last_1, this.TouchingFirst_1, this.TouchingLast_1)
                this.First_1 = P1[0]
                this.Last_1 = P1[1]
                this.TouchingFirst_1 = P1[2]
                this.TouchingLast_1 = P1[3]  

            if len(this.SecondStrand) > 0 and this.Parallel == False:
                
                this.First_1 = this.SecondStrand[0]
                this.Last_1 = this.SecondStrand[-1]

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
                    if stp1 != None:
                        stp1.extTouch(this, bp1)
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
                    if stp2 != None: 
                        stp2.extTouch(this, bp2)
                else:
                    #print("Recursive 2")
                    this.Recursive2 = True
        
        P = (First, Last, TouchingFirst, TouchingLast)
        return P
    
    
    def extTouch(this, Touching, BP):
        if BP != None:
            if len(this.FirstStrand) > 0:
                if BP == this.getFirst1() :
                    this.TouchingFirst_1 = Touching
                if BP == this.getLast1() :
                    this.TouchingLast_1 = Touching 

            if len(this.SecondStrand) > 0:
                if BP == this.getFirst2() :
                    this.TouchingFirst_2 = Touching

                if BP == this.getLast2() :
                    this.TouchingLast_2 = Touching 


    def getFirst1(this):
        #print(this.FirstStrand[0].getX())
        
        return this.FirstStrand[0]
    
    def getFirst2(this):
        #return this.First_2
        #print(this.SecondStrand[0].getX())
        return this.SecondStrand[0]
    
    def getLast1(this):
        #return this.Last_1
        #print(this.FirstStrand[-1].getX())
        return this.FirstStrand[-1]
    
    def getLast2(this):
        #return this.Last_2
        #print(this.SecondStrand[-1].getX())
        return this.SecondStrand[-1]
    
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
        if this.isEnabled():
            this.getMinLength()
            if len(this.FirstStrand) > 1 :
                this.applyStrand(this.First_1, this.Last_1, this.FirstStrand)
            if len(this.SecondStrand) > 1:
                this.applyStrand(this.First_2, this.Last_2, this.SecondStrand)
        #print("Applying")
        
    
    def applyStrand(this, First, Last, Elements):    
        ## Set begining:

        if this.Enabled:

            First.setPrevStp(None)
            
            Previo = First
            
            for BP in Elements:
                if BP != Previo and BP != None:
                    #if BP.getStaple() == this:
                    Previo.setNextStp(BP)
                    BP.setPrevStp(Previo)
                    Previo = BP
            
            ## Set ending:
            Last.setNextStp(None)
        
        
        
        
    def getLengthFirst(this):
        return this.LengthFirst
        
    def getLengthLast(this):
        return this.LengthLast
    

    def tryFuseStaple(this, Minstp):
        this.MinStaple = Minstp
        MinD =  this.getMinLength()

        print("Fusion ? " + str(MinD))

        if MinD < this.MinStaple:
            this.Strand1.tryFuse()
            this.Strand2.tryFuse() 

            for k in range(10):
                this.Strand1.growStep()
                this.Strand2.growStep()


    def tryFuseStapleN(this, Minstp):
        ### Here, it will attempt to dissolve a staple
        ### And probably merge it with another when it 
        ### is too short

        
        this.MinStaple = Minstp
        
        MinD =  this.getMinLength()
        
        if MinD < this.MinStaple:
            print("Staple must be fused: " + str(MinD))

            ### How to fuse them???
            ### First strand should grow from beggining and then
            ### after the cross section, it will be added to the second 
            ### strand. And viceversa.

            ### The crossing will be removed of course

            ### Also, vector can be reseted, grow again from the
            ### Start1 and finish in the Last2

            ## Let's do this:



            if this.First_1 != None and this.First_2 != None and this.Last_1 != None and this.Last_2 != None and len(this.FirstStrand) > 0 and len(this.SecondStrand) > 0:
                
                #this.First_1 = this.FirstStrand[0]
                #this.First_2 = this.SecondStrand[0]
                
                #this.Last_1 = this.FirstStrand[-1]
                #this.Last_2 = this.SecondStrand[-1]

                ## Itera first strand
                BeginBP = this.First_1
                EndBP = this.Last_2

                this.FirstStrand.clear()
                this.FirstStrand.append(BeginBP)
                Siguiente = BeginBP.getPrev()
                
                while Siguiente != EndBP:
                    this.FirstStrand.append(Siguiente)
                    Siguiente = Siguiente.getPrev()

                this.FirstStrand.append(EndBP)

                print("Fusion : " + str(BeginBP.getRod()) + " , " + str(BeginBP.getX()))
                indices = []
                for BP in this.FirstStrand:
                    indices.append(BP.getX())
                print(indices)
                
                ## Itera second strand
                
                BeginBP = this.First_2
                EndBP = this.Last_1

                this.SecondStrand.clear()

                this.SecondStrand.append(BeginBP)

                Siguiente = BeginBP.getPrev()

                
                while Siguiente != EndBP:
                    this.SecondStrand.append(Siguiente)
                    Siguiente = Siguiente.getPrev()
                
                this.SecondStrand.append(EndBP)

                print("Fusion : " + str(BeginBP.getRod()) + " , " + str(BeginBP.getX()))
                indices = []
                for BP in this.FirstStrand:
                    indices.append(BP.getX())
                print(indices)

                ## Switch places

                #BPT = this.Last_1
                #this.Last_1 = this.Last_2
                #this.Last_2 = BP

                #this.Last_1 = this.FirstStrand[-1]
                #this.Last_2 = this.SecondStrand[-1]

                ### Here comes one really important step:
                ### Fuse with next staple and remove current.
                ## is it possible?

                ## Try fuse only First


    def getTouchingVector(this,BP):
        """
        This new definition will take another approach.
        It will check directly the neighbor of BP (Next and Prev)
        if it belongs to another staple or not.
        """

        P = None
        Strand  = None

        P1 = BP.getNext()
        P2 = BP.getPrev()

        if P1 != None :
            if P1.getStaple() != BP.getStaple():
                P = P1
        
        if P2 != None :
            if P2.getStaple() != BP.getStaple():
                P = P2

        if P != None :
            stp = P.getStaple()
            if stp != None: 
                FS = stp.getFirstStrand()
                SS = stp.getSecondStrand()
                ## There are only 2 options, first or second strand
                if FS[0] == P or FS[-1] == P :
                    Strand = FS
                
                if SS[0] == P or SS[-1] == P :
                    Strand = SS

        return Strand




    def getTouchingVector2 (this, BP):
        ### Try to obtain the touching vector for BP
        Touching = None
        try :
            if BP != None :

                print ("BP: " + str(BP.getX()))

                BPN = BP.getNext()
                
                if BPN != None : 
                    if this.TouchingFirst_1 != None:
                        if this.TouchingFirst_1.getLast1() == BPN:
                            Touching = this.TouchingFirst_1.getFirstStrand()
                            print("C1")
                        if this.TouchingFirst_1.getLast2() == BPN:
                            Touching = this.TouchingFirst_1.getSecondStrand()
                            print("C2")

                    if this.TouchingFirst_2 != None:
                        if this.TouchingFirst_2.getLast1() == BPN:
                            Touching = this.TouchingFirst_2.getFirstStrand()
                            print("C3")

                        if this.TouchingFirst_2.getLast2() == BPN:
                            Touching = this.TouchingFirst_2.getSecondStrand()
                            print("C4")

                

                BPN = BP.getPrev()
                if BPN != None: 
                    if this.TouchingLast_1 != None:
                        if this.TouchingLast_1.getFirst1() == BPN:
                            Touching = this.TouchingLast_1.getFirstStrand()
                            print("C5")
                        if this.TouchingLast_1.getFirst2() == BPN:
                            Touching = this.TouchingLast_1.getSecondStrand()
                            print("C6")

                    if this.TouchingLast_2 != None:
                        if this.TouchingLast_2.getFirst1() == BPN:
                            Touching = this.TouchingLast_2.getFirstStrand()
                            print("C7")
                        if this.TouchingLast_2.getFirst2() == BPN:
                            Touching = this.TouchingLast_2.getSecondStrand()
                            print("C8")

                

        except:
            None
        
        return Touching



    def tryMergeStaples(this):
        if this.Merged == False:
            this.mergeByTouchHead(this.TouchingFirst_1)
            #this.mergeByTouchHead(this.TouchingFirst_2)
    
    def fuseVectorsAppend2(this, initial, final ):
        Stp = initial[-1].getStaple()

        BP1 = initial[-1]
        BP2 = final[0]

        k = 0

        n = len(initial)

        for BP in final:
            if k == 0:
                initial.insert(n-1,BP)
                BP.setStaple(Stp)
            k = k+1
        indices = []

        for BP in initial:
            indices.append( BP.getX() )
        
        print (indices)

        ### Check the end of the strand:
        BP1 = initial[0].getNext()
        BP2 = initial[-1].getPrev()
        print("Append: " +  str(type(BP1)) + " , " + str(type(BP2)))

    def fuseVectorsAppend(this, initial,final):
        this.fuseVectorsInitial(final, initial)


    def fuseVectorsInitial(this, initial, final ):
        
        k = 0
        Stp = initial[0].getStaple()

        for BP in final:
            initial.insert(k,BP)
            BP.setStaple(Stp)
            k += 1

        indices = []
        for BP in initial:
            indices.append( BP.getX()  )
        
        print("Initial")
        print (indices)
        

    def tryMergeSingleLines(this):
        ### Try to merge
        Exito = False

        if True:
        #if this.Visited == False:
            #Exito = True
            if Exito == False:
                BP1 = this.FirstStrand[0]
                BP2 = this.FirstStrand[-1]

                if BP1.getRod() == BP2.getRod():
                    print(str(this.Rod1.getNumber())+ ") Single lines AB: " + str(BP1.getRod()) + " , " + str(BP1.getX()) + " - " + str(BP2.getX()))
                    Rows = this.getTouchingVector(BP1)
                    if Rows != None :
                        if Rows[-1].getRod() == BP1.getRod() :
                            print("Preparing to fuse vectors A")
                            this.fuseVectorsAppend2(Rows, this.FirstStrand)
                            #this.FirstStrand.clear()
                            Rows.clear()
                            Exito = True
                    
                    if Exito == False:
                        Rows = this.getTouchingVector(BP2)
                        if Rows != None :
                            if Rows[0].getRod() == BP2.getRod() :
                                print("Preparing to fuse vectors B")
                                if Rows == this.FirstStrand:
                                    print("Es el mismo vector")
                                this.fuseVectorsInitial(Rows, this.FirstStrand)
                                this.FirstStrand.clear()
                                Exito = True
            
            Exito = False ## Forced to check second strand
            if Exito == False:
                BP1 = this.SecondStrand[0]
                BP2 = this.SecondStrand[-1]

                if BP1.getRod() == BP2.getRod():
                    print(str(this.Rod1.getNumber())+ ") Single lines CD: " + str(BP1.getRod()) + " , " + str(BP1.getX()) + " - " + str(BP2.getX()))
                    Rows = this.getTouchingVector(BP1)
                    if Rows != None :
                        if Rows[-1].getRod() == BP1.getRod() :
                            print("Preparing to fuse vectors C")
                            
                            this.fuseVectorsAppend(Rows, this.SecondStrand)
                            #this.SecondStrand.clear()
                            #this.fuseVectorsInitial(Rows,this.SecondStrand)
                            Rows.clear()
                            #this.SecondStrand.clear()

                            Exito = True
                    
                    #Exito = True

                    if Exito == False:
                        Rows = this.getTouchingVector(BP2)
                        if Rows != None :
                            if Rows[0].getRod() == BP2.getRod() :
                                print("Preparing to fuse vectors D")
                                if Rows == this.SecondStrand:
                                    print("Es el mismo vector")
                                this.fuseVectorsInitial(Rows, this.SecondStrand)
                                this.SecondStrand.clear()
                                Exito = True

        this.Visited = True
     



    def mergeFirstStrandTail(this, Strand):
        
        BP1 = Strand[0]

        if BP1.getRod() == this.Last_1.getRod() :

            print("Merging strand")
            for BP in Strand:
                this.FirstStrand.append(BP)
            if Strand[-1] != None:
                this.Last_1 = Strand[-1]
            this.Merged = True


    def mergeSecondStrandTail(this, Strand):
        
        print("Merging strand")
        for BP in Strand:
            this.SecondStrand.append(BP)
        if Strand[-1] != None:
            this.Last_2 = Strand[-1]
        this.Merged = True        


    def isMerged(this):
        return this.Merged




    def mergeByTouchHead(this, Touch):
        ### This method will attempt to merge the strands to 
        ### the strands of the touching object.
        ### This will attempt one of the TouchFirsts, and the
        ### corresponding strand to the other vector.
        Exito = False

        if Touch != None :
            if Touch.isMerged() == False:
                # Touch is another staple. Let's check where it is touching
                BP1 = Touch.getLast1()
                ## Prev should be the touching
                N = BP1.getPrev()
                FusingStrand = None
                if N == this.First_1 : ### Fuse first strand
                    FusingStrand = this.FirstStrand
                
                if N == this.First_2:
                    FusingStrand = this.SecondStrand

                if FusingStrand != None :
                    Touch.mergeFirstStrandTail(FusingStrand)
                    FusingStrand.clear()
                    this.Merged = True
                    Exito = True

                if Exito == False:
                    ## Repeat with the other
                    BP1 = Touch.getLast2()
                    ## Prev should be the touching
                    N = BP1.getPrev()
                    FusingStrand = None
                    if N == this.First_1 : ### Fuse first strand
                        FusingStrand = this.FirstStrand
                    
                    if N == this.First_2:
                        FusingStrand = this.SecondStrand

                    if FusingStrand != None :
                        Touch.mergeSecondStrandTail(FusingStrand)
                        FusingStrand.clear()
                        this.Merged = True                    
            
            







        
        
    
