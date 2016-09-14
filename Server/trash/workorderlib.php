<?php
// --------------------------------------------------------------------
// Given the WorkOrderID, returns a associative array, with the following
// keys: (WorkOrderID, WorkOrderName, Description, DateRequested,
//    DateNeeded, Priority, DayEstimate, Revision, Requestor,
//    RequestingIPTLeadApproval, AssignedIPTLeadApproval, Project, 
//    RequestingIPTGroup, ReceivingIPTGroup, ProjectOfficeApproval,
//    ReviewedBy, AssignedTo, Completed, CompletedOn). False returned if
//    work order not found.
function GetWorkOrderInfo($workorderid)
{
    $loc = "userlib.php->GetUserInfo";
    $sql = 'SELECT * FROM WorkOrders WHERE WorkOrderID=' . SqlClean($workorderid);
    $result = SqlQuery($loc, $sql);
    if($result->num_rows != 1) { return false; }
    $row = $result->fetch_assoc();
    return $row;
}
// --------------------------------------------------------------------
// Given the WorkOrderID, returns a associative array, with the following
// keys: (PrereqID, PrevWorkOrderID, WorkOrderID). False returned if
//    work order prerequisite not found.
function GetWorkOrderPrereqInfo($workorderid)
{
    $loc = "userlib.php->GetUserInfo";
    $sql = 'SELECT * FROM Prerequisites WHERE WorkOrderID=' . SqlClean($workorderid);
    $result = SqlQuery($loc, $sql);
    if($result->num_rows != 1) { return false; }
    $row = $result->fetch_assoc();
    return $row;
}
// --------------------------------------------------------------------
// Given the WorkOrderID, returns a associative array, with the following
// keys: (TaskID, WorkOrderID, Quantity, Description, UnitPrice). False returned if
//    work order task not found.
function GetWorkOrderTasksInfo($workorderid)
{
    $loc = "userlib.php->GetUserInfo";
    $sql = 'SELECT * FROM WorkOrderTasks WHERE WorkOrderID=' . SqlClean($workorderid);
    $result = SqlQuery($loc, $sql);
    if($result->num_rows != 1) { return false; }
    $row = $result->fetch_assoc();
    return $row;
}
// --------------------------------------------------------------------
// Given the WorkOrderID, returns a associative array, with the following
// keys: (FileID, WorkOrderID, FilePath). False returned if
//    work order task not found.
function GetWorkOrderFiles($workorderid)
{
    $loc = "userlib.php->GetUserInfo";
    $sql = 'SELECT * FROM RelatedFiles WHERE WorkOrderID=' . SqlClean($workorderid);
    $result = SqlQuery($loc, $sql);
    if($result->num_rows != 1) { return false; }
    $row = $result->fetch_assoc();
    return $row;
}
?>
