<html>
<head>
	<link rel="stylesheet" type="text/css" href="css/page.css" />
	<script src="js/jquery.min.js" type="text/javascript" charset="UTF-8"></script>
	<link href="css/a.css" type="text/css" rel="stylesheet" />

	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script> 
	<script>



var auto_refresh = setInterval(
function()
{
$('#button_search').fadeOut('slow').load('textAnalysisReload.php').fadeIn("slow");
}, 10000);


		function callGetValue(value)
		{
			//alert(value);
			getValue(value,"sendToBoss.php","web");
		}
		function clickResponse()
		{
			getValue(document.getElementById("user_search").value,"sendToBoss.php","web");
		}
		
		function keyResponse(e)
		{
			if(e.keyCode == 13)
				getValue(document.getElementById("user_search").value,"sendToBoss.php","web");
		}

		function getValue(input,fileName,key)
		{
			var xmlhttp;
			var responseFromServer="0";
			if (input.length==0 || input == "Search...")
			{ 
				return;
			}
			if (window.XMLHttpRequest)
			{// code for IE7+, Firefox, Chrome, Opera, Safari
				xmlhttp=new XMLHttpRequest();
			}
			else
			{// code for IE6, IE5
				xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
			}
			xmlhttp.onreadystatechange=function()
			{
				if (xmlhttp.readyState==4 && xmlhttp.status==200)
				{
					responseFromServer=xmlhttp.responseText;
					//alert(responseFromServer);
				}
			}
			xmlhttp.open("GET",fileName + "?q=" + encodeURIComponent(input) + "&r=" + key,false);
			xmlhttp.send();

			parent.parent.timeline.refresh(input);
			//alert("DID NOT WORK PROPERLY");
		}
	</script>
</head>
<body>
<?php

	session_start();

?>

<div id="button_search">

</div>

</body>
</html>
