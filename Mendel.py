Blender = False
try:
    import bpy
    Blender = True
except:
    None
    

if Blender:
    from mathutils import Vector

import time
from time import sleep

if Blender:
    def print(data):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'CONSOLE':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT") 
                

if Blender:
    ## Imports as Blender
    
    filepath = bpy.path.abspath("//scaff.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
    
    #filepath = bpy.path.abspath("//ExportCad.py")
    #exec(compile(open(filepath).read(), filepath, 'exec'))
    
    filepath = bpy.path.abspath("//HelixCad.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
    
    filepath = bpy.path.abspath("//HelixRod.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
    
    filepath = bpy.path.abspath("//Staple.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
    
    filepath = bpy.path.abspath("//Strand.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
    
    filepath = bpy.path.abspath("//Render.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
    
    filepath = bpy.path.abspath("//SubRod.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))

    try:
        filepath = bpy.path.abspath("//asymptote.py")
        exec(compile(open(filepath).read(), filepath, 'exec'))
    except:
        print("Module asymptote cannot be initialized")
        
else:
    ## Imports as Python
    from scaff import *
    from HelixCad import *



class Mendel():
    
    t = time.time()
    
    Lattice="Square"
    
    CurrentSense = 0
    prevAngle = 270
    
    mode = "Wire"
    
    #direction = Vector((1,0,0))
    
    LimitBP = 8000
    
    OverLimit = False
    
    prevBP = None
    
    CurrentRow = None
    pAng = 720/21
    #pAng = 34.28
    
    firstTime = False
    
    c_id = 0
    
    initial = 0
    
    currentAngle = 0
    
    xAngle = 0

    HelCad = None

    Analyzed = False

    Draft = False

    Elements = None

    Parallel = False

    minX = 0
    minY = 0
    minZ = 0
    
    maxX = 0
    maxY = 0
    maxZ = 0
    
    growAxes = "Y"
    growSign = True
    
    backwards = False
    
    bp2end = 0
    
    HCSet = 0 ## Honeycomb set to switch
    
    
    def DistanceAng(this, A, B):
        
        ### Calculates the distance in angles 
        ### Between A and B
        A = this.AdjustAngle(A)
        B = this.AdjustAngle(B)
        
        D = this.AdjustAngle(A-B)
        if D > 180:
            D = this.AdjustAngle(B-A)
        return D
    
    def AdjustAngle(this, number):
        
        Valid = True
        
        if number > 360:
            number = number - 360
            Valid = False
        if number < 0:
            number = number + 360
            Valid = False
            
        if Valid == False:
            return this.AdjustAngle(number)
        else:
            ### Adjust precision
            if abs(floor(number)-number) < 0.001:
                number = floor(number)
            elif abs(ceil(number)-number) < 0.001:
                number = ceil(number)
            
            return number
    
    
    
    def BpTurn(this, number ):
        this.pAng = 360/number
    
    def setCadnanoBpTurn(this):
        this.BpTurn(10.67)
    
    def SetHoneyComb(this):
        this.Lattice = "HoneyComb"
    
    def BP2End(this, bp):
        this.bp2end = bp
    
    def Stats(this):
        elapsed = time.time() - this.t
        print("======================")
        print("MENDEL")
        print("Created by Jorge Guerrero")
        print("North Carolina A&T State University")
        print("V. 22.10.25") ## Year, Month, Day
        
        print("")
        print("Total base pairs: " + str(len(this.Elements)))
        print(f'Generation time: {elapsed:.3f} seconds')
        
        
        dimX = abs (this.maxX - this.minX) + 1
        dimY = abs (this.maxY - this.minY)/2 + 1 
        dimZ = abs (this.maxZ - this.minZ)/2 + 1
        
        dimX = round( dimX * 0.34 )
        dimY = round( dimY * 3 )
        dimZ = round( dimZ * 3 )
        
        print("Expected dimensions:")
        print("x,y,z: " + str(dimX) + ", " + str(dimY) + ", " + str(dimZ ) + " [ nm ]")
        
        
        #print("Previous: ")
        #print(this.prevSize)
        #print("After: ")
        #print(this.finalSize)
        
        ## Count scaffolds
        cuenta = 1
        Previo = None
        for BP in this.Elements:
            if Previo != None:
                if Previo.getNext() != BP or BP.getPrev() != Previo:
                    cuenta = cuenta + 1
                Previo = BP
        print(f"Total: {cuenta} scaffolds")
        
        if this.OverLimit:
           print(f"Structure reached the maximum size: {this.LimitBP} BP ")
           print("--To force it, modify the parameter LimitBP--")
        
        
    def CheckMax(this):
        
        if this.Elements == None:
            return True
        
        if this.LimitBP > len(this.Elements):
            return True
        else:
            this.OverLimit = True
            return False
        
    
    
    def Growth(this, sense = "Y+"):
        ### Define the orientation of growth for DNA
        ## Y+: Grow along Y axes, positive X
        ## Y-: Grow along Y axes, negative X
        ## Z+: Grow along Z axes, positive X
        ## Z-: Grown along Z axes, negative X
        if sense == "Y+":
            this.growAxes = "Y"
            this.growSign = True
            
        if sense == "Y-":
            this.growAxes = "Y"
            this.growSign = False
            
        if sense == "Z+":
            this.growAxes = "Z"
            this.growSign = True
        
        if sense == "Z-":
            this.growAxes = "Z"
            this.growSign = False
            
    
    def GetNumber(this):
        return len(this.Elements)
    
    def Split(this):
        if this.prevBP != None:
            prev1 = this.prevBP.getPrev()
            this.prevBP.SetPrev(None)
            if prev1 != None:
                prev1.SetNext(None)

    def setDraft(this):
        this.Draft = True

    def Add(this, n):
        this.AddMore(n)
    
    def UpZ(this):
        this.AddTurn_Z_up()
    
    def UpY(this):
        this.AddTurn_Y_up()

    def DownZ(this):
        this.AddTurn_Z_down()
    
    def DownY(this):
        this.AddTurn_Y_down()
    
    
    def configure(this):
        names = False
        p = 0
        t = 0
        digit_count= len(str(len(bpy.context.scene.objects)))
        for k in bpy.context.scene.objects:
            k.parent = None
            k.rotation_euler=(0,0,0)
            k.location=(0,0,0)
            
            if names == True:
                if p == 0:
                    Prefix = "_BP"
                elif p==1:
                    Prefix = "_Scal"
                else:
                    Prefix = "_Stap"            
                
                k.name = "%0*i%s" % ( digit_count, t, Prefix)
                
                p = p+1
                
                if p==3:
                    p=0
                    t = t+1
            
            
            
    
    def setMode(this, nmode):
        this.mode = nmode
    
    
    def setDirection(this,x,y,z):
        this.direction = Vector((x,y,z))
        #this.direction.normalize()


    def StartAt(this, n):
        #this.initial = n
        this.AddAt(n,0,0)
        #this.AddBP()
    
    ang_offset=0
    
    def AddAt(this,x,y,z):
        ### Tries to add a new BP independent of others
        
        this.initial = x
        K = Scaff()    
        y = -y    
        K.setId(this.c_id)
        this.c_id = this.c_id+1
        K.setMode(this.mode)
        this.currentAngle= this.initial*this.pAng + this.ang_offset
        K.SetAngle(this.currentAngle)
        K.SetXAng(0)
        this.firstTime = True

        rr = y+z
        if rr%2 == 1:
            K.TurnZ()


        K.AddObj((x,2*y,2*z))
        
        this.prevBP = K

        if this.Elements == None:
            this.Elements = []
        this.Elements.append(this.prevBP)

        Ppos = this.prevBP.getXYZ()
        x,y,z = Ppos[0],Ppos[1], Ppos[2]

        this.minX = min(x,this.minX)
        this.minY = max(y,this.minY)
        this.minZ = min(z,this.minZ)

        this.maxX = max(x, this.maxX)
        this.maxY = min(y, this.maxY)
        this.maxZ = max(z, this.maxZ)

        K.getAngleX()		        


    def AddHelix(this,x,y,z,angle):
        this.Parallel = True
        K = Scaff()    
        y = -y    
        K.setId(this.c_id)
        this.c_id = this.c_id+1
        K.setMode(this.mode)
        K.SetAngle(angle)
        K.SetXAng(0)
        this.firstTime = True
        K.AddObj((x,2*y,2*z))
        this.currentAngle= this.initial*this.pAng
        this.prevBP = K

        if this.Elements == None:
            this.Elements = []
        this.Elements.append(this.prevBP)

        Ppos = this.prevBP.getXYZ()
        x,y,z = Ppos[0],Ppos[1], Ppos[2]

        this.minX = min(x,this.minX)
        this.minY = max(y,this.minY)
        this.minZ = min(z,this.minZ)
        
        this.maxX = max(x, this.maxX)
        this.maxY = min(y, this.maxY)
        this.maxZ = max(z, this.maxZ)        

        K.getAngleX()		

    def GetX(this):
        pX = 0
        if this.prevBP != None:
            pX = this.prevBP.getX()
        
        return pX
    
    def GetY(this):
        pY = 0
        if this.prevBP != None:
            pY = this.prevBP.getXYZ()[1]
        
        return pY  

    def GetZ(this):
        pZ = 0
        if this.prevBP != None:
            pZ = this.prevBP.getXYZ()[2]
        
        return pZ
    
            
    def GotoX(this, X):
        ### Adds enough elements to move to the respective X coordinate
        P = this.prevBP.getXYZ()
        pX = P[0]
        
        d = abs(X-pX)
        oz = this.prevBP.getOz()

        if oz == 0 or oz == 360:
            if pX > X:
                this.AddTurn_Y_down()
        else:
            if pX < X:
                this.AddTurn_Y_down()

        this.AddMore(d)

    def GotoXUp(this, X):
        ### Adds enough elements to move to the respective X coordinate
        P = this.prevBP.getXYZ()
        pX = P[0]
        
        d = abs(X-pX)
        oz = this.prevBP.getOz()

        if oz == 0 or oz == 360:
            if pX > X:
                this.AddTurn_Y_up()
        else:
            if pX < X:
                this.AddTurn_Y_up()

        this.AddMore(d)

    def RectUp(this, width, height, shift = 0):
        this.AddRectUp(width, height, shift)

    def RectDown(this,width, height, shift = 0):
        this.AddRect(width, height, shift)        

    def AddRect_old(this, width , height) :
        ### Adds a rectangule forward with an specific size
        if this.prevBP == None:
            this.Add(1)

        P = this.prevBP.getXYZ()
        pX = P[0]
        pY = -P[1]

        dX = pX + width
        dY = pY + height*2

        Exito = False

        maxX = dX
        minX = pX

        height = width*height

        print("Creating system..." + str(height))

        while Exito == False:
            if this.CheckMax() == False:
                break
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = -C[1]

            minX = min(minX,CX)
            maxX = max(maxX,CX)
            
            oz = this.prevBP.getOz()

            #print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )

            if oz == 0 or oz == 360:
                if CX < dX : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        this.AddTurn_Y_down()

            else:
                if CX > pX : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        this.AddTurn_Y_down() 

        if oz == 0 or oz == 360:
            this.GotoX(maxX)
        else:
            this.GotoX(minX)

    
    def AddRect(this, width , height, shift = 0) :
        ### Adds a rectangule forward with an specific size
        if this.prevBP == None:
            this.Add(1)

        P = this.prevBP.getXYZ()
        pX = P[0] + shift
        
        Ny = 1
        if this.growAxes == "Z":
            Ny = 2
        
        pY = -P[Ny]


        if this.growSign:
            dX = pX + width
        else:
            dX = pX
            pX = pX - width
        
        
        dY = pY + height*2

        Exito = False

        maxX = dX
        minX = pX

        height = width*height

        print("Creating system..." + str(height))
        tX1 = 0
        tX2 = 0
        while Exito == False:
            if this.CheckMax() == False:
                break
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = -C[Ny]

            minX = min(minX,CX)
            maxX = max(maxX,CX)
            
            oz = this.prevBP.getOz()

            #print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )

            if CY == dY-2:
                if oz == 0 or oz == 360:
                    tX2 = this.bp2end
                else:
                    tX1 = this.bp2end

            if oz == 0 or oz == 360:
                if CX < dX -tX1 : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        if this.growAxes == "Y":
                            this.AddTurn_Y_down()
                        else:
                            this.AddTurn_Z_down()

            else:
                if CX > pX +tX2: ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        if this.growAxes == "Y":
                            this.AddTurn_Y_down()
                        else:
                            this.AddTurn_Z_down()

        if oz == 0 or oz == 360:
            this.GotoX(maxX-this.bp2end)
        else:
            this.GotoX(minX+this.bp2end)

        this.bp2end = 0
        
    def AddRect_old_latest(this, width , height) :
        ### Adds a rectangule forward with an specific size
        if this.prevBP == None:
            this.Add(1)

        P = this.prevBP.getXYZ()
        pX = P[0]
        
        Ny = 1
        if this.growAxes == "Z":
            Ny = 2
        
        pY = -P[Ny]


        if this.growSign:
            dX = pX + width
        else:
            dX = pX
            pX = pX - width
        
        
        dY = pY + height*2

        Exito = False

        maxX = dX
        minX = pX

        height = width*height

        print("Creating system..." + str(height))
        tX1 = 0
        tX2 = 0
        while Exito == False:
            if this.CheckMax() == False:
                break
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = -C[Ny]

            minX = min(minX,CX)
            maxX = max(maxX,CX)
            
            oz = this.prevBP.getOz()

            #print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )

            if CY == dY-2:
                if oz == 0 or oz == 360:
                    tX2 = this.bp2end
                else:
                    tX1 = this.bp2end

            if oz == 0 or oz == 360:
                if CX < dX -tX1 : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        if this.growAxes == "Y":
                            this.AddTurn_Y_down()
                        else:
                            this.AddTurn_Z_down()

            else:
                if CX > pX +tX2: ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        if this.growAxes == "Y":
                            this.AddTurn_Y_down()
                        else:
                            this.AddTurn_Z_down()

        if oz == 0 or oz == 360:
            this.GotoX(maxX-this.bp2end)
        else:
            this.GotoX(minX+this.bp2end)

        this.bp2end = 0





    def AddRectUp_old(this, width , height) :
        ### Adds a rectangule forward with an specific size
        if this.prevBP == None:
            this.Add(1)

        P = this.prevBP.getXYZ()
        pX = P[0]
        pY = P[1]

        dX = pX + width
        dY = pY + height*2

        Exito = False

        maxX = dX
        minX = pX

        print("Creating system..." + str(height))

        while Exito == False:
            if this.CheckMax() == False:
                break
            
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = C[1]

            minX = min(minX,CX)
            maxX = max(maxX,CX)
            
            oz = this.prevBP.getOz()

            #print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )

            if oz == 0 or oz == 360:
                if CX < dX : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        this.AddTurn_Y_up()
                        

            else:
                if CX > pX : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        this.AddTurn_Y_up()         

        
        if oz == 0 or oz == 360:
            this.GotoX(maxX)
        else:
            this.GotoX(minX)


    def AddRectUp(this, width , height, shift = 0) :
        ### Adds a rectangule forward with an specific size
        if this.prevBP == None:
            this.Add(1)

        P = this.prevBP.getXYZ()
        pX = P[0] + shift ##  
        
        Ny = 1;
        
        if this.growAxes == "Z":
            Ny = 2
        
        pY = P[Ny]
        

        if this.growSign:
            dX = pX + width
        else:
            dX = pX
            pX = pX - width
        #dX = pX + width
        
        
        
        dY = pY + height*2

        Exito = False

        maxX = dX
        minX = pX

        print("Creating system..." + str(height))
        tX1 = 0
        tX2 = 0
        while Exito == False:
            
            if this.CheckMax() == False:
                break
            
            
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = C[Ny]

            minX = min(minX,CX)
            maxX = max(maxX,CX)
            
            oz = this.prevBP.getOz()

            #print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )
            
            if CY == dY-2:
                if oz == 0 or oz == 360:
                    tX2 = this.bp2end
                else:
                    tX1 = this.bp2end
                

            if oz == 0 or oz == 360:
                if CX < dX -tX1 : ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        if this.growAxes == "Y":
                            this.AddTurn_Y_up()
                        else:
                            this.AddTurn_Z_up()
                        

            else:
                if CX > pX +tX2: ### I am in the range
                    this.AddBP()
                else:
                    if CY == dY:
                        Exito = True
                    else:
                        if this.growAxes == "Y":
                            this.AddTurn_Y_up()         
                        else:
                            this.AddTurn_Z_up()
            
            
        
        if oz == 0 or oz == 360:
            this.GotoX(maxX - this.bp2end)
        else:
            this.GotoX(minX + this.bp2end)

        this.bp2end = 0
            
    
        
    def AddBP(this):
        ang_offset=10
        K = Scaff()
        K.baseRot = this.pAng
        K.setId(this.c_id)
        this.c_id = this.c_id+1
        K.setMode(this.mode)

        
        
        if this.Elements == None:
            this.Elements = []
        
        
        
        if (this.firstTime == False):
            print("Added initial")
            
            if (this.Lattice == "HoneyComb"):
                ang_offset = 270
                
                
            K.SetAngle(this.initial*this.pAng*0.5+ang_offset)
            K.ox = ang_offset
            #K.SetXAng(0)
            this.firstTime = True
            K.AddObj((this.initial,0,0))
            this.currentAngle= this.initial*this.pAng*0.5+ang_offset
            this.prevBP = K
            
                
            
        else:
            K.SetAngle(this.pAng)
            K.AddObj((1,0,0))
            K.SetPrev(this.prevBP)
            this.currentAngle= this.currentAngle+this.pAng
            
            ## Reset for precision issues
            if abs(floor(this.currentAngle)-this.currentAngle) < 0.001:
                this.currentAngle = floor(this.currentAngle)
            elif abs(ceil(this.currentAngle)-this.currentAngle) < 0.001:
                this.currentAngle = ceil(this.currentAngle)
            
        
        this.prevBP = K

        this.Elements.append(this.prevBP)

#        if (this.currentAngle >= 360):
#            this.currentAngle = this.currentAngle - 360
        
        this.currentAngle = this.AdjustAngle(this.currentAngle)
        
        #print("Current angle")
        #print(this.GetXAngle())
        # print("pAng")
        # print(this.pAng)
        
        
        Ppos = this.prevBP.getXYZ()

        x,y,z = Ppos[0],Ppos[1], Ppos[2]
        
        this.minX = min(x,this.minX)
        this.minY = max(y,this.minY)
        this.minZ = min(z,this.minZ)


        this.maxX = max(x, this.maxX)
        this.maxY = min(y, this.maxY)
        this.maxZ = max(z, this.maxZ)

#        print("Angle: ")
#        print(round(this.currentAngle))
        #K.getAngleX()
        #this.xAngle = K.getAngleX()
        #print(xAngle)
                    

    def AddMore(this, n):
        
        for k in range(n):
            if this.CheckMax():
                this.AddBP();
            else:
                break
            
            
                
            
            
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            #lastAng = this.GetXAngle()
            #print("R:")
            #print (lastAng)

            
    
    def GetXAngleN(this):
        tt = 0
        if this.prevBP.getOz() == 0 or this.prevBP.getOz() == 360:
            tt = this.currentAngle
        else:
            tt = 180-this.currentAngle
        
        if tt < 0:
            tt=tt+360 
        return tt
    
    def GetXAngle(this):
        tt = this.prevBP.getAngleX()    
        if tt < 0:
            tt=tt+360
        
        if tt >= 360:
            tt = tt-360
        
        return tt

    def GetXAngle2(this):
        tt = this.prevBP.getAngleX() 
        
        if this.prevBP.getOz() == 180:
            tt = tt-180        
        
        if tt < 0:
            tt=tt+360
        
        if tt >= 360:
            tt = tt-360
            

        
        return tt
    
    def AddTurn_Z_down(this):
        if this.Lattice == "Square":
            this.AddTurn_Z(0)
        if this.Lattice == "HoneyComb":
            this.AddTurn_H(180)
    
    def AddTurn_Z_up(this):
        if this.Lattice == "Square":
            this.AddTurn_Z(180)
        if this.Lattice == "HoneyComb":
            this.AddTurn_H(0)
    
    def AddTurn_Y_down(this):
        #if this.prevBP.getOz() == 180:
        #    this.AddTurn_Y(270) 
        #else:
        
        
        if this.Lattice == "Square":
            this.AddTurn_Y(270)
        if this.Lattice == "HoneyComb":
            this.AddTurn_H(270)

    def AddTurn_Y_up(this):
        #if this.prevBP.getOz() == 180:  ### Coming back
        #    this.AddTurn_Y(90)   
        #else:
        if this.Lattice == "Square":
            this.AddTurn_Y(90)# Coming up
        if this.Lattice == "HoneyComb":
            this.AddTurn_H(90)  
        
    def testingAngle(this,A,B):
        #compare distance between angles
        if A>360:
          A=A-360

        if A < -180:
          A=A+360    

        if B>360:
          B=B-360        

        if B < -180:
          B=B+360       

        C=abs(A-B)
        
        if C > 180:
          C=C-360

        return abs(C)
             

    def AddTurn_Z_old(this,n, targetAngle):
        ### Add n BP and then continue
        ### until turn down in Y direction
        #targetAngle = 270
        this.AddMore(n)
        
        if (this.prevBP.getOz() != 180):
            targetAngle = targetAngle
        else:
            targetAngle = targetAngle+180
            
        
        #testAng = abs(this.prevBP.getAngleX()-targetAngle)
        #testAng = abs(this.GetXAngle()-targetAngle)
        testAng=this.testingAngle(this.GetXAngle(), targetAngle)
        
        
        cuenta = 0
        lastAng = 0
        while testAng > this.pAng:
            this.AddBP()
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            testAng = this.testingAngle(lastAng, targetAngle)
            #testAng = abs(lastAng-targetAngle)            
            cuenta = cuenta + 1
            #print("R:")
            #print (lastAng)
            
            if cuenta > 30:
                testAng = 0
        
        #print("Last Angle")
        #print(lastAng)
        
        if cuenta < 30:    
        ### now Add another BP and rotate it
            this.AddBP()
            this.prevBP.GetObj().location = (0,0,-2)            
            this.prevBP.GetObj().rotation_euler.rotate_axis("Z", radians(180))
            this.prevBP.GetObj().rotation_euler.rotate_axis("X", radians(180)) 
            
            this.prevBP.addAngleX(180)       
            this.prevBP.TurnZ()
            
            this.prevBP.compensateX(testAng)
            
            #print("TestAng")
            #print (testAng)
           
            
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            #print("R:")
            #print (lastAng)
        
        #print("End turn")    
            
#        this.currentAngle = 0


    def AddTurn_Z(this, targetAngle):
        ### Add n BP and then continue
        ### until turn down in Y direction
        #targetAngle = 270
        #testAng = abs(this.prevBP.getAngleX()-targetAngle)

        ### If direction is negative, which angle should it turn?

        if targetAngle == 0:
            targetAngle = 360

        GA =   this.GetXAngle2()-targetAngle      

        testAng = abs(GA)
        
        if GA <= 0:
            testAng += 360
    
        
        cuenta = 0
        lastAng = 0
        print("Target: " + str(targetAngle))
        print("Doing Z turn, Angle " + str( this.GetXAngle()) + " -> " + str(testAng))
        
        
        while testAng > this.pAng+0.5:
            this.AddBP()
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle2()
            GA = lastAng-targetAngle
            
            testAng = abs(GA) 
            print("Angle: " + str(lastAng) + " -> " + str(testAng))
            
            
            
            if GA > 0:
                testAng += 360
            
            
            
            cuenta = cuenta + 1
            #print("R:")
            #print (lastAng)
            
            if cuenta > 30:
                testAng = 0
        
        #print("Last Angle")
        #print(lastAng)
        
        if cuenta < 30:    
        ### now Add another BP and rotate it
            if this.prevBP.getOz() == 0 or this.prevBP.getOz() == 360:
                this.AddBP()
            else:
                this.AddBP()

            this.prevBP.setTurn( (targetAngle) )

            #this.prevBP.GetObj().location = (0,0,-2)            
            #this.prevBP.GetObj().rotation_euler.rotate_axis("Z", radians(180))
            #this.prevBP.GetObj().rotation_euler.rotate_axis("X", radians(180)) 
            
            #this.prevBP.addAngleX(180)       
            #this.prevBP.TurnZ()
            #this.prevBP.compensateX(testAng)
            
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            #print("R:")
            #print (lastAng)
        
        #print("End turn")    
            
#        this.currentAngle = 0

        
    def AddTurn_Y_deprecated(this, targetAngle):
        ### Add n BP and then continue
        ### until turn down in Y direction
        #targetAngle = 270
        #testAng = abs(this.prevBP.getAngleX()-targetAngle)

        ### If direction is negative, which angle should it turn?


        testAng = (targetAngle-this.GetXAngle())
        cuenta = 0
        lastAng = 0
        
        if testAng < 0:
            testAng += 360
        
        #print("Xangle " + str(this.GetXAngle()))
        #print("testang " + str(testAng))
        #print("pang " + str(this.pAng))
        print("Angle " + str( this.GetXAngle()) + " -> " + str(testAng))
        while testAng > this.pAng:
            this.AddBP()
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            testAng = (targetAngle-lastAng)   
            
            if testAng < 0:
                testAng += 360
            
            print(str(lastAng) + " -> " + str(testAng))
            cuenta = cuenta + 1
            #print("R:")
            #print (lastAng)
            
            if cuenta > 30:
                testAng = 0
        
        #print("Last Angle")
        #print(lastAng)
        
        if cuenta < 30:    
        ### now Add another BP and rotate it
            if this.prevBP.getOz() == 0 or this.prevBP.getOz() == 360:
                this.AddBP()

            this.prevBP.setTurn( (targetAngle) )

            #this.prevBP.GetObj().location = (0,0,-2)            
            #this.prevBP.GetObj().rotation_euler.rotate_axis("Z", radians(180))
            #this.prevBP.GetObj().rotation_euler.rotate_axis("X", radians(180)) 
            
            #this.prevBP.addAngleX(180)       
            #this.prevBP.TurnZ()
            #this.prevBP.compensateX(testAng)
            
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            #print("R:")
            #print (lastAng)
        
        #print("End turn")    
            
#        this.currentAngle = 0

        
   
    def AddTurn_Y(this, targetAngle):
        ### Add n BP and then continue
        ### until turn down in Y direction
        #targetAngle = 270
        #testAng = abs(this.prevBP.getAngleX()-targetAngle)

        ### If direction is negative, which angle should it turn?


        testAng = (targetAngle-this.GetXAngle())
        cuenta = 0
        lastAng = 0
        
        if testAng < 0:
            testAng += 360
        

        print("Doing Y turn, Angle " + str( this.GetXAngle()) + " -> " + str(testAng))
        
        while testAng > this.pAng:
            this.AddBP()
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            testAng = (targetAngle-lastAng)   
            
            if testAng < 0:
                testAng += 360
            
            print(str(lastAng) + " -> " + str(testAng))
            cuenta = cuenta + 1
            #print("R:")
            #print (lastAng)
            
            if cuenta > 30:
                testAng = 0
        
        
        if cuenta < 30:    
        ### now Add another BP and rotate it
            if this.prevBP.getOz() == 0 or this.prevBP.getOz() == 360:
                print("Adding last BP")
                this.AddBP()
            else:
                print("Adding last BP2")
                this.AddBP()

            this.prevBP.setTurn( (targetAngle) )

            lastAng = this.GetXAngle()


    def AddTurn_H(this, targetAngle):
        ### Add n BP and then continue
        ## Modified version for HoneyComb
        
        ## This follows the Square Model
        ## And adapts to the HoneyComb
        ## The Target Angle is computed with 
        ## Respect to the last position
        ## Let's see how this will work
        
        ## Target = 0, 90, 180, 270
        ## New target: 270, 30, 150
        ## New target: 120, 240, 90
        
        nt1 = [ 0, 90, 180, 270 ]
        ##    [ Z+, Y+, Z-, Y- ]
        
        
        t1  = [ 30, 150, 150, 270 ]
        t1b = [ 30, 30, 150, 270 ]
        t2  = [ 330, 90,  210, 210 ]
        t2b = [ 330, 90,  210, 330 ]
        
#        this.HCSet = 0
        
        
        if this.HCSet == 1:
            t1 = t1b
            t2 = t2b
        
            
        
        newtarget = 0
        
        ## Control Variables:
        print(this.prevAngle)  ## Honeycomb angle
        print(this.CurrentSense) ## Square reference
        
        opcs = nt1.index(targetAngle)
#        if this.CurrentSense == targetAngle:
        
        if this.prevAngle in t1:
            newtarget = t1[opcs]
            if opcs == 1:
                if this.HCSet == 0:
                    this.HCSet = 1
                else:
                    this.HCSet = 0
        else:
            newtarget = t2[opcs]
            if opcs == 3:
                if this.HCSet == 0:
                    this.HCSet = 1
                else:
                    this.HCSet = 0
            
#        newtarget = this.prevAngle;
#        newtarget = this.AdjustAngle(this.prevAngle + 120)
        
        
#        if this.prevAngle in t1        
        
        
        this.prevAngle = this.AdjustAngle(newtarget+180)
        
        targetAngle = newtarget
        
        print("Target: ")
        print(round(targetAngle))
        
#        offNewAngle = this.pAng
        
        
        
        

        testAng = (targetAngle-this.GetXAngle())
        cuenta = 0
        lastAng = 0
        
        testAng = this.AdjustAngle(testAng) 
        

        print("Doing H turn, Angle " + str( this.GetXAngle()) + " -> " + str(testAng))
        
        while testAng > 2: ## Honeycomb has exact angles
            this.AddBP()
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle() 
            
            testAng = this.DistanceAng(targetAngle,lastAng)   
            
#            print(str(lastAng) + " -> " + str(testAng))
            cuenta = cuenta + 1
            #print("R:")
            #print (lastAng)
            
#            print("L: " + str( round(lastAng)) + "  N: " + str( round(testAng)) )
            if cuenta > 30:
                testAng = 0
        
        print ("R: " + str(lastAng))
        if cuenta < 30:    
        ### now Add another BP and rotate it
            if this.prevBP.getOz() == 0 or this.prevBP.getOz() == 360:
#                print("Adding last BP")
                this.AddBP()
            else:
#                print("Adding last BP2")
                this.AddBP()

            this.prevBP.setTurnH( targetAngle )

            lastAng = this.GetXAngle()
    
    
    
    def AddRow(this,x,y,z):
        #pAng = -5*360/20

        Pos = Vector((x,y,z))
        
        #bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
        #bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
        #bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, location = (0, 0, 0) )
        #Pivot = bpy.data.objects[-1]
        First = None 
        Prev = None
        
        assigned = False
        
        
        
        for n in range(62):
            
            K = Scaff()
            K.setId(this.c_id)
            
            this.c_id = this.c_id+1
            
            K.setMode(this.mode)
            

            
            if (this.firstTime == False):
                K.SetAngle(0)
                this.firstTime = True
            else:
                K.SetAngle(this.pAng)
            
            
            #this.pAng = this.pAng - 360/20
        
            K.AddObj((1,0,0))
            
            if  assigned == False :
                First = K
                assigned = True
                Prev = K
            else: 
                K.SetPrev(Prev)

            #Npos = n*this.direction + Pos
            #Scaff.createSphere(1,1,2,2)

            #K.Add(Npos[0],Npos[1],Npos[2])
            #print(K.GetObj())

            Prev = K
            

        
        First.GetObj().location = Pos;

        #First.GetObj().parent = Pivot
        
        
            
        #Pivot.location = Pos;
        # Rotation
        # Direction (1,0,0): Standar 
        #First.GetObj().rotation_euler=(0,0,0)
        First.GetObj().rotation_euler.rotate_axis("X", radians( (this.direction[0])*90 ))
        First.GetObj().rotation_euler.rotate_axis("Y", radians( (this.direction[2])*90 ))
        First.GetObj().rotation_euler.rotate_axis("Z", radians( (this.direction[1])*90 ))       
        
        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
        
        TT = First
        
        #for h in range(10):
        #    print(TT.getOrientation())
        #    TT = TT.GetNext()
    
    def analyzeStructure(this):

        if this.Analyzed == False :

            ## set minimum: Compensate negative coordinates

            #print("Compensating coordinates")
            print(this.minX)
            print(this.minY)
            print(this.minZ)

            if this.minX < 0 or this.minY > 0 or this.minZ < 0:
                print("Compensating coordinates")
                ### Compensate
                sY = - this.minY*2
                sZ = - this.minZ*2

                ### X should be increased in terms of the angle: 21 bp
                ### that is, if x = -1, should be 19
                sX = abs(this.minX - this.minX % 21  ) 

                for BP in this.Elements:
                    BP.shift(sX, sY, sZ)

            ## End minimum 

            this.HelCad = HelixCad()
            this.HelCad.SetParallel(this.Parallel)
            #this.HelCad.setLast(this.prevBP)
            
            this.prevSize = len(this.Elements)
            
            this.HelCad.setElements(this.Elements)
            
            this.HelCad.buildRods()
            
            this.HelCad.RemoveConflict()
            
            this.Elements = this.HelCad.getElements()
            
            this.finalSize = len(this.Elements)
            
           
            

            if this.Draft == False:
                this.HelCad.AnalyzeStaples()

                #this.HelCad.solveConflicts()

                #this.HelCad.stepGrowStaples()


                if this.Parallel == False:
                    this.HelCad.reduceStaples()
                    print("Reducing staples")
                    
                else:
                    None
                    this.HelCad.stepGrowStaples()

                #this.HelCad.reduceStaples()

                #this.HelCad.stepGrowStaples()
                

                this.HelCad.applyStaples()

                this.HelCad.stapleWorkarounds()
                #this.HelCad.CleanStaple()


            this.Analyzed = True


    ## Compatibility with previous name
    def writecaDNAno(this, filename):
        this.writeCaDNAno(filename)
        
    
    def writeCadnano(this, filename):
        this.writeCaDNAno(filename)
        
    def writeCaDNAno(this, filename):

        #this.HelCad = HelixCad()

        #sal = ExportCad()
        
        #sal.setLast(this.prevBP)
        
        #sal.buildRods()
        
        #sal.AnalyzeStaples()
        # ~ sal.AnalyzeStaplesOld()

        #sal.writeFile(filename)
        this.analyzeStructure()

        this.HelCad.writeFile(filename)

    
    def SetSkips(this):
        ### Analyse the structure and search differences
        ## Between 10.5 bp per turn and 10.67, then align
        bAng = 720/21  ### 10.5
        
        cAng = (10-bAng)/2
        
        dAng = this.Elements[0].ox
        
        for BP in this.Elements:
            #dAng = BP.ox
            dAng = this.AdjustAngle(dAng + this.pAng)
            
            difference = this.AdjustAngle(dAng - cAng)
            
            
            if difference < 180:
                cAng  = this.AdjustAngle( cAng + bAng )
            else:
                BP.Skip = True
            
    
    
    def CleanAll(this):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)

    def Clean(this):
        bpy.ops.object.select_all(action='SELECT')
        
        ## Omit objects that are not object_name*
        for cosa in bpy.data.objects:
            if ("object_name" in cosa.name) == False:
                cosa.select_set(False)
        
        
        bpy.ops.object.delete(use_global=False, confirm=False)
    
    def RenderCylinders(this, res = 5):
        
        this.analyzeStructure()
        render = RenderCad()
        render.setHelices(this.HelCad)
        minvector = [this.minX, this.minY, this.minZ]
        
        render.RenderCylinders(res, minvector )

    def RenderRibbons(this):
        
        this.analyzeStructure()
        render = RenderCad()
        render.setHelices(this.HelCad)
        render.RenderRibbons()

    def RenderPDF(this, filename):
        this.analyzeStructure()
        render = RenderCad()
        render.setHelices(this.HelCad)
        render.RenderPDF3(filename)
        



        
  
    
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.delete(use_global=False, confirm=False)
