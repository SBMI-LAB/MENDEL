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
            bpy.context.active_object.name = 'object_name'


    def compareX (this, x1, x2):
        ### Compare if they are neighbors

        D = abs(x1-x2)
        if D == 1:
            return True
        else:
            return False    

    
    def RenderCylinders(this, vertices=5):
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



    def RenderStrand(this, SC_Coord, mat):
        ### Function that renders the strand as a ribbon
        print("Rendering strand")


        depth = 0.5
        res = 4

        obj2 = this.createSpline(SC_Coord, 2, False)         
        bpy.context.scene.collection.objects.link(obj2)
        #obj2.data.bevel_object = obj1
        obj2.data.bevel_depth = depth
        obj2.data.bevel_resolution = res
        
        bpy.data.objects[-1].data.materials.append(bpy.data.materials[mat])
        obj2.data.twist_mode = 'Z_UP'


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

        PC = None

        for BP in this.Helices.getElements() :
            ### Basically, just draw them
            P = BP.getPosScaffold()
            C = [  P[0], P[1], P[2] ]

            if PC == None:
                PC = C

            if abs(PC[0] - C[0]) > 1:
                ### Create a scaffold
                this.RenderStrand(SC_Coord,0)
                SC_Coord.clear()

            PC = C

            SC_Coord.append( C )



        this.RenderStrand(SC_Coord,0)
        """
        obj2 = this.createSpline(SC_Coord, 2, False)         
        bpy.context.scene.collection.objects.link(obj2)
        #obj2.data.bevel_object = obj1
        obj2.data.bevel_depth = depth
        obj2.data.bevel_resolution = res
        bpy.data.objects[-1].data.materials.append(bpy.data.materials[0])
        #obj2.data.twist_mode = 'Z_UP'


        """
        ### Scaffold created
        

        for staplec in this.Helices.getStapleList():
            
            if staplec.isEnabled():
                Listas = []
                Listas.append(staplec.getFirstStrand())
                Listas.append(staplec.getSecondStrand())

                for lista in Listas :
                    if len(lista) > 0:
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
            C = [  (P[0]+P2[0])/2, (P[1]+P2[1])/2, (P[2]+P2[2])/2 ]
            coordN.append( C )


    def renderAsyStrand(this, g, Coords, mat):
        ### Try to create a path with the current strand
        ### it is a 2D projection. What matters here?
        print("Rendering asy strand")
        
        material = ["blue", "red", "lightolive", "green"]

        LBP = None

        dy = 1

        scale = 10

        PP = "draw("
        Initial = True
        for EL in Coords:
            if Initial == False:
                PP = PP + " -- "

            C = EL[0]

            C[0] = C[0] + dy

            BP = EL[1]
            LBP = BP

            BPC =  BP.getXYZCenter()[1]
            #print (BP)
            RD = BP.getRod()

            CT = C[1]
            
            if C[1] > BPC:
                C[1] =  -1
                CT =   1
            else:
                C[1] =  1
                CT =  - 1
            

            C[1] = C[1] + RD*4
            CT = CT + RD*4

            C[0] = C[0] * scale
            C[1] = C[1] * scale
            CT = CT * scale

            PP = PP + "(" + str(C[1]) + "," + str(C[0]) + ")"

            if mat == 0:
                PP = PP + "--(" + str(CT) + "," + str(C[0]) + ")" + "--(" + str(C[1]) + "," + str(C[0]) + ")"


            Initial = False
        PP = PP + ", marker=MarkFill[0], "+str(material[mat])+");"

        g.send(PP)

        if LBP != None:
            ## Print label
            R = LBP.getRod()*4*scale
            x = -round( LBP.getXYZCenter()[1]/2 )
            z = round(LBP.getXYZCenter()[2]/2)
            
            if mat == 0:
                g.send("defaultpen(fontsize(0.1pt));")
                Tt = 'label("(' + str(z)+ ','+ str(x) + ')" , ('+str(R)+',0));' 
                g.send(Tt)





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


            #g.send("draw(unitsquare)")
            #g.fill("unitsquare, blue")
            #g.clip("unitcircle")
            #g.label("\"$O$\", (0,0), SW")

            ### Starting picture
            
            #Starting scaffolds
            SC_Coord = []

            PC = None

            for BP in this.Helices.getElements() :
                ### Basically, just draw them


                P = BP.getPosScaffold()

                Ps = BP.getPosStp()


                C = [  P[0], P[1], P[2] ]

                #LL = "draw(("+str(-P[1]) + "," +str(P[0])+ ")--(" + str(-Ps[1])+","+str(Ps[0])+"), marker=MarkFill[0]);"
                #g.send(LL)

                if PC == None:
                    PC = C

                if abs(PC[0] - C[0]) > 1:
                    ### Create a scaffold
                    this.renderAsyStrand(g, SC_Coord,0)
                    SC_Coord.clear()

                PC = C
                CP = [C, BP]

                SC_Coord.append( CP )
            this.renderAsyStrand(g, SC_Coord,0)
            #End scaffolds

            print("End scaffolds")


            print("Start staples")
            stpInd = 1

            for staplec in this.Helices.getStapleList():
                
                if staplec.isEnabled():
                    Listas = []
                    Listas.append(staplec.getFirstStrand())
                    Listas.append(staplec.getSecondStrand())

                    for lista in Listas :
                        if len(lista) > 0:
                            coordN = []
                            
                            BP = lista[0]
                            BP2 = BP.getNext()
                            #this.addIntermediate(BP, BP2, coordN)
                            
                            for BP in lista :
                                ### Basically, just draw them

                                P = BP.getPosStp()
                                C = [  P[0], P[1], P[2] ]
                                CP = [ C, BP ]
                                coordN.append( CP )
                            
                            BP = lista[-1]
                            BP2 = BP.getPrev()

                            this.renderAsyStrand(g, coordN,stpInd)
                            #this.addIntermediate(BP, BP2, coordN)

                            stpInd += 1

                            if stpInd == 4:
                                stpInd = 1


            print("End staples")
            
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
    

    def RenderPDF2(this, filename):

        Exito = False
        
        try:
            print ("Rendering in asymptote")
            g = asy()
            print("Executing...")
            g.send("import settings")
            g.send('outformat="pdf"')
            g.send('interactiveView=false')
            

            g.size(300)

            Prev = None

            for BP in this.Helices.getElements() :
                
                
                ## Render BP
                if Prev != None:
                    ## Set the points. 
                    if Prev.getNext() == BP :
                        ## Render scaffold
                        Py1 = Prev.getX()
                        Py2 = BP.getX()
                        Px1 = Prev.getRod()*4
                        Px2 = BP.getRod()*4
                        comm = "draw( ("+str(Px1)+","+str(Py1)+") -- (" + str(Px2)+ "," + str(Py2) + "),  blue)"
                        g.send(comm)

                    # Render joint
                    Py1 = BP.getX()
                    Px1 = BP.getRod()*4
                    Py2 = Py2
                    Px2 = Px1+1
                    comm = "draw( ("+str(Px1)+","+str(Py1)+") -- (" + str(Px2)+ "," + str(Py2) + "),  black)"
                    g.send(comm)

                    ## Render staple
                    if BP.getPrevStp() != None :
                        NT = BP.getPrevStp()
                        Py1 = NT.getX()
                        Px1 = NT.getRod()*4 + 1
                        comm = "draw( ("+str(Px1)+","+str(Py1)+") -- (" + str(Px2)+ "," + str(Py2) + "), red)"
                        g.send(comm)




                Prev = BP


            
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
                    

    def renderSC(this, g, scList):
        
        dy = 1
        scale = 10
        RDS = 6
        
        ## Prepare staples:
        salida = "draw("
        salida2 = "draw("
        First = False
        for BP in scList:
            if First == True:
                salida += "--"
                salida2 += "--"
            ### Adding list of elements, just coordinates
            C = BP.getXYZCenter()
            C2 = BP.getRod()
            Y = C[0] + dy
            X = C2*RDS - 1
            X2 = X + 2
            X = X*scale
            X2 = X2*scale
            Y = Y*scale
            salida += "("+str(X) + ","+str(Y) + ")"
            salida2 += "("+str(X2) + ","+str(Y) + ")"
            First = True


            ### Check prev staple:
            stap = BP.getPrevStp()
            
            if stap != None:
                if stap.getRod() != BP.getRod():
                    ## It's different!
                    R = str(stap.getRod()) + "/"  + str(stap.getX())
                    ststring = "draw(("+str(X2) + ","+str(Y) + ")--("+str(X2+4) + ","+str(Y) + "),red)" 
                    
                    ststring2 = 'label("'+R+'" , ('+str(X2+4) + ","+str(Y) +'),align=E);' 
                    g.send(ststring)
                    g.send(ststring2)

            stap = BP.getNextStp()
            if stap != None:
                if stap.getRod() != BP.getRod():
                    R = str(stap.getRod()) + "/"  + str(stap.getX()) 
                    ## It's different!
                    ststring = "draw(("+str(X2) + ","+str(Y) + ")--("+str(X2+4) + ","+str(Y) + "),red)" 
                    ststring2 = 'label("'+R+'" , ('+str(X2+4) + ","+str(Y) +'),align=E);' 
                    g.send(ststring)
                    g.send(ststring2)




        salida += ",marker=MarkFill[0],blue)"
        salida2 += ",marker=MarkFill[0],red)"
        g.send(salida)
        g.send(salida2)




        BP = scList[-1]
        R = BP.getRod()
        C = BP.getXYZCenter()
        y = round(-C[1]/2)
        z = round(C[2]/2)

        g.send("defaultpen(fontsize(0.1pt));")
        
        Tt = 'label("(' + str(z)+ ','+ str(y) + ')" , ('+str(R*RDS*scale)+',9));' 
        g.send(Tt)
        Tt = 'label("Helix '+str(R)+'" , ('+str(R*RDS*scale)+',0));' 
        g.send(Tt)



        





    def RenderPDF3(this, filename):

        Exito = False
        
        try:
            print ("Rendering in asymptote")
            g = asy()
            print("Executing...")
            g.send("import settings")
            g.send('outformat="pdf"')
            g.send('interactiveView=false')
            

            g.size(300)

            scList = []
            stList = []

            for BP in this.Helices.getElements() :
                Added = False
                Prev = BP.getPrev() 
                if Prev != None:
                    if Prev.getRod() == BP.getRod() :
                        scList.append(BP)
                        Added = True

                if Added == False:
                    if len(scList) > 0 :
                        this.renderSC(g, scList)
                        scList.clear()
                        
                        scList.append(BP)


            if len(scList) > 0: 
                this.renderSC(g, scList)

            
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
                    


    
    





