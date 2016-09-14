<?php

if( $_SERVER["REQUEST_METHOD"] == "POST”){
	$myfile = fopen("newfile.txt", "w") or die("Unable to open file!");
	foreach ($_POST as $key => $value) {
		$txt = $key . “=“ . $value;
		fwrite($myfile, $txt);
 	}
fclose($myfile);
}


?>