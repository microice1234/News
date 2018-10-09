<html> 
    <head> 
        <title>Count Page Access</title> 
   </head> 
  <body> 
<?php 
    if (!isset($_COOKIE['count']))
    {
?> 
Welcome! This is the first time you have viewed this page. 
<?php 
        $cookie = 1;
        setcookie("count", $cookie);
    }
    else
    {
        $cookie = ++$_COOKIE['count'];
        setcookie("count", $cookie);
?> 
You have viewed this page <?= $_COOKIE['count'] ?> times. 
<?php   }    ?> 
   </body> 
</html>