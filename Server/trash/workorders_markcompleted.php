<?php
session_start();
require_once 'libs/all.php';
$loc = "workorders_markcompleted.php";
echo "made it!";
if(isset($_POST['completed']) && 
   $_POST['completed'] == 'Yes') 
{
	log_msg($loc,
       array("Work Order Completed!  Work Order ID =" . $_SESSION["WorkOrderID"]));
	$WorkOrderID = $_SESSION["WorkOrderID"];
        $success_msg = 'Work Order "' . $WorkOrderID . ' completed.';
	$sql =  'UPDATE WorkOrders SET completed = 1 WHERE WorkOrderID = "' . $WorkOrderID . '";';
	$result = SqlQuery($loc, $sql);
	echo "Work Order " . $_SESSION["WorkOrderID"] . "Completed";
    	JumpToPage("workorders_thisuser.php");
}
echo "outside";
if(isset($_POST['AssignedTo']))
{
	echo "inside?";
//	&&
//   $_POST['completed'] == 'Yes')
//{
	log_msg($loc,
       array("User assigned!  for Work Order ID =" . $_SESSION["WorkOrderID"]));
	$WorkOrderID = $_SESSION["WorkOrderID"];
	$userid = $_SESSION["UserID"];
        $success_msg = 'Work Order  ' . $WorkOrderID . ' completed.';
	$sql =  'UPDATE WorkOrders SET AssignedTo ="' . $userid . '"  WHERE WorkOrderID = "' . $WorkOrderID . '";';
	$result = SqlQuery($loc, $sql);
	echo "Worker  " . $_SESSION["WorkOrderID"] . " Completed";
    	JumpToPage("workorders_thisuser.php");
}

?>

