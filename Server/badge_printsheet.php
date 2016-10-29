
<?php
require_once "libs/all.php";
$testSheet = "Badges_2016-2017_";
$badgelist=array("C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008");
MakePrintSheet($badgelist, $testSheet."1");
$badgelist=array("C009", "C010", "C011", "C012", "C013", "C014", "C017", "C018");
MakePrintSheet($badgelist, $testSheet."2");
$badgelist=array("C021", "C022", "C023", "C024", "C025", "C026", "C027", "C028");
MakePrintSheet($badgelist, $testSheet."3");
$badgelist=array("C029", "C030", "C031", "C032", "C033", "C034", "C035", "C036");
MakePrintSheet($badgelist, $testSheet."4");
$badgelist=array("C033", "C065", "C066", "C067", "C039", "C015", "C039", "C040");
MakePrintSheet($badgelist, $testSheet."5");
$badgelist=array("C041", "C042", "C043", "C044", "C045", "C046", "C047", "C048");
MakePrintSheet($badgelist, $testSheet."6");
$badgelist=array("C049", "C050", "C051", "C052", "C053", "C054", "C055", "C056");
MakePrintSheet($badgelist, $testSheet."7");
$badgelist=array("C057", "C058", "C059", "C060", "C061", "C062", "C063", "C064");
MakePrintSheet($badgelist, $testSheet."8");

echo "finished!"
?>
