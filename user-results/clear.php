<?php

$images = scandir("../user-results");

foreach($images as $image){
	if(pathinfo($image, PATHINFO_EXTENSION) == "png"){
		 unlink($image);
	}
}

?>