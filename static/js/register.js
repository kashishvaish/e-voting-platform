function openCamera() {
    Webcam.set({
        width: 320,
        height: 240,
        dest_width: 640,
        dest_height: 480,
        image_format: 'jpeg',
        jpeg_quality: 100
    });
    Webcam.attach('#my_camera');
    document.getElementById('captureButton').style.visibility = "visible";
}

function take_snapshot() {
    Webcam.snap(function(data_uri) {
        var raw_image_data = data_uri.replace(/^data\:image\/\w+\;base64\,/, '');
        document.getElementById('faceImage').value = raw_image_data        
        Webcam.reset();
        document.getElementById('captureButton').style.visibility = "hidden";
        document.getElementById('error').innerHTML = "Captured"
        document.getElementById('error').style.color = "green"
    } );            
}

function validate() {
    if (document.getElementById('faceImage').value) {
        document.getElementById('registerForm').submit();
    }
    else {
        document.getElementById('error').innerHTML = "*Capture Your Image";
        alert("Capture Image for face Verification!!");
    }
}