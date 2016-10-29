<?php
// --------------------------------------------------------------------
// reader_upload_scan.php - upload data from scanner onto EpicAdmin website
// created 07/27/16  
// --------------------------------------------------------------------

require_once "libs/all.php";
$loc = 'reader_upload_scan.php';
$error_msg = "";
$success_msg = "";
$userid = 0;
$username = "";
$picurl = "";
$badge_front_url = "";
$badge_back_url  = "";
$badgeid = "";
$json="";
$nadded=0;
$nadded=0;
$nupdated=0;
if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['json'])){
	$json=$_POST["json"];
	$decoded = json_decode($json, true);
	if (! isset($decoded['logtime'])) $error_msg .= " logtime,";
	if (! isset($decoded['badgeid'])) $error_msg .= " badgeid,";
	if (! isset($decoded['side'])) $error_msg .= " side,";
	if (! isset($decoded['flags'])) $error_msg .= " flags,";
	if (! isset($decoded['firstname'])) $error_msg .= " firstname,";
	if (! isset($decoded['lastname'])) $error_msg .= " lastname";
	if ($error_msg != ""){
		$error_msg = "Incoming scan is missing values: " . $error_msg;
		log_error($loc, $error_msg);
	} else{
		$tme = $decoded['logtime'];
		$badgeid=$decoded['badgeid'];
		$dir = $decoded['side'];
		$flag = $decoded['flags'];
		$firstname = $decoded['firstname'];
		$lastname = $decoded['lastname'];
		$method = "log";
		$readerid = "B17";
		$ir = UpdateRawScan($tme, $badgeid, $dir, $flag, $method, $readerid);
		if($ir != 0) {
			$nadded++;
			log_msg($loc, "Badge " . $badgeid . " ( " . $firstname . " " . $lastname . ") Scanned in at " . $tme);
		}
		else{
		         $nupdated++;
			log_msg($loc, "Scan Updated for: Badge " . $badgeid . " ( " . $firstname . " " . $lastname . ") at " . $tme);
		}

	}
}
?>
