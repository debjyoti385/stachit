<?php 

	$q=$_GET["q"];

	//$q="\"Sachin tendulkar and Rahul dravid\"";

	$command = "python cap_test.py " . $q ;

	//echo $command;
	//$command = 'ls';
	
	system($command, $retval);

	//echo "<br/>" . "From server after query solution ";
?>

	
