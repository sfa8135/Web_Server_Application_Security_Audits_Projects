<?php
//in this script will send header info using php-cgi  

echo $_GET['statusCode'] ;

//send either GET or POST
// GET: URI.  POST:request header

// $_POST['']

echo "\n";
 
$contentType = $argv[1];
echo $contentType  ; 

// the result will be displayed to the user

?>
