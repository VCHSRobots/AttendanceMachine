<?php
// --------------------------------------------------------------------
// reader_pull_all.php - Pull all logs from scanner to website
// created 07/27/16  
// --------------------------------------------------------------------

require_once "libs/all.php";
$loc = 'reader_pull_all.php';
$error_msg = "";
$success_msg = "";
$json="";
$nadded=0;
$nupdated=0;
$nfailed=0;
if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['scans'])){
	$scans=$_POST["scans"];
	$scanList=explode("\n", $scans);
	foreach ($scanList as &$json){
		$error_msg="";
		if ($json != ""){
			$decoded = json_decode($json, true);
			if (! isset($decoded['logtime'])) $error_msg .= " logtime,";
			if (! isset($decoded['badgeid'])) $error_msg .= " badgeid,";
			if (! isset($decoded['side'])) $error_msg .= " side,";
			if (! isset($decoded['flags'])) $error_msg .= " flags,";
			if (! isset($decoded['firstname'])) $error_msg .= " firstname,";
			if (! isset($decoded['lastname'])) $error_msg .= " lastname";
			if ($tempError != ""){
				$error_msg = "Incoming scan is missing values: " . $error_msg . ". [SCAN]:" . $decoded . "\n";
				log_error($loc, $error_msg);
				$nfailed++;
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
					//log_msg($loc, "Badge " . $badgeid . " ( " . $firstname . " " . $lastname . ") Scanned in at " . $tme);
				}
				else{
				         $nupdated++;
					//log_msg($loc, "Scan Updated for: Badge " . $badgeid . " ( " . $firstname . " " . $lastname . ") at " . $tme);
				}

			}
		}
	}
	log_msg($loc, "All Logs Pulled from scanner. " . $nadded . " added, " . $nupdated . " updated,  " . $nfailed . " failed. ");

	
}
?>
