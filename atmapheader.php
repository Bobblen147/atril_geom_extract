<?php
//Alien Trilogy DOS geometry extractor script by Bobblen
//based on documentation on the Xentax wiki by Lex Safonov
//this generates a command line to use with Bin2Obj by Mark Sowden

ini_set('memory_limit','128M');

$type = 'map'; //map or model
$filename = 'L111LEV.MAP';

if( $type == 'map' )
{
	$header = 0x14; // Hardcoded
	$vsoffset = 56; //always straight after header
}

if( $type == 'model' )
{
	$header = 0x14; // Hardcoded
	$qsoffset = 28; //always straight after header
}

$bin = fopen("D:\\VSProjects\\Bin2Obj-master\\x64\\Debug\\".$filename, "r");
fseek( $bin, $header );

if( $type == 'map' )
{
//get vertex count
$lowv = getByte($bin);
$highv = getByte($bin);
$vcount = binhex(chr($highv)).binhex(chr($lowv));
$decvcount = hexdec($vcount);

//get vertex end offset in decimal
$veoffset = ($vsoffset-1) + ($decvcount*8) -2; //bin2obj reads too far unless you subtract the last 2 unused bytes

//get quad count
$lowq = getByte($bin);
$highq = getByte($bin);
$qcount = binhex(chr($highq)).binhex(chr($lowq));
$decqcount = hexdec($qcount);

//get quad start and end offsets
$qsoffset = $veoffset + 3;
$qeoffset = $qsoffset + ($decqcount*20) -2;//same as for vertices above
}

if( $type == 'model' )
{
//get quad count
$lowq = getByte($bin);
$highq = getByte($bin);
getByte($bin);//unused
getByte($bin);//unused
$qcount = binhex(chr($highq)).binhex(chr($lowq));
$decqcount = hexdec($qcount);

//get quad end offset in decimal
$qeoffset = ($qsoffset-1) + ($decqcount*20) -2; //bin2obj reads too far unless you subtract the last 2 unused bytes

//get vertex count
$lowv = getByte($bin);
$highv = getByte($bin);
getByte($bin);//unused
getByte($bin);//unused
$vcount = binhex(chr($highv)).binhex(chr($lowv));
$decvcount = hexdec($vcount);

//get vertex start and end offsets
$vsoffset = $qeoffset + 3;
$veoffset = $vsoffset + ($decvcount*8) -2;//same as for quads above
}

echo "Alien Trilogy DOS map header reader\n\n";
echo "file name is ".$filename."\n";
echo "file type is set to ".$type."\n";
echo "vertex count ".$decvcount."\n";
echo "face count ".$decqcount."\n";
echo "vertex start offset ".$vsoffset."\n";
echo "vertex end offset ".$veoffset."\n";
echo "face start offset ".$qsoffset."\n";
echo "face end offset ".$qeoffset."\n\n";
echo "bin2obj.exe ".$filename." -soff ".$vsoffset." -eoff ".$veoffset." -stri 2 -vtyp 1 -fsof ".$qsoffset." -feof ".$qeoffset." -fstr 4 -ftyp 1 -fquad";






////////////////////////////////////////////////////////

// Functions
function binhex( $data )
{
	$str = '';

	for( $i=0; $i<strlen($data); $i++)
	{
		
		$num = ord($data[$i]);
		if( $num < 16 ) $str .= '0';
		$str .= dechex($num);
	}
	return strtoupper($str);
}



function getByte( &$source )
{
	return ord( fread( $source,1 ) );
}



?>