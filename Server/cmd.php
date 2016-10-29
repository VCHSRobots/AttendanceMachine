<?php
if (isset($_POST["command"]))
{
    $data = $_POST["command"];
    $f = fopen("cmd.txt", "a+");
    fwrite($f, $data . "\n");
    fclose($f);
}
else
{
    $data = "";
}
?>
