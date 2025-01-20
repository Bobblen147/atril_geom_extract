# Alien Trilogy DOS Geometry Extraction Python Scripts
These Python scripts will read the header of an Alien Trilogy DOS map or model file and determine the offsets required to extract geometry to the wavefront obj format. It does not do the extraction itself but instead generates some useful information and a command line to be used with another tool, Bin2Obj by Mark E Sowden. The command line can be used directly with Bin2Obj as is or the information used in other programs.

If you provide the appropriate textures and texture mesh files, the script will also generate the UV co-ordinates and materials to allow you to load those textures in your 3d modeling program on choice (tested only in Blender for now)

These scripts are very bare bones, and have had little testing. Use at your own risk.

## Credits
This script is 99% based on the documentation of the Alien Trilogy map and model format reverse engineered by Lex Safonov and available on the Xentax wiki here (https://web.archive.org/web/20230518104117/https://wiki.xentax.com/index.php/Alien_Trilogy_MAP)
(https://web.archive.org/web/20230518104114/https://wiki.xentax.com/index.php/Alien_Trilogy_BND)
I have done a small amount of additional research on the texture mesh files to support map textures.

Bin2Obj is authored by Mark E Sowden who is not involved with this particular project in any way. He just happened to have written a compact binary obj extractor that supported quads and which I happened to stumble across when looking at Alien Trilogy.
(https://github.com/hogsy/Bin2Obj)


## Usage
To use just run either atrilmaptextures.py or atrilmodeltextures.py with the appropriate files in the same folder.
It can be helpful to pipe to a file due to the amount of data generated. e.g. atrilmaptextures.py > output.txt
The output should be pasted into an obj file (which you can generate using bin2obj) overwriting the faces

The scripts require a small amount of modification to work. They currently assume your files are in the same folder as the scripts themselves.

The map_file_name field at the top of the map script is the name of your .map file (e.g. L111LEV.MAP for map 1, Entrance)

The model_file_name field at the top of the model script is a little different, it requires you to extract model data out of one of the container files and save as a binary. This must currently be done manually.
map_texture_mesh_file_name_00 (and 01,02,03,04) are names of the texture mesh files you want to use. Again, you must extract this data out of one of the container files and save as a binary.

See the BND and MAP documentation from Lex Safanov for pointers on how to do this. Generally models will start with an M00 style header (or L00 for lifts and D00 for doors) and texture maps will start with a BX00 header. Copy hex including the header all the way down to the byte preceding the next header and save out as a binary.

## Additional Notes
There is an extra manual step required after using Bin2Obj to extract geometry. As per the docs, if the game wants to denote a triangle instead of a quad, it will set the 4th vertex index to FF instead of a valid value. Bin2Obj will interpret this as a 0 which isn't valid either, for this to work these 0s need to be completely removed. After extraction you should open the obj file up in a text editor and do a bulk replace of all 0 values with nothing.

It is recommended to 'sanitise' the coordinates which by default are very large values. Scaling down by 0.01 seems to get good results in Blender

