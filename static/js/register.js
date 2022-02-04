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
        document.getElementById('enterDetails').style.visibility = "visible";
        document.getElementById('capture').style.visibility = "hidden";
    } );            
}

function validate() {
    if (document.getElementById('faceImage').value && 
    document.getElementById('aadhaarNo').value &&
    document.getElementById('name').value &&
    document.getElementById('dob').value &&
    document.getElementById('aadhaarImage').value) {
        document.getElementById('registerForm').submit();
    }
    else if (document.getElementById('faceImage').value == "") {
        alert("Capture Image for face Verification!!");
    }
    else if (document.getElementById('aadhaarNo').value == "") {
        alert("Enter your Aadhaar Number!!");
    }
    else if (document.getElementById('name').value == "") {
        alert("Enter your Name!!");
    }
    else if (document.getElementById('dob').value == "") {
        alert("Enter your Date of Birth!!");
    }
    else if (document.getElementById('aadhaarImage').value == "") {
        alert("Upload your Aadhaar Card Image!!");
    }
}