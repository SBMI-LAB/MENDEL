import bpy
from mathutils import Vector
from time import sleep


def print(data):

    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT") 
                


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

filepath = bpy.path.abspath("//Render.py")
exec(compile(open(filepath).read(), filepath, 'exec'))

try:
    filepath = bpy.path.abspath("//asymptote.py")
    exec(compile(open(filepath).read(), filepath, 'exec'))
except:
    print("Module asymptote cannot be initialized")


class Cadnano():
    
    mode = "Wire"
    
    direction = Vector((1,0,0))
    
    prevBP = None
    
    CurrentRow = None
    pAng = 720/21
    
    
    firstTime = False
    
    c_id = 0
    
    initial = 0
    
    currentAngle = 0
    
    xAngle = 0

    HelCad = None

    Analyzed = False

    Draft = False

    

    def setDraft(this):
        this.Draft = True
    
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
        this.initial = n
        #this.AddBP()
        
    def AddHelix(this,x,y,z,angle):
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

        K.getAngleX()		

    def gotoX(this, X):
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

    def gotoXUp(this, X):
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
        

    def AddRect(this, width , height) :
        ### Adds a rectangule forward with an specific size
        P = this.prevBP.getXYZ()
        pX = P[0]
        pY = -P[1]

        dX = pX + width
        dY = pY + height*2

        Exito = False

        height = width*height

        print("Creating system..." + str(height))

        while Exito == False:
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = -C[1]
            
            oz = this.prevBP.getOz()

            print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )

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






    def AddRectUp(this, width , height) :
        ### Adds a rectangule forward with an specific size
        P = this.prevBP.getXYZ()
        pX = P[0]
        pY = P[1]

        dX = pX + width
        dY = pY + height*2

        Exito = False

        

        print("Creating system..." + str(height))

        while Exito == False:
            C = this.prevBP.getXYZ()
            CX = C[0]
            CY = C[1]
            
            oz = this.prevBP.getOz()

            print( "Target : " + str(CX) + ": " + str(pX)  + " - "+ str(dX)  + " ==>" + str(oz)  )

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



            

        
    def AddBP(this):
        K = Scaff()
        K.setId(this.c_id)
        this.c_id = this.c_id+1
        K.setMode(this.mode)
        if (this.firstTime == False):
            K.SetAngle(this.initial*this.pAng)
            #K.SetXAng(0)
            this.firstTime = True
            K.AddObj((this.initial,0,0))
            this.currentAngle= this.initial*this.pAng
            this.prevBP = K
        else:
            K.SetAngle(this.pAng)
            K.AddObj((1,0,0))
            K.SetPrev(this.prevBP)
            this.currentAngle= this.currentAngle+this.pAng
        
        this.prevBP = K
        if (this.currentAngle >= 360):
            this.currentAngle = this.currentAngle - 360
        
        
        K.getAngleX()
        #this.xAngle = K.getAngleX()
        #print(xAngle)
                    

    def AddMore(this, n):
        for k in range(n):
            this.AddBP();
            
            
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            #lastAng = this.GetXAngle()
            #print("R:")
            #print (lastAng)

            
    
    def GetXAngle(this):
        tt = this.prevBP.getAngleX()    
        if tt < 0:
            tt=tt+360
        
        if tt >= 360:
            tt = tt-360
        
        return tt
    
    def AddTurn_Z_down(this):
        this.AddTurn_Y(0)    
    
    def AddTurn_Z_up(this):
        this.AddTurn_Y(180)
    
    def AddTurn_Y_down(this):
        this.AddTurn_Y(270)

    def AddTurn_Y_up(this):
        this.AddTurn_Y(90)   
        
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
             

    def AddTurn_Z(this,n, targetAngle):
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

        
    def AddTurn_Y(this, targetAngle):
        ### Add n BP and then continue
        ### until turn down in Y direction
        #targetAngle = 270
        
        
        #testAng = abs(this.prevBP.getAngleX()-targetAngle)
        testAng = abs(this.GetXAngle()-targetAngle)
        cuenta = 0
        lastAng = 0
        while testAng > this.pAng:
            this.AddBP()
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
            lastAng = this.GetXAngle()
            testAng = abs(lastAng-targetAngle)            
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
            this.HelCad = HelixCad()
            this.HelCad.setLast(this.prevBP)
            this.HelCad.buildRods()


            if this.Draft == False:
                this.HelCad.AnalyzeStaples()

                #this.HelCad.solveConflicts()

                this.HelCad.stepGrowStaples()


                this.HelCad.reduceStaples()

                #this.HelCad.stepGrowStaples()
                

                this.HelCad.applyStaples()

                #this.HelCad.CleanStaple()


            this.Analyzed = True



        
    def writeCadnano(this, filename):

        #this.HelCad = HelixCad()

        #sal = ExportCad()
        
        #sal.setLast(this.prevBP)
        
        #sal.buildRods()
        
        #sal.AnalyzeStaples()
        # ~ sal.AnalyzeStaplesOld()

        #sal.writeFile(filename)
        this.analyzeStructure()

        this.HelCad.writeFile(filename)

    def Clean(this):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)

    
    def RenderCylinders(this, res):
        
        this.analyzeStructure()
        render = RenderCad()
        render.setHelices(this.HelCad)
        render.RenderCylinders(res)

    def RenderRibbons(this):
        
        this.analyzeStructure()
        render = RenderCad()
        render.setHelices(this.HelCad)
        render.RenderRibbons()

    def RenderPDF(this, filename):
        this.analyzeStructure()
        render = RenderCad()
        render.setHelices(this.HelCad)
        render.RenderPDF(filename)
        



        
  
    
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.delete(use_global=False, confirm=False)
