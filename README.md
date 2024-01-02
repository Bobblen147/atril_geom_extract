# Alien Trilogy DOS Geometry Extraction PHP Helper Script
This PHP script will read the header of an Alien Trilogy DOS map or model file and determine the offsets required to extract geometry to the wavefront obj format. It does not do the extraction itself but instead generates some useful information and a command line to be used with another tool, Bin2Obj by Mark E Sowden. The command line can be used directly with Bin2Obj as is or adapted for use with your binary hacking program of choice.

## Credits
This script is entirely based on the documentation of the Alien Trilogy map and model format reverse engineered by Lex Safonov and available on the Xentax wiki here (https://web.archive.org/web/20230518104117/https://wiki.xentax.com/index.php/Alien_Trilogy_MAP)
(https://web.archive.org/web/20230518104114/https://wiki.xentax.com/index.php/Alien_Trilogy_BND)

Bin2Obj is authored by Mark E Sowden who is not involved with this particular project in any way. He just happened to have written a compact binary obj extractor that supported quads and which I happened to stumble across when looking at Alien Trilogy.
(https://github.com/hogsy/Bin2Obj)

The PHP script itself is effectively a heavily hacked up version of an 8 bit Sonic the Hedgehog map extraction script by Rolken from Sonic Retro. Little remains of the original script other than a few byte manipulation functions and the general structure. This script can be found here https://www.soniccenter.org/rolken/stt/sttrom.txt

## Usage
The script almost works as is, but needs to be modified a little to suit your particular setup.

The $type variable at the top of the script can be set to 'map' or 'model'. There are no sanity checks for this, but the output will print which is selected. If you're getting garbage output that's something to check.

The $filename variable at the top of the script should be set to the name of the file you're interested in.

This line '$bin = fopen("D:\\VSProjects\\Bin2Obj-master\\x64\\Debug\\".$filename, "r");' should be modified to reflect the location of the file you're interested in. Ideally that would be a variable too, but isn't yet.

## Additional Notes
There is an extra manual step required after using Bin2Obj to extract geometry. As per the docs, if the game wants to denote a triangle instead of a quad, it will set the 4th vertex index to FF instead of a valid value. Bin2Obj will interpret this as a 0 which isn't valid either, for this to work these 0s need to be completely removed. After extraction you should open the obj file up in a text editor and do a bulk replace of all 0 values with nothing.

Also all Alien Trilogy maps appear to end with a final quad of index ff ff ff ff. This is always included in the quad count, so bin2obj will throw a warning up that all values are zero and completely ignore it. This appears to work fine and doesn't require manual action.

For models, this script cannot work on the raw files which often contain multiple models and other structures mixed together. Each model is generally denoted M00, M01 etc (see the docs for details). Use a hex editor to extract an individual model (copy from M00 text to the byte before the next header) to its own file and apply the script to that file.
