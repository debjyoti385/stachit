<?php 

	session_start();

	$q=urldecode($_GET["q"]);
	$q = "\"" . $q . "\"";

	if(isset($_SESSION['name']))
		$command = "python boss_test.py " .  $_GET["r"] . " " . $q . " " . $_SESSION['name'] . "_sample1.json";
	else
		$command = "python boss_test.py " .  $_GET["r"] . " " . $q . " sample1.json";

	//echo $command;
	//$command = 'ls';
	
	$last_line = system($command , $retval);

	echo "<br/>" . "From server after query solution " . $retval . " " . $command;
?>

	
