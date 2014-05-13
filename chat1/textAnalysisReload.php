
<?php

	session_start();

	echo "<div id=\"header_text\">Your points of discussion</div>";

	$con = mysql_connect("localhost","root","1234");
	if (!$con)
	{
	  die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("chat", $con);

	//$result = mysql_query("SELECT MAX(webchat_lines.id) as MAXITEM FROM webchat_lines");
	//$row = mysql_fetch_array($result);
//	echo "MAXIMUM : ". $row['MAXITEM'];

	$result = mysql_query("SELECT * FROM webchat_lines LIMIT 5");

	echo "<br/>";

	$corpus="";

	while($row = mysql_fetch_array($result))
	{
		//echo "<br/>" . $row['id'] . "     ";
		$corpus = $corpus . $row['text'] . "\n";
	}

	//echo count($result);

	if(isset($_SESSION['name']))
	{
		$result = mysql_query("SELECT webchat_users.concepts FROM webchat_users where webchat_users.name='".$_SESSION['name']."'");
		$row = mysql_fetch_array($result);

		if(isset($row)){
					
			$chunks = explode("*", trim($row[0]));

			//print_r($chunks);
	
			for($i = 0; $i < count($chunks) && $i < 15; $i++){
				if($chunks[$i]=="")
						continue;
				echo	"<div class=\"button\" onClick=\"callGetValue(this.innerHTML) \">". $chunks[$i] .						
					"</div>";
			}
		}
	}
	if($corpus!="")
	{
	//	echo $corpus . "<br/>";

		//$corpus = "If you want to help contribute to Ubuntu then you've come to the right place. Keep reading to learn how. ";

		//echo $corpus . "<br/>";
		//echo "<div class=\"button\" onClick=\"callGetValue(this.innerHTML) \">". " testing ". "</div>";
		$command = "python cap_test.py \"" . $corpus . "\" > corpusConcepts.txt";

	//	echo $command . "<br/>";
		system($command);
	
		$theData="";
		while(!file_exists("corpusConcepts.txt")){}

		$myFile = "corpusConcepts.txt";
		$fh = fopen($myFile, 'r') or exit("Unable to open file!");
		while(!feof($fh))
		{
			//echo fgets($fh) . "<br/>";
			$theData = $theData . fgets($fh);
		}
		fclose($fh);
	//	echo $theData;
		//echo "<div class=\"button\" onClick=\"callGetValue(this.innerHTML) \">". $theData . "</div>";
		
		$command = "rm corpusConcepts.txt";
		system($command);

		$chunks = explode("\n", trim($theData));

		if(count($chunks) == 0  && isset($_SESSION['name']))
		{
			$result = mysql_query("SELECT * FROM webchat_users where webchat_users.name='".$_SESSION['name']."'");
			$row = mysql_fetch_array($result);
		
			if(isset($row)){
					
				$chunks = explode("*", trim($row[0]['concepts']));

				//print_r($chunks);
	
				for($i = 0; $i < count($chunks) && $i < 15; $i++){
					if($chunks[$i]=="")
						continue;
					echo	"<div class=\"button\" onClick=\"callGetValue(this.innerHTML) \">". $chunks[$i] .						
						"</div>";
				}
			}
		}
		else
		{

			//print_r($chunks);

			if(isset($_SESSION['name'])){
	
				for($i = 0; $i < count($chunks); $i++){
					if($chunks[$i]=="")
						continue;
					echo	"<div class=\"button\" onClick=\"callGetValue(this.innerHTML) \">". $chunks[$i] . "</div>";
					mysql_query("UPDATE webchat_users set webchat_users.concepts=concat(webchat_users.concepts,concat('*','".$chunks[$i]."')) where webchat_users.name='".$_SESSION['name']."'");
				}
			}
		}
	}

	mysql_close($con);
?>
