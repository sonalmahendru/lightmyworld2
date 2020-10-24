var videoHeight = document.getElementsByTagName("main")[0].offsetHeight;
var videoWidth = document.getElementsByTagName("main")[0].offsetWidth;
var permissonAllowed = false;

var video = document.getElementById("video");
video.height = videoHeight;
video.width = videoWidth;
video.autoplay = true;
video.hidden = false;

var canvas = document.getElementById("canvas");
canvas.hidden = true;


var context = canvas.getContext('2d');
context.translate(canvas.width , 0);
context.scale(-1,1);

var captureButton = document.getElementById("captureButton");
var retakeButton = document.getElementById("retakeButton");
retakeButton.hidden = true;
var proceedButton = document.getElementById("proceedButton");
proceedButton.hidden = true;

function start(){
    if(navigator.mediaDevices === undefined){
        alert("Opps!! Your device do not support video streaming");
    }else{
        if(navigator.mediaDevices.getUserMedia){
            navigator.mediaDevices.getUserMedia({video: {width:videoWidth , height:videoHeight }}).then(function(stream){
                video.srcObject = stream;
                permissonAllowed = true;
            }).catch(function(error){
                alert("Kindly allow permisson so you can capture image");
            });
        }else{
            alert("Opps!! No media device has been found");
        }
    }
}

function snap(){
    if(permissonAllowed == false){
      start();
    }else{

        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;
        canvas.style.marginTop = ((videoHeight - video.videoHeight)/2)+"px";
      
        var context = canvas.getContext('2d');
        context.translate(canvas.width , 0);
        context.scale(-1,1);
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        var imageData = canvas.toDataURL('image/jpeg');
        localStorage.setItem("diwaliImage", imageData);

        video.hidden = true;
        canvas.hidden = false;
        captureButton.hidden = true;
        retakeButton.hidden = false;
        proceedButton.hidden = false;

        var downloadLink = document.createElement('a');
        downloadLink.href = imageData;
        downloadLink.download = 'download.jpg';
        downloadLink.click();

    }
}

function retake(){
    canvas.hidden = true;
    video.hidden = false;
    retakeButton.hidden = true;
    proceedButton.hidden = true;
    captureButton.hidden = false;
    context.clearRect(0, 0, canvas.width, canvas.height);
}