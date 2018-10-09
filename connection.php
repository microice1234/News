<?php

	$dbhost = "localhost";
	$dbuser = "root";
	$dbpassword = "";
	$db = "allinonenews";

	$conn = new mysqli ($dbhost,$dbuser,$dbpassword);

	// Check connection
	if($conn->connect_error){
		echo "Connection failed";
	}
	else{
		echo "Connection successful";
	}
	
	$sql = "CREATE DATABASE $db";
	if ($conn->query($sql) === TRUE) {
		echo "Database created successfully";
	} else {
		echo "Error creating database: " . $conn->error;
	}
	
	$conn = new mysqli ($dbhost,$dbuser,$dbpassword,$db);
	
	// sql to create table
	$sql = "CREATE TABLE admin (
ad_id int(30) NOT NULL,
id int(30) NOT NULL,
Work varchar(30) NOT NULL
)";
	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Admin created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}

	$sql = "CREATE TABLE `article` (
  `arti_id` int(30) NOT NULL,
  `name` varchar(50) NOT NULL,
  `date_pub` date NOT NULL,
  `aid` int(30) NOT NULL,
  `eid` int(30) NOT NULL
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Aritcle created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}
	
	$sql = "CREATE TABLE `article_cat` (
  `arti_id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Article Categories created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}

	$sql = "CREATE TABLE `author` (
  `aid` int(30) NOT NULL,
  `id` int(30) NOT NULL,
  `no_articles` int(10) NOT NULL,
  `rank` int(10) NOT NULL
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Author created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}
	
	$sql = "CREATE TABLE `editor` (
  `eid` int(30) NOT NULL,
  `id` int(30) NOT NULL,
  `no_edits` int(10) NOT NULL
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Editor created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}

	$sql = "CREATE TABLE `person` (
  `id` int(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `contactNo` int(10) NOT NULL,
  `password` char(30) NOT NULL,
  `country` varchar(15) NOT NULL DEFAULT 'India',
  `email` varchar(30) NOT NULL DEFAULT 'abc12@abc12.com'
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Person created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}
	
	$sql = "CREATE TABLE `recommendations` (
  `categories` varchar(30) NOT NULL,
  `type` varchar(30) NOT NULL,
  `uid` int(30) NOT NULL
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table Recommendations created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}

	$sql = "CREATE TABLE `user` (
  `uid` int(30) NOT NULL,
  `id` int(30) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(10) NOT NULL
)";

	if ($conn->query($sql) === TRUE) {
    		echo "<h1>Table User created successfully</h1>";
	}else {
    		echo "Error creating table: " . $conn->error;
	}
	$conn->close();	
?>