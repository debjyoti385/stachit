<?php

	session_start();

	if(isset($_SESSION['name']))
	{
		$command = 'rm ' . $_SESSION['name'] . "_sample1.json";
		system($command);
	}

	if(isset($_SESSION['name']))
		unset($_SESSION['name']);
	//session_destroy();

?>
