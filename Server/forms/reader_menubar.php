<!--
** --------------------------------------------------------------------
** reader_menubar.php -- HTML fragment to show the reader menu bar.
**
** Created: 1/15/15 DLB
** --------------------------------------------------------------------
-->

 <style>
    .content_area {min-height: 275px; } 
 </style>

<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript">
function rqln()
    {
        $.post("cmd.php", { command: "rqln" }, function() { content.html(response); });
    }
function rqla()
    {
        $.post("cmd.php", { command: "rqla" }, function() { content.html(response); });
    }
function rqlo()
    {
        $.post("cmd.php", { command: "rqlo" }, function() { content.html(response); });
    }
function rqul()
    {
        $.post("cmd.php", { command: "rqul" }, function() { content.html(response); });
    }
function tgdm()
    {
        $.post("cmd.php", { command: "tgdm" }, function() { content.html(response); });
    }
function psul()
    {
        $.post("cmd.php", { command: "psul" }, function() { content.html(response); });
    }
</script>

<div class="menubar_area">

<!--

<div class="menu_button">
<a href="reader_uploadlog.php">Upload Log</a>
</div>

<div class="menu_button">
<a href="reader_uploadcorrections.php">Upload Corrections</a>
</div>

-->

<div class="menu_button">
<a href="" onclick="rqln();">Pull Newest</a>
</div>

<div class="menu_button">
<a href="" onclick="rqla();">Pull All</a>
</div>
<!--
<div class="menu_button">
<a href="" onclick="rqlo();">Pull Outlog</a>
</div>

<div class="menu_button">
<a href="" onclick="rqul();">Pull Userlist</a>
</div>

<div class="menu_button">
<a href="" onclick="tgdm();">Toggle Demo</a>
</div>

<div class="menu_button">
<a href="" onclick="psul();">Push Userlist</a>
</div>
-->
<div class="menu_button">
<a href="reader_uploadlog.php">Upload Log</a>
</div>

<div class="menu_button">
<a href="reader_uploadcorrections.php">Upload Corrections</a>
</div>
</div>
