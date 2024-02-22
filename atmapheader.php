<?php
//Alien Trilogy DOS geometry extractor script by Bobblen
//based on documentation on the Xentax wiki by Lex Safonov
//
//this script generates a command line to use with Bin2Obj by Mark Sowden
//Bin2Obj expects decimals in its command line so everything is converted
//
//usage: php atmapheader.php
//don't forget to set your type, filename and path on lines 14,15,16!


ini_set('memory_limit','128M');

$type = 'map'; //map or model
$filename = 'L111LEV.MAP';
$bin = fopen("D:\\Maps\\".$filename, "r");

if( $type == 'map' )
{
	$header = 0x14; // hardcoded length
	$vsoffset = 56; //in decimal, always straight after header. Map format is vertexes then quads
}

if( $type == 'model' )
{
	$header = 0x14; // hardcoded length
	$qsoffset = 28; //in decimal, always straight after header. Model format is quads then vertexes
}

fseek( $bin, $header );

if( $type == 'map' )
	{
	//get vertex count in decimal
	$lowv = getByte($bin);
	$highv = getByte($bin);
	$vcount = binhex(chr($highv)).binhex(chr($lowv));
	$decvcount = hexdec($vcount);
	
	//get vertex end offset in decimal
	$veoffset = ($vsoffset-1) + ($decvcount*8) -2; //bin2obj reads too far unless you ignore the last 2 unused bytes
	
	//get quad count in decimal
	$lowq = getByte($bin);
	$highq = getByte($bin);
	$qcount = binhex(chr($highq)).binhex(chr($lowq));
	$decqcount = hexdec($qcount);
	
	//get quad start and end offsets in decimal (quads follow on directly from the vertexes)
	$qsoffset = $veoffset + 3;
	$qeoffset = $qsoffset + ($decqcount*20) -2;//ignore last 2 unused bytes again
	}

if( $type == 'model' )
	{
	//get quad count in decimal
	$lowq = getByte($bin);
	$highq = getByte($bin);
	getByte($bin);//unused
	getByte($bin);//unused
	$qcount = binhex(chr($highq)).binhex(chr($lowq));
	$decqcount = hexdec($qcount);
	
	//get quad end offset in decimal
	$qeoffset = ($qsoffset-1) + ($decqcount*20) -2; //bin2obj reads too far unless you ignore the last 2 unused bytes
	
	//get vertex count in decimal
	$lowv = getByte($bin);
	$highv = getByte($bin);
	getByte($bin);//unused
	getByte($bin);//unused
	$vcount = binhex(chr($highv)).binhex(chr($lowv));
	$decvcount = hexdec($vcount);
	
	//get vertex start and end offsets in decimal (they follow on directly from the quads)
	$vsoffset = $qeoffset + 3;
	$veoffset = $vsoffset + ($decvcount*8) -2;//ignore last 2 unused bytes again
	}

echo "Alien Trilogy DOS map header reader\n\n";
echo "file name is ".$filename."\n";
echo "file type is set to ".$type."\n";
echo "vertex count (decimal) ".$decvcount."\n";
echo "face count (decimal) ".$decqcount."\n";
echo "vertex start offset (decimal) ".$vsoffset."\n";
echo "vertex end offset (decimal) ".$veoffset."\n";
echo "face start offset (decimal) ".$qsoffset."\n";
echo "face end offset (decimal) ".$qeoffset."\n\n";
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