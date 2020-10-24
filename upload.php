<?php

$responseData = array(
    'status' => 'failed'
);

if(isset($_POST['image']) && isset($_POST['decoration']) && !empty($_POST['image']) && is_numeric($_POST['decoration'])){
    $image = $_POST['image'];
    $decoration = $_POST['decoration'];
    if($decoration > 0 && $decoration < 4){
        $fileName = 'user-results/'.date('Ymdhsi').'-'.mt_rand(10000, 99999).'.jpeg';
        $image = substr($image, (strpos($image,',')+1));
        if(file_put_contents($fileName, base64_decode($image))){
            $responseData['status'] = 'success';
            $responseData['url'] = $fileName;
        }        
    }
}

print(json_encode($responseData));

?>