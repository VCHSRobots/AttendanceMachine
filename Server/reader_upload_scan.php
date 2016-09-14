<?php
// --------------------------------------------------------------------
// reader_upload_scan.php - upload data from scanner onto EpicAdmin website
// created 07/27/16  
// --------------------------------------------------------------------

require_once "libs/all.php";
session_start();
log_page();
//CheckLogin();
//CheckEditor();
$timer = new timer();
$loc = 'reader_upload_scan.php';
$error_msg = "";
$success_msg = "";
$userid = 0;
$username = "";
$picurl = "";
$badge_front_url = "";
$badge_back_url  = "";
$badgeid = "";

$json = '{"logtime": "2016/07/27 17:33:29", "badgeid": "B041", "side": "back", "flags": "okay", "lastname": "Poole", "firstname": "Jelani"}';
$decoded = json_decode($json, true);
echo print_r($decoded, true);
echo $decoded['logtime'];
?>
