import bpy
from mathutils import Vector

import shutil, os

class RenderCad: 

    Helices = None

    y = 0
    z = 0
    vertices = 3

    BaseRibbon = None


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



    def RenderStrand(this, Lista):
        ### Function that renders the strand as a ribbon
        print("Rendering strand")


    def createSpline(this, coords_list, resolution, closed):
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '3D'
        # make a new spline in that curve
        spline = crv.splines.new(type='BEZIER')
        #spline.use_endpoint_u = True
        #spline.use_bezier_u = True
        

        if closed: 
            spline.use_cyclic_u = True
        
        
        # a spline point for each point
        spline.bezier_points.add(len(coords_list)-1) # theres already one point by default

        prevL = coords_list[0]

        prev = None

        First = False

        # assign the point coordinates to the spline points
        for p, new_co in zip(spline.bezier_points, coords_list):
            p.co = (new_co ) # (add nurbs weight)
            p.handle_left = p.handle_right = p.co

            if prev != None:
                left = ( (prevL[0] + new_co[0]) / 2, (prevL[1] + new_co[1]) / 2, (prevL[2] + new_co[2]) / 2)
                prev.handle_right = left
                p.handle_left = left

                if First == False:
                    prev.handle_right = left
            
            

            prev = p
            prevL = new_co

            




            
            




        # make a new object with the curve
        obj = bpy.data.objects.new('object_name', crv)

        spline.order_u = resolution

        return obj
    

    def RenderRibbons(this):
        ### Function that will create a set of ribbons
        ### To me shown as the scaffold and staples
        print("Rendering ribbons")

        ### This will create Ribbons
        ## First, the base Ribbon

        stpInd = 1

        depth = 0.5
        res = 4

        b = 0.5
        h = 0.5
        coord1 = [ [0,0,0], [0, b, 0], [h, b , 0], [h, 0, 0] ]
        obj1 = this.createSpline( coord1, 4, True )

        bpy.context.scene.collection.objects.link(obj1)


        ### Create the Scaffold:
        SC_Coord = []

        

        for BP in this.Helices.getElements() :
            ### Basically, just draw them
            P = BP.getPosScaffold()
            C = [  P[0], P[1], P[2] ]
            SC_Coord.append( C )

        obj2 = this.createSpline(SC_Coord, 2, False)         
        bpy.context.scene.collection.objects.link(obj2)
        #obj2.data.bevel_object = obj1
        obj2.data.bevel_depth = depth
        obj2.data.bevel_resolution = res


        bpy.data.objects[-1].data.materials.append(bpy.data.materials[0])
        #obj2.data.twist_mode = 'Z_UP'

        ### Scaffold created

        for staplec in this.Helices.getStapleList():
            
            if staplec.isEnabled():
                Listas = []
                Listas.append(staplec.getFirstStrand())
                Listas.append(staplec.getSecondStrand())

                for lista in Listas :
                    coordN = []
                    
                    BP = lista[0]
                    BP2 = BP.getNext()
                    this.addIntermediate(BP, BP2, coordN)
                    
                    for BP in lista :
                        ### Basically, just draw them
                        P = BP.getPosStp()
                        C = [  P[0], P[1], P[2] ]
                        coordN.append( C )
                    
                    BP = lista[-1]
                    BP2 = BP.getPrev()
                    this.addIntermediate(BP, BP2, coordN)

                    objN = this.createSpline(coordN, 3, False)         
                    bpy.context.scene.collection.objects.link(objN)
                    objN.data.bevel_depth = depth
                    objN.data.bevel_resolution = res
                    bpy.data.objects[-1].data.materials.append(bpy.data.materials[stpInd])

                    stpInd += 1

                    if stpInd == 4:
                        stpInd = 1

                    #objN.data.bevel_object = obj1
                    #objN.data.twist_mode = 'Z_UP'


    def addIntermediate (this, BP1, BP2, coordN):
        if BP1 != None and BP2 != None :
            P = BP1.getPosStp()
            P2 = BP2.getPosStp()
            C = [  (P[0]+P2[0])/2, (P[1]+P2[1])/2, (P[2]+P2[2]/2) ]
            coordN.append( C )


    def RenderPDF(this, filename):

        Exito = False
        
        try:
            print ("Rendering in asymptote")
            g = asy()
            print("Executing...")
            g.send("import settings")
            g.send('outformat="pdf"')
            g.send('interactiveView=false')
            

            g.size(300)
            g.send("draw(unitsquare)")
            g.fill("unitsquare, blue")
            g.clip("unitcircle")
            g.label("\"$O$\", (0,0), SW")
            
            g.finish()

            
            Exito = True

        
        except:
            print ("Error running asymptote")

        
        if Exito :
            ## Move file to user location
            try:
                filepath = bpy.path.abspath("//"+filename)
                
                shutil.move("out.pdf", filepath)
                print("Output file located in: " + filepath)
            except:
                print("Error moving file. Check your home folder")
                    






    
    





