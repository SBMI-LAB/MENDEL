Blender = False
try:
    import bpy
    Blender = True
except:
    from Vector import *

from math import *

class Scaff():
    name = "name"

    baseRot = 720/21

    sid = 0
    r_id = 0
    p_id = 0
    
    pSep = 0.8
    
    sSep = 0.8
    
    HCSet = 0 ## Honeycomb set to switch
    
    Ob_center = None
    Ob_scaf = None
    Ob_link = None
    
    Prev = None
    Next = None
    
    PrevStp = None
    NextStp = None
    
    StapleObj = None
    
    StapleStrand = None
    
    x, y, z = 0,0,0

    sx,sy, sz = 0,0,0

    lx,ly,lz = 0,0,0
    
    ox,oy,oz = 0,0,0
    
    ### honeycomb related
    hx, hy, hz = 0,0,0
    

    ang = 0
    
    mode = "Final"
    
    compatible = True
    
    geom = False
    
    rodnumber = 0
    posinrod = 0
    
    NextRod = None
    PrevRod = None
    
    assigned = False
    
    inTurn = False
    
    #Minnor grove angle
    minGr = -0
    # ~ asigned = 0
    
    Skip = False
    
    def setNextRod(this, BP):
        if this.getRod() == BP.getRod():
            this.NextRod = BP
            BP.setPrevRod(this)
    
    def setPrevRod(this, BP):
        if this.getRod() == BP.getRod():
            this.PrevRod = BP
    
    def getNextRod(this):
        if this.oz == 0 or this.oz == 360:
            return this.NextRod
        else:
            return this.PrevRod

    def getPrevRod(this):
        if this.oz == 0 or this.oz == 360:
            return this.PrevRod
        else:
            return this.NextRod
    
    
    def distStp(this, Other):
        D = 0
        P1 = this.getPosStp()
        P2 = Other.getPosStp()
        
        ## Como es la distancia en 3D
        dx = abs(P1[0]-P2[0])
        dy = abs(P1[1]-P2[1])
        dz = abs(P1[2]-P2[2])
        
        dxy = sqrt( dx*dx + dy*dy )
        
        D = sqrt(dxy*dxy + dz*dz)
        
        #D = (P1-P2).length
        return D

    def shift(this, x,y,z):
        this.x += x
        this.y += y
        this.z += z
        
        this.hx += x
        this.hy += abs(int(y))
        this.hz += abs(int(z))


    def setStaple(this, staple):
        this.StapleObj = staple
        # ~ print("A:  " + str(this.rodnumber) + ": " + str(this.x))
        # ~ this.asigned += 1
        # ~ print("Asigned: " + str(this.asigned))
    
    def getStaple(this):
        return this.StapleObj

    def updateElements(this):

        if this.geom: 

            if this.Ob_link != None:
                this.Ob_link.location = (this.lx,this.ly,this.lz)

            if this.Ob_scaf != None:
                this.Ob_scaf.location = (this.sx,this.sy,this.sz)

            if this.Ob_center != None:
                this.Ob_center.location = (this.x,this.y,this.z)            


    def setTurnH(this, TargetAngle):
        ### Do the changes for the Honeycomb
        this.inTurn = True
        
        if this.getPrev() != None :
            ## Reset coordinates
            G = this.Prev.getXYZ()
            this.x = G[0]
            this.y = G[1]
            this.z = G[2]
            
            this.y = this.y + 2*sin(radians(TargetAngle))
            this.z = this.z + 2*cos(radians(TargetAngle))
            
            #this.ox = this.ox - 180
            
            if this.oz == 0 or this.oz == 360:
                this.oz = 180
                this.ox = this.ox 
            else:
                this.oz = 0
                this.ox = this.ox + 3*this.baseRot
                #this.ox = this.ox + 2*this.baseRot
                
        ### Set hy and hz according to the target angle
        TA = [330,270, 210, 30, 90, 150]
        dhz = [1,  0,   -1,  1, 0, -1]
        dhy = [0,  1,    0,  0, -1, 0]
        
        for kn in range(len(TA)):
            if TA[kn] == TargetAngle:
                this.hy += 2*dhy[kn]
                this.hz += 2*dhz[kn]
            
            
            
            
            
        
    
    def setTurn(this, P) :
        ### Transform the position and rotate it
        this.inTurn = True
        
        if this.getPrev() != None :
            G = this.Prev.getXYZ()
            
            
            
            this.x = G[0]
            this.y = G[1]
            this.z = G[2]

            
            if P == 270 or P == 270 - this.baseRot:
                print("Turn 270")
                this.y += -2
            
            if P == 90 or P == 90 - this.baseRot:
                this.y += 2

            if P == 0 or P == 360: 
                this.z += -2
                P = 0
            
            if P == 180:
                this.z += 2

            if this.oz == 0 or this.oz == 360:
                this.oz = 180

                print("Case 1")
                ### Compatibility with caDNAno orientation
                if this.compatible == True:
                    print(this.ox)
                    if this.ox > P:
                        this.ox = this.ox-this.baseRot
                        
                    this.ox = 180 - this.ox 

                #this.ox = -this.ox + 180
                
            else:
                this.oz = 0
                print("Case 2")
                ### Compatibility with caDNAno orientation
                if this.compatible == True:
                    this.ox = 180 - this.ox+this.baseRot
            
            
            
            this.updatePos()



    def updatePos (this):
        ### Will update positions of scaffold and stapples
        ### According to the xyz coordinates 
        ### and the orientations
        
        ## Minor grove angle
        minGr = this.minGr
        
        if this.oz == 0 or this.oz == 360:
            ## perform direct rotation
            #print ("Case 1")
            ### check ox and rotate against it
            this.sy = this.pSep*sin(this.ox*radians(180)/180)
            this.sz = -this.pSep*cos(this.ox*radians(180)/180)

            
            ## Staple

            this.ly = -this.sSep*sin((this.ox+minGr)*radians(180)/180)
            this.lz = this.sSep*cos((this.ox+minGr)*radians(180)/180)

            #print("z: " + str(this.sz) + " ang: " + str(this.ox))

        else:
            ## perform opposit rotation
            #print ("Case 2")
            this.sy = -this.pSep*sin(this.ox*radians(180)/180)
            this.sz = -this.pSep*cos(this.ox*radians(180)/180)

            #Staple

            this.ly = this.sSep*sin((this.ox-minGr)*radians(180)/180)
            this.lz = this.sSep*cos((this.ox-minGr)*radians(180)/180)


        this.sx = this.x
        this.sy += this.y
        this.sz += this.z

        this.lx = this.x
        this.ly += this.y
        this.lz += this.z    


        this.updateElements()        

    
    def getNextStp(this):
        return this.NextStp
    
    def setNextStp(this,N, recursive = True):
        this.NextStp = N

        if N != None and recursive == True:
            N.setPrevStp(this, False)

    def getPrevStp(this):
        return this.PrevStp
    
    def setPrevStp(this,N, recursive = True):
        this.PrevStp = N

        if N != None and recursive == True:
            N.setNextStp(this, False)
    
    def setR (this, n):
        this.rodnumber = n
        this.assigned = True
        #print(this.rodnumber)
    
    def setRod(this,n, pos):
        this.rodnumber = n
        this.posinrod = pos
        this.assigned = True
    
    def isAssigned(this):
        return this.assigned
    
    def getPosStp(this):
        #P = Vector( (this.lx, this.ly, this.lz) )
        P = [this.lx, this.ly, this.lz]
        return P
        #return this.Ob_link.matrix_world.to_translation()
    def getPosScaffold(this):
        P = Vector ( (this.sx, this.sy, this.sz) )
        return P
    
    def getPos(this):
        return this.posinrod
        
    def getRod(this):
        return this.rodnumber
    
    def getPrev(this):
        return this.Prev
    
    def getNext(this):
        return this.Next
    
    
    
    def getXYZCenter(this):
		#return P = (this.x, this.y, this.z)
        #return this.Ob_center.matrix_world.to_translation()
        return this.getXYZ()
    
    
    def getOrientation(this):
        return this.Ob_center.matrix_world.to_quaternion().to_euler()
    
    
    def getOz(this):
        return this.oz
    

                
    def compensateX(this, ang):
        if (this.oz != 0):
            this.Prev.GetObj().rotation_euler.rotate_axis("X", radians(ang))           
            this.GetObj().rotation_euler.rotate_axis("X", radians(ang))  
            #this.ox = this.ox + 2*ang         
        else:
            this.Prev.GetObj().rotation_euler.rotate_axis("X", radians(-ang))           
            this.GetObj().rotation_euler.rotate_axis("X", radians(-ang))   
            #this.ox = this.ox - 2*ang   
        
        #print("Compensate")
        #print(ang)
        #print(this.ox)     
    
    
    def addAngleX(this, ang):
        this.ox = this.ox + ang
        if this.ox > 359:
            this.ox=this.ox-360
        if this.ox < 0:
            this.ox = this.ox+360
        
        if this.ox == 360:
            this.ox = 0



    def getAngleX(this):

        if this.oz == 0 or this.oz == 360 :
            aX = this.ox
        else:
            aX = this.ox + 180
            #aX = 360 - this.ox 

        return aX
    
    def oldgetAngleX(this):
        #print( (this.Ob_scaf.matrix_world.to_euler()[0])*180/radians(180))
        aZ = (this.Ob_scaf.matrix_world.to_euler()[2])*180/radians(180)
        #aX = (this.Ob_scaf.matrix_world.to_euler()[0])*180/radians(180)
        
        if this.oz > 359:
            this.oz=this.oz-360
        if this.oz < 0:
            this.oz = this.oz+360
        if this.oz == 360:
            this.oz = 0 
                   
        
        #print("aZ")
        #print(aZ)
        #print(this.oz)
        
        
        aZ = this.oz
        aX = this.ox
        
        sX = this.ox
        
        
        
                
        if abs(aZ) < 10  :
            aX = aX
        else:
            aX = aX#+180
            #sX = 360-sX 

        
        if sX > 180:
            sX = sX-360
            
        #print (this.oz)
        #print ("Real:")
        #print (aX)
        #print ("T:")
        #print(sX)

        #print(this.ox)
        #print(aX)    
        
        return aX
    
    
    def setId(this, cid):
        this.sid = cid
    
    def setMode(this, nmode):
        
        if nmode == "Normal":
            this.compatible = False
        else:
            this.mode = nmode
        
    
    
    def createSphere(this,x,y,z,r):
        
        #print('pic')
        
        if this.mode == "Final" :
            bpy.ops.mesh.primitive_ico_sphere_add(radius=r, location = (x, y, z) )
        elif this.mode == "Wire":
            bpy.ops.mesh.primitive_plane_add(size=r, location = (x, y, z) )
        elif this.mode == "Light":
            bpy.ops.object.light_add(type='POINT', radius=r, location = (x, y, z) )            
        else:
            bpy.ops.object.empty_add(type='SINGLE_ARROW', location=(x, y, z))


     
    def GetObj (this):
        #print(this.Ob_scaf)
        return this.Ob_center
    
    def GetNext (this):
        return this.Next
    
    def SetPrev2(this, Prev):
        this.Prev = Prev
    
    def SetPrev(this, Prev):
        if Prev == None:
            this.Prev = None
        else:
            if this.GetObj() != Prev.GetObj()  or this.geom == False  :
                #this.GetObj().parent = Prev.GetObj()
                P = Prev.getXYZ()
                this.oz = Prev.getOz()


                if this.oz == 0 or this.oz == 360:
                    this.x += P[0] 
                else:
                    this.x = P[0] - this.x
                    #print("Neg")

                this.y += P[1]
                this.z += P[2]
                
                this.hx = this.x
                this.hy = Prev.hy
                this.hz = Prev.hz

                

            this.Prev = Prev
            Prev.SetNext(this)
        


    def getXYZ(this):
        P = (this.x, this.y, this.z)
        return P

    def getX(this):
        return this.x

    def SetNext(this, Next):
        if Next == None:
            this.Next = None
        else:
            this.Next = Next

            Next.SetZAng(this.oz)
            Next.SetXAng(this.ox)  
        
            this.updatePos()
    
    
    def SetXAng (this,ang):
        
        
        #if this.oz == 0 :
        this.ox = ang+this.ang 
        
        
        #else:
        #    this.ox = ang - this.ang
           
        if abs(floor(this.ox)-this.ox) < 0.001:
            this.ox = floor(this.ox)
        elif abs(ceil(this.ox)-this.ox) < 0.001:
            this.ox = ceil(this.ox)

        if this.ox > 360:
            this.ox=this.ox - 360
        
        if this.ox < 0:
            this.ox=this.ox+360
        
        this.updatePos()

        #this.ang = this.ox
        
        #print("A:")
        #print(ang)
        
    
    
    def TurnZ(this):
        this.oz = this.oz+180
        this.ox = -this.ox+180
        if this.oz > 360:
            this.oz = this.oz-360
        
        this.inTurn = True

    
    def SetZAng (this, ang):
        this.oz = ang
        #print(this.oz)
            
    def SetAngle(this,ang):
        this.ang = ang
        

            
    def SetRotation(this):
        this.Ob_link.parent = this.Ob_center
        this.Ob_scaf.parent = this.Ob_center        
        this.Ob_center.rotation_euler.rotate_axis("X", radians(this.ang))



        #print(this.ang)        
        
    
    def AddObj (this,P):
        #print(this.ang)
        x,y,z = P[0],P[1],P[2]
        
        #print(this.sid*2 + 1)
        #print(len(bpy.data.objects) )
        
        this.x = x
        this.y = y
        this.z = z
        
        
        if this.geom :

            if ( this.sid*3 +3  > len(bpy.data.objects)  ) :
            
                this.createSphere(0,0,0,0.2)
                this.createSphere(0,0,-this.pSep,0.3)
                this.createSphere(0,0,this.sSep,0.3)
                this.Ob_center  = bpy.data.objects[-3]                    
                this.Ob_scaf = bpy.data.objects[-2]        
                this.Ob_link = bpy.data.objects[-1]
                #this.SetRotation()
                #this.Ob_center.location = (x,y,z)
            else:
                this.Ob_center = bpy.data.objects[this.sid*3]                    
                this.Ob_scaf = bpy.data.objects[this.sid*3+1]        
                this.Ob_link = bpy.data.objects[this.sid*3+2]
                #this.Ob_center.parent = None            
                #this.Ob_scaf.parent = None
                #this.Ob_link.parent = None
                #this.Ob_center.location=(0,0,0)            
                #this.Ob_scaf.location=(0,0,-this.pSep)
                #this.Ob_link.location=(0,0,this.sSep)

                #this.SetRotation()
                #this.Ob_center.location = (x,y,z)

            

            
            this.Ob_center.data.materials.clear()
            this.Ob_center.data.materials.append(bpy.data.materials[0])
            
            this.Ob_scaf.data.materials.clear()
            this.Ob_scaf.data.materials.append(bpy.data.materials[2])
            
            this.Ob_link.data.materials.clear()
            this.Ob_link.data.materials.append(bpy.data.materials[1])

        #this.Ob_scaf.name = 'Scaf'  + str(this.sid)
        #this.Ob_scaf.name = 'Scaf' 
        #this.Ob_link.name = 'Link_' + str(this.sid)
        #print(this.Ob_scaf)




    



