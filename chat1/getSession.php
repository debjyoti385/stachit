<?php
	session_start();

	if(isset($_SESSION['name']))
		echo $_SESSION['name']."_";
	else
		echo "";
?>
