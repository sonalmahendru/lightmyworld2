function begin_clicked(){
    window.location.href="capture.html";
}

function proceed(){
    window.location.href = 'decoration.html';
}

function getResult(decoration){

    document.getElementById("overlay-background").style.display = 'block';

    var imageData = localStorage.getItem("diwaliImage");
    var XMLhttp = new XMLHttpRequest();

    XMLhttp.onreadystatechange = function(){
        if(XMLhttp.readyState == 4){
            if(XMLhttp.status == 200){

                document.getElementById("overlay-background").style.display = 'none';
                
                console.log(this.responseText);

            }else{
                alert("Opps!! Looks like something went wrong please try again after sometime")
            }
        }
    }

    var formData = new FormData;
    formData.append("image",imageData);
    formData.append("decoration",decoration);
    XMLhttp.open("POST","upload.php");
    XMLhttp.send(formData);
}