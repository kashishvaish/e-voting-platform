from django.shortcuts import render, redirect
from .form import CustomRegisterForm
from django.contrib import messages
import cv2
from pyzbar.pyzbar import decode
import xmltodict
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import CognitiveServicesCredentials, ApiKeyCredentials
from decouple import config
from PIL import Image
import numpy as np
import io
import os
import base64
from pyaadhaar.deocde import AadhaarSecureQr
from pyaadhaar.deocde import AadhaarOldQr
from datetime import datetime

FACE_API_KEY=os.environ['FACE_API_KEY']
FACE_ENDPOINT=os.environ['FACE_ENDPOINT']
DETECTION_KEY=os.environ['DETECTION_KEY']
DETECTION_ENDPOINT=os.environ['DETECTION_ENDPOINT']
DETECTION_MODEL_NAME=os.environ['DETECTION_MODEL_NAME']
DETECTION_PROJECT_ID=os.environ['DETECTION_PROJECT_ID']

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_API_KEY))

detection_credentials = ApiKeyCredentials(in_headers={"Prediction-key": DETECTION_KEY})
detection_client = CustomVisionPredictionClient(endpoint=DETECTION_ENDPOINT, credentials=detection_credentials)

# Create your views here.
def register(request):
    if request.session.get('id', False):
        return redirect('homepage')
    if request.method == "POST":

        aadhaar_no = request.POST['aadhaarNo']
        name = request.POST['name']
        dob = request.POST['dob']
        aadhaar_image = request.FILES['aadhaarImage']
        face_image = request.POST['faceImage']

        face_id = aadhaar_verification(request, aadhaar_no, name, dob, aadhaar_image)
        if face_id:
            face_match = face_verification(request, face_id, face_image)
            if face_match:
                request.session.set_expiry(300)
                request.session['id'] = aadhaar_no
                request.session['name'] = name
                request.session['dob'] = dob                    
                return redirect('homepage')
        else:
            messages.warning(request, ("Please Upload A Valid and Clear Image of Aadhaar Card!"))
    return render(request, 'register.html')

def aadhaar_verification(request, aadhaar_no, name, dob, aadhaar_image):
    aadhaar_img = None
    qr_img = None
    img_data = aadhaar_image
    try:
        prediction = detection_client.detect_image(DETECTION_PROJECT_ID, DETECTION_MODEL_NAME, img_data)
    except:
        messages.warning(request, ("Size of the aadhaar image must not exceed 4MB!"))
        return False
    img_open = Image.open(img_data)
    img = cv2.cvtColor(np.asarray(img_open), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (600, 600))
    for pred in prediction.predictions:
        if pred.probability > 0.8:
            bbox = pred.bounding_box
            x = int(bbox.left * img.shape[0])
            y = int(bbox.top * img.shape[1])
            width = x + int(bbox.width * img.shape[0])
            height = y + int(bbox.height * img.shape[1])
            if pred.tag_name == 'aadhaar':
                aadhaar_img = img[y:height, x:width]
            elif pred.tag_name == 'qr':
                qr_img = img[y:height, x:width]
    try:
        if type(aadhaar_img) == 'NoneType' or type(qr_img) == 'NoneType':
            if type(aadhaar_img) == 'NoneType':
                messages.warning(request, ("Aadhar Card not detected."))
            else:
                messages.warning(request, ("QR code not detected."))
            return False
    except:
        pass
    try:
        qr_img = cv2.resize(qr_img, (400, 400))
        code = decode(qr_img)
        qrData = code[0].data
    except:
        messages.warning(request, ("Unable to read QR code! Upload a clear Aadhaar Image."))
        return False
    secure = None
    old = None 
    isValid = False
    try:
        obj  = AadhaarSecureQr(qrData)
        print(obj.decodeddata())
        secure = obj.decodeddata()
        print("From Card: ", secure['adhaar_last_4_digit'], secure['name'], datetime.strptime(secure['dob'], "%d-%m-%Y"))
        print("From Input: ", str(aadhaar_no)[-4:], name.split(), datetime.strptime(dob, "%Y-%m-%d"))
        if secure['adhaar_last_4_digit'] == str(aadhaar_no)[-4:] and secure['name'] == name.strip() and datetime.strptime(secure['dob'], "%d-%m-%Y") == datetime.strptime(dob, "%Y-%m-%d"):
            isValid = True
        else:
            messages.warning(request, ("Aadhaar Details Does Not Match!!"))
            return False
    except:
        pass

    try:
        obj  = AadhaarOldQr(qrData)
        print(obj.decodeddata())
        old = obj.decodeddata()
        print("From Card: ", old['uid'], old['name'], datetime.strptime(old['dob'], "%d/%m/%Y"))
        print("Input: ", str(aadhaar_no), name.strip(), datetime.strptime(dob, "%Y-%m-%d"))
        if old['uid'] == str(aadhaar_no) and old['name'] == name.strip() and datetime.strptime(old['dob'], "%d/%m/%Y") == datetime.strptime(dob, "%Y-%m-%d"):
            isValid = True
        else:
            messages.warning(request, ("Aadhaar Details Does Not Match!!"))
            return False
    except:
        pass
    if isValid:
        messages.success(request, ("Aadhaar Verified Successfully!!"))
        print("Aadhaar Verified")
        ret,buf = cv2.imencode('.jpg', aadhaar_img) 
        stream = io.BytesIO(buf)
        print(type(stream))
        try:
            response_detected_faces = face_client.face.detect_with_stream(
                stream, 
                return_face_id=True,
                detection_model='detection_03',
                recognition_model='recognition_04'
            )
        except:
            print(type(stream))
            return False
        if response_detected_faces: 
            if len(response_detected_faces) == 1:
                person1 = response_detected_faces[0]
                print("Face Detected.")
                return person1.face_id
            else:
                messages.warning(request, ("More than one face detected in Aadhaar Image."))
    return False

def face_verification(request, id, face_image):
    temp = base64.b64decode(face_image)
    stream = io.BytesIO(temp)
    img_open = Image.open(stream).convert("RGBA")
    img = cv2.cvtColor(np.asarray(img_open), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (1024, 768))
    ret,buf = cv2.imencode('.jpg', img) 
    stream = io.BytesIO(buf)
    try:
        response_detected_faces = face_client.face.detect_with_stream(
            stream, 
            return_face_id=True,
            detection_model='detection_03',
            recognition_model='recognition_04'
        )
    except:
        print(type(face_image), "->", type(temp), "->", type(stream))
        messages.warning(request, ("Invalid input format for face image!"))
        return False
    if response_detected_faces:
        if len(response_detected_faces) == 0:
            messages.warning(request, ("No face detected!!"))
            return False
        person1 = response_detected_faces[0]
        id2 = person1.face_id
        face_verified = face_client.face.verify_face_to_face(
            face_id1=id,
            face_id2=id2
        )
        if not face_verified.is_identical:
            messages.warning(request, ("Face Does Not Match!!"))
            return False
        return face_verified.is_identical
    return False

def logout(request):
    request.session.flush()
    messages.success(request, ("Logged Out Successfully."))
    return redirect('register')

def details(request):
    return render(request, 'details.html')