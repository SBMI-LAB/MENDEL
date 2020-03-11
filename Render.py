import bpy
from mathutils import Vector

class RenderCad: 

    Helices = None

    y = 0
    z = 0
    vertices = 3


    def setHelices(this, helices):
        this.Helices = helices

    def Generate(this, xini, xfin):

        L = abs(xini-xfin)
        xpos = min((xini,xfin))
        #print ("Xinit: " + str(xini) + "  Xfin: " + str(xfin))

        xpos = xpos + L/2

        if L > 0 :
            
            #print("Creating cylinder of L : " + str(L) )

            bpy.ops.mesh.primitive_cylinder_add(vertices=this.vertices, radius = 1, depth = L, location=(xpos,-this.y,this.z), rotation=(0,radians(90),0))


    def compareX (this, x1, x2):
        ### Compare if they are neighbors

        D = abs(x1-x2)
        if D == 1:
            return True
        else:
            return False    

    
    def RenderCylinders(this, vertices):
        ## Should generate cilinders in blender
        print("Rendering...")

        this.vertices = vertices

        x = 0

        for row in this.Helices.getHelices():

            ### This will start a new rod
            this.y = 2*row.getY()
            this.z = 2*row.getZ()

            Prev = None

            xinit = -1
            xfin = -1

            xprev = -1

            Rod = -1

            for BP in row.getRow():
                
                if type(BP) != type([]) :

                    genera = False

                    x = BP.getX()

                    R = BP.getRod()


                    if R != Rod or this.compareX(x,xprev) == False:
                        genera = True
                    else:
                        if xinit < 0:
                            xinit = x
                        xinit = min( ( xinit, x ) )
                        xfin = max ( (xfin, x) )
                        #print("comparing.." + str(xinit) + " ,  " + str(xfin) + "  Rod: "+ str(Rod))
                        #else:                         


                        #print("comparing.." + str(xinit) + " ,  " + str(xfin) + "  Rod: "+ str(Rod))

                    Rod = R
                    xprev = x

                    if genera :
                        #print("Generating: " + str(xinit) + ", " + str(xfin))
                        if xinit >= 0 and xfin >= 0 :

                            this.Generate(xinit, xfin)

                        xinit = x
                        xfin = x

                            #xinit = -10
                            #xfin = -10
            this.Generate(xinit,xfin)








