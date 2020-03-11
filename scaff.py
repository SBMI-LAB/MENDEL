import bpy
from math import *

class Scaff():
    name = "name"
    sid = 0
    r_id = 0
    p_id = 0
    
    pSep = 0.7
    
    sSep = 1
    
    Ob_center = None
    Ob_scaf = None
    Ob_link = None
    
    Prev = None
    Next = None
    
    PrevStp = None
    NextStp = None
    
    StapleObj = None
    
    x, y, z = 0,0,0

    sx,sy, sz = 0,0,0

    lx,ly,lz = 0,0,0
    
    ox,oy,oz = 0,0,0

    ang = 0
    
    mode = "Final"
    
    geom = False
    
    rodnumber = 0
    posinrod = 0
    
    # ~ asigned = 0


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



    def setTurn(this, P) :
        ### Transform the position and rotate it
        if this.getPrev() != None :
            G = this.Prev.getXYZ()
            this.x = G[0]
            this.y = G[1]
            this.z = G[2]

            
            if P == 270:
                this.y += -2
            
            if P == 90:
                this.y += 2

            if P == 0: 
                this.z += -2
            
            if P == 180:
                this.z += 2

            
            this.ox += 720/21


            if this.oz == 0 or this.oz == 360:
                this.oz = 180
            else:
                this.oz = 0
            
            this.updatePos()



    def updatePos (this):
        ### Will update positions of scaffold and stapples
        ### According to the xyz coordinates 
        ### and the orientations
        if this.oz == 0 or this.oz == 360:
            ## perform direct rotation
            #print ("Case 1")
            ### check ox and rotate against it
            this.sy = this.pSep*sin(this.ox*radians(180)/180)
            this.sz = -this.pSep*cos(this.ox*radians(180)/180)

            this.ly = -this.sSep*sin(this.ox*radians(180)/180)
            this.lz = this.sSep*cos(this.ox*radians(180)/180)

            #print("z: " + str(this.sz) + " ang: " + str(this.ox))

        else:
            ## perform opposit rotation
            #print ("Case 2")
            this.sy = -this.pSep*sin(this.ox*radians(180)/180)
            this.sz = this.pSep*cos(this.ox*radians(180)/180)

            this.ly = this.sSep*sin(this.ox*radians(180)/180)
            this.lz = -this.sSep*cos(this.ox*radians(180)/180)


        this.sx = this.x
        this.sy += this.y
        this.sz += this.z

        this.lx = this.x
        this.ly += this.y
        this.lz += this.z    


        this.updateElements()        

    
    def getNextStp(this):
        return this.NextStp
    
    def setNextStp(this,N):
        this.NextStp = N

    def getPrevStp(this):
        return this.PrevStp
    
    def setPrevStp(this,N):
        this.PrevStp = N
    
    def setR (this, n):
        this.rodnumber = n
        #print(this.rodnumber)
    
    def setRod(this,n, pos):
        this.rodnumber = n
        this.posinrod = pos
    
    def getPosStp(this):
        P = Vector( (this.lx, this.ly, this.lz) )
        return P
        #return this.Ob_link.matrix_world.to_translation()
    
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
    
      
    def SetPrev(this, Prev):
        
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

            

            this.Prev = Prev
            Prev.SetNext(this)
        


    def getXYZ(this):
        P = (this.x, this.y, this.z)
        return P

    def getX(this):
        return this.x

    def SetNext(this, Next):
        this.Next = Next

        Next.SetZAng(this.oz)
        Next.SetXAng(this.ox)  
    
        this.updatePos()
    
    
    def SetXAng (this,ang):
        
        
        #if this.oz == 0 :
        this.ox = ang+this.ang
        #else:
        #    this.ox = ang - this.ang
            

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




    



