#Alien Trilogy model obj/mtl generator script by Bobblen
model_file_name="M00"
map_texture_mesh_file_name_00="BX00"
map_texture_mesh_file_name_01="BX01"
map_texture_mesh_file_name_02="BX02"
map_texture_mesh_file_name_03="BX03"
map_texture_mesh_file_name_04="BX04"

#open all the texture mesh files and extract the total texture count from each one
#for each new file we must add the count to the previous total, as the texture indexes carry over all files
with open(map_texture_mesh_file_name_00, 'rb') as inBX00, open(map_texture_mesh_file_name_01, 'rb') as inBX01, open(map_texture_mesh_file_name_02, 'rb') as inBX02, open(map_texture_mesh_file_name_03, 'rb') as inBX03, open(map_texture_mesh_file_name_04, 'rb') as inBX04:
    inBX00.seek(8)
    texcountBX00raw = inBX00.read(2)
    texcountBX00 = int.from_bytes(texcountBX00raw, byteorder='little')
    
    inBX01.seek(8)
    texcountBX01raw = inBX01.read(2)
    texcountBX01 = int.from_bytes(texcountBX01raw, byteorder='little') + texcountBX00
    
    inBX02.seek(8)
    texcountBX02raw = inBX02.read(2)
    texcountBX02 = int.from_bytes(texcountBX02raw, byteorder='little') + texcountBX01
    
    inBX03.seek(8)
    texcountBX03raw = inBX03.read(2)
    texcountBX03 = int.from_bytes(texcountBX03raw, byteorder='little') + texcountBX02
    
    inBX04.seek(8)
    texcountBX04raw = inBX04.read(2)
    texcountBX04 = int.from_bytes(texcountBX04raw, byteorder='little') + texcountBX03

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
    
    inBX01.seek(10)
    while(x<texcountBX01):

        #read raw bytes
        xposraw = inBX01.read(1)
        yposraw = inBX01.read(1)
        xsizeraw = inBX01.read(1)
        ysizeraw = inBX01.read(1)
        unknown1 = inBX01.read(1)
        unknown2 = inBX01.read(1)
    
        #Extract UV
        xpos = int.from_bytes(xposraw, byteorder='little')
        ypos = int.from_bytes(yposraw, byteorder='little')
        xsize = int.from_bytes(xsizeraw, byteorder='little') + 1
        ysize = int.from_bytes(ysizeraw, byteorder='little') + 1      
        #calculate and normalise UV
        uvcoord1x = xpos / 256
        uvcoord1y = ((256-ypos)-ysize) / 256
        uvcoord2x = (xpos+xsize) / 256
        uvcoord2y = ((256-ypos)-ysize) / 256
        uvcoord3x = (xpos+xsize) / 256
        uvcoord3y = (256-ypos) / 256
        uvcoord4x = xpos / 256
        uvcoord4y = (256-ypos) / 256
        
        #extract material
        material_name = "TP01"
        materialdict["Index{0}".format(str(x))] = x 
        materialdict["Material{0}".format(str(x))] = material_name
        
        #add to UV dictionary if not exists
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
        
    inBX02.seek(10)
    while(x<texcountBX02):

        #read raw bytes
        xposraw = inBX02.read(1)
        yposraw = inBX02.read(1)
        xsizeraw = inBX02.read(1)
        ysizeraw = inBX02.read(1)
        unknown1 = inBX02.read(1)
        unknown2 = inBX02.read(1)
    
        #Extract UV
        xpos = int.from_bytes(xposraw, byteorder='little')
        ypos = int.from_bytes(yposraw, byteorder='little')
        xsize = int.from_bytes(xsizeraw, byteorder='little') + 1
        ysize = int.from_bytes(ysizeraw, byteorder='little') + 1      
        #calculate and normalise UV
        uvcoord1x = xpos / 256
        uvcoord1y = ((256-ypos)-ysize) / 256
        uvcoord2x = (xpos+xsize) / 256
        uvcoord2y = ((256-ypos)-ysize) / 256
        uvcoord3x = (xpos+xsize) / 256
        uvcoord3y = (256-ypos) / 256
        uvcoord4x = xpos / 256
        uvcoord4y = (256-ypos) / 256
        
        #extract material
        material_name = "TP02"
        materialdict["Index{0}".format(str(x))] = x 
        materialdict["Material{0}".format(str(x))] = material_name
        
        #add to UV dictionary if not exists
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
        
    inBX03.seek(10)
    while(x<texcountBX03):

        #read raw bytes
        xposraw = inBX03.read(1)
        yposraw = inBX03.read(1)
        xsizeraw = inBX03.read(1)
        ysizeraw = inBX03.read(1)
        unknown1 = inBX03.read(1)
        unknown2 = inBX03.read(1)
    
        #Extract UV
        xpos = int.from_bytes(xposraw, byteorder='little')
        ypos = int.from_bytes(yposraw, byteorder='little')
        xsize = int.from_bytes(xsizeraw, byteorder='little') + 1
        ysize = int.from_bytes(ysizeraw, byteorder='little') + 1      
        #calculate and normalise UV
        uvcoord1x = xpos / 256
        uvcoord1y = ((256-ypos)-ysize) / 256
        uvcoord2x = (xpos+xsize) / 256
        uvcoord2y = ((256-ypos)-ysize) / 256
        uvcoord3x = (xpos+xsize) / 256
        uvcoord3y = (256-ypos) / 256
        uvcoord4x = xpos / 256
        uvcoord4y = (256-ypos) / 256
        
        #extract material
        material_name = "TP03"
        materialdict["Index{0}".format(str(x))] = x 
        materialdict["Material{0}".format(str(x))] = material_name
        
        #add to UV dictionary if not exists
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
    
    inBX04.seek(10)
    while(x<texcountBX04):

        #read raw bytes
        xposraw = inBX04.read(1)
        yposraw = inBX04.read(1)
        xsizeraw = inBX04.read(1)
        ysizeraw = inBX04.read(1)
        unknown1 = inBX04.read(1)
        unknown2 = inBX04.read(1)
    
        #Extract UV
        xpos = int.from_bytes(xposraw, byteorder='little')
        ypos = int.from_bytes(yposraw, byteorder='little')
        xsize = int.from_bytes(xsizeraw, byteorder='little') + 1
        ysize = int.from_bytes(ysizeraw, byteorder='little') + 1      
        #calculate and normalise UV
        uvcoord1x = xpos / 256
        uvcoord1y = ((256-ypos)-ysize) / 256
        uvcoord2x = (xpos+xsize) / 256
        uvcoord2y = ((256-ypos)-ysize) / 256
        uvcoord3x = (xpos+xsize) / 256
        uvcoord3y = (256-ypos) / 256
        uvcoord4x = xpos / 256
        uvcoord4y = (256-ypos) / 256
        
        #extract material
        material_name = "TP04"
        materialdict["Index{0}".format(str(x))] = x 
        materialdict["Material{0}".format(str(x))] = material_name
        
        #add to UV dictionary if not exists
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
        
        #texflag = 11, flip 180
        if texflag==11: #flip texture 180
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
        print("usemtl " + materialdict[materialname] + "\nf " + str(xquad) + texquadx + " " + str(yquad) + texquady + " " + str(zquad) + texquadz + " " + str(wquad) + texquadw)
            
        z=z+1
        
print("\nAlien Trilogy DOS Model Header Reader\n" + "\nmodel file name is " + model_file_name
+ "\nvertex count (decimal) " + str(vertcount) + "\nface count (decimal) " + str(quadcount)  + "\nfaces start offset (decimal) " + str(quadstart) + "\nfaces end offset (decimal) " + str(quadend)
+ "\nvertex start offset (decimal) " + str(vertstart) + "\nvertex end offset (decimal) " + str(vertend))

print("\nbin2obj.exe " + model_file_name + " -soff " + str(vertstart) + " -eoff " + str(vertend) + " -stri 2 -vtyp 1") #-fsof " + str(quadstart) + " -feof " + str(quadend) + " -fstr 4 -ftyp 1 -fquad")
        
