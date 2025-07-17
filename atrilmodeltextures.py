#Alien Trilogy model obj/mtl generator script by Bobblen
model_file_name="OPTM000"
model_texture_mesh_file_name_00="OPTBX00"

#open the texture mesh files and extract the total texture count
with open(model_texture_mesh_file_name_00, 'rb') as inBX00:
    inBX00.seek(8)
    texcountBX00raw = inBX00.read(2)
    texcountBX00 = int.from_bytes(texcountBX00raw, byteorder='little')

    x=0 #initialise counter, this will also double up as our identifier for each texture
    uvcoordcount=1
    uvcoordsdict={} #initialise UV coordinate dictionary
    materialdict={} #initialise material dictionary

    inBX00.seek(10)
    while(x<texcountBX00):

        #read raw bytes
        xposraw = inBX00.read(1)
        yposraw = inBX00.read(1)
        xsizeraw = inBX00.read(1)
        ysizeraw = inBX00.read(1)
        unknown1 = inBX00.read(1)
        unknown2 = inBX00.read(1)
    
        #Extract UV info
        xpos = int.from_bytes(xposraw, byteorder='little')
        ypos = int.from_bytes(yposraw, byteorder='little')
        xsize = int.from_bytes(xsizeraw, byteorder='little') + 1
        ysize = int.from_bytes(ysizeraw, byteorder='little') + 1      
        #calculate UV coords and normalise (total texture size hard coded to 256 for now)
        #note the y coord starts at the top left in Alien Trilogy, so we subtract to move it to the bottom left
        uvcoord1x = xpos / 256
        uvcoord1y = ((256-ypos)-ysize) / 256
        uvcoord2x = (xpos+xsize) / 256
        uvcoord2y = ((256-ypos)-ysize) / 256
        uvcoord3x = (xpos+xsize) / 256
        uvcoord3y = (256-ypos) / 256
        uvcoord4x = xpos / 256
        uvcoord4y = (256-ypos) / 256
        
        #extract material info
        material_name = "TP00"
        materialdict["Index{0}".format(str(x))] = x 
        materialdict["Material{0}".format(str(x))] = material_name
        
        #add to UV dictionary but only if it doesn't already exist
        if "vt " + str(uvcoord1x) + " " + str(uvcoord1y) in uvcoordsdict.keys():
            materialdict["UVone{0}".format(str(x))] = uvcoordsdict.get("vt " + str(uvcoord1x) + " " + str(uvcoord1y))
        else:
            uvcoordsdict["vt " + str(uvcoord1x) + " " + str(uvcoord1y)] = uvcoordcount
            materialdict["UVone{0}".format(str(x))] = uvcoordcount
            uvcoordcount = uvcoordcount + 1          
        if "vt " + str(uvcoord2x) + " " + str(uvcoord2y) in uvcoordsdict.keys():
            materialdict["UVtwo{0}".format(str(x))] = uvcoordsdict.get("vt " + str(uvcoord2x) + " " + str(uvcoord2y)) 
        else:
            uvcoordsdict["vt " + str(uvcoord2x) + " " + str(uvcoord2y)] = uvcoordcount
            materialdict["UVtwo{0}".format(str(x))] = uvcoordcount
            uvcoordcount = uvcoordcount + 1
        if "vt " + str(uvcoord3x) + " " + str(uvcoord3y) in uvcoordsdict.keys():
            materialdict["UVthree{0}".format(str(x))] = uvcoordsdict.get("vt " + str(uvcoord3x) + " " + str(uvcoord3y))
        else:
            uvcoordsdict["vt " + str(uvcoord3x) + " " + str(uvcoord3y)] = uvcoordcount
            materialdict["UVthree{0}".format(str(x))] = uvcoordcount
            uvcoordcount = uvcoordcount + 1
            
        if "vt " + str(uvcoord4x) + " " + str(uvcoord4y) in uvcoordsdict.keys():
            materialdict["UVfour{0}".format(str(x))] = uvcoordsdict.get("vt " + str(uvcoord4x) + " " + str(uvcoord4y))
        else:
            uvcoordsdict["vt " + str(uvcoord4x) + " " + str(uvcoord4y)] = uvcoordcount
            materialdict["UVfour{0}".format(str(x))] = uvcoordcount
            uvcoordcount = uvcoordcount + 1

        
        x=x+1
      
#print material library header
print("mtllib Materials\\" + str(model_file_name) + ".mtl")
#print uv
for keys in uvcoordsdict.keys():
    print(keys)

#now extract the faces from the extracted M00 file
with open(model_file_name, 'rb') as inMOD:
    inMOD.seek(20)
    quadcountraw = inMOD.read(2)
    quadcount = int.from_bytes(quadcountraw, byteorder='little')
    unknown1=inMOD.read(1)
    unknown2=inMOD.read(1)
    
    quadstart=28
    quadend = (quadstart-1) + (quadcount*20) - 2
    
    vertcountraw = inMOD.read(2)
    unknown3=inMOD.read(1)
    unknown4=inMOD.read(1)
    vertcount = int.from_bytes(vertcountraw, byteorder='little')

    vertstart = quadend + 3
    vertend = vertstart + (vertcount*8) - 2
    
    z=0 #initialise counter
    
    inMOD.seek(quadstart)
    while (z<quadcount):
        xquadraw = inMOD.read(4)
        yquadraw = inMOD.read(4)
        zquadraw = inMOD.read(4)
        wquadraw = inMOD.read(4)
        texquadraw = inMOD.read(2) #the index of the texture in the BXfile, we can use this to look up the material and UV using our dictionaries
        texflagraw = inMOD.read(1)
        unknown2 = inMOD.read(1)
        
        xquad = int.from_bytes(xquadraw, byteorder='little') + 1
        yquad = int.from_bytes(yquadraw, byteorder='little') + 1
        zquad = int.from_bytes(zquadraw, byteorder='little') + 1
        wquad = int.from_bytes(wquadraw, byteorder='little') + 1
        texquad = int.from_bytes(texquadraw, byteorder='little')
        texflag = int.from_bytes(texflagraw, byteorder='little')
        
        materialindex="Index" + str(texquad)
        materialname="Material" + str(texquad)
        UVone="UVone" + str(texquad)
        UVtwo="UVtwo" + str(texquad)
        UVthree="UVthree" + str(texquad)
        UVfour="UVfour" + str(texquad)
        
        #texflag = 2, triangle? not always
        #texflag = 4, transparency?
        #texflag = 11, flip 180
        #texflag = 128 ?
        if texquad>x-1: #no texture if texture index is out of range
            texquadx = ""
            texquady = ""
            texquadz = ""
            texquadw = ""
        elif texflag==2: #flag=2 triangle?
            texquadx = "/" + str(materialdict[UVone])
            texquady = "/" + str(materialdict[UVthree])
            texquadz = "/" + str(materialdict[UVfour])
            texquadw = ""
        elif texflag==11: #flip texture 180
            texquadx = "/" + str(materialdict[UVtwo])
            texquady = "/" + str(materialdict[UVone])
            texquadz = "/" + str(materialdict[UVfour])
            texquadw = "/" + str(materialdict[UVthree])
        else:
            texquadx = "/" + str(materialdict[UVone])
            texquady = "/" + str(materialdict[UVtwo])
            texquadz = "/" + str(materialdict[UVthree])
            texquadw = "/" + str(materialdict[UVfour])
        
        #some faces are triangles, not quads. These set the w coord as 0xff in the game but we clear them for the obj file.
        if wquad == 4294967296:
            wquad=""
            texquadw=""
        
        #print faces
        if texquad<x:
            print("usemtl " + materialdict[materialname]) 
        else:
            print("usemtl TPxx") #texture index out of range, assign a dummy material for now
            
        print("f " + str(xquad) + texquadx + " " + str(yquad) + texquady + " " + str(zquad) + texquadz + " " + str(wquad) + texquadw)
            
        z=z+1
        
print("\nAlien Trilogy DOS Model Header Reader\n" + "\nmodel file name is " + model_file_name
+ "\nvertex count (decimal) " + str(vertcount) + "\nface count (decimal) " + str(quadcount)  + "\nfaces start offset (decimal) " + str(quadstart) + "\nfaces end offset (decimal) " + str(quadend)
+ "\nvertex start offset (decimal) " + str(vertstart) + "\nvertex end offset (decimal) " + str(vertend))

#bin2obj extract command
print("\nbin2obj.exe " + model_file_name + " -soff " + str(vertstart) + " -eoff " + str(vertend) + " -stri 2 -vtyp 1") 
#-fsof " + str(quadstart) + " -feof " + str(quadend) + " -fstr 4 -ftyp 1 -fquad")
        
