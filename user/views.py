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

FACE_API_KEY=config('FACE_API_KEY')
FACE_ENDPOINT=config('FACE_ENDPOINT')
DETECTION_KEY=config('DETECTION_KEY')
DETECTION_ENDPOINT=config('DETECTION_ENDPOINT')
DETECTION_MODEL_NAME=config('DETECTION_MODEL_NAME')
DETECTION_PROJECT_ID=config('DETECTION_PROJECT_ID')

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_API_KEY))

detection_credentials = ApiKeyCredentials(in_headers={"Prediction-key": DETECTION_KEY})
detection_client = CustomVisionPredictionClient(endpoint=DETECTION_ENDPOINT, credentials=detection_credentials)

# Create your views here.
def register(request):
    if request.session.get('id', False):
        return redirect('homepage')
    if request.method == "POST":
        register_form = CustomRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            face_id = aadhaar_verification(register_form)
            if face_id:
                face_match = face_verification(face_id)
                if face_match:
                    request.session.set_expiry(300)
                    request.session['id'] = register_form.cleaned_data['aadhaar_no']
                    request.session['name'] = register_form.cleaned_data['name']
                    request.session['dob'] = register_form.cleaned_data['dob'].strftime("%d/%m/%Y")                    
                    return redirect('homepage')
                messages.warning(request, ("Face Is Not Identical With Aadhaar Image!"))
            else:
                messages.warning(request, ("Please Upload A Valid and Clear Image of Aadhaar Card!"))
    else:
        register_form = CustomRegisterForm()
    return render(request, 'register.html', {'register_form': register_form})

def aadhaar_verification(register_form):
    aadhaar_img = None
    qr_img = None
    img_data = register_form.cleaned_data['aadhaar_image']
    prediction = detection_client.detect_image(DETECTION_PROJECT_ID, DETECTION_MODEL_NAME, img_data)
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
            print("Aadhar Card or QR code not detected.")
            return False
    except:
        pass
    try:
        code = decode(qr_img)
        qrData = code[0].data
        qrDict = dict(xmltodict.parse(qrData))
    except:
        print("QR code not detected.")
        return False
    if qrDict:
        if 'PrintLetterBarcodeData' in qrDict:
            details = dict(qrDict['PrintLetterBarcodeData'])
            if ['@uid', '@name', '@gender', '@yob', '@co', '@house', '@street', '@lm', '@loc', '@vtc', '@po', '@dist', '@subdist', '@state', '@pc', '@dob'] == list(details.keys()):
                uid = int(details['@uid'])
                name = details['@name']
                dob = details['@dob']
                uid_input = register_form.cleaned_data['aadhaar_no']
                name_input = register_form.cleaned_data['name']
                dob_input = register_form.cleaned_data['dob'].strftime("%d/%m/%Y")
                if uid_input == uid and name_input == name and dob_input == dob:
                    print("Aadhaar Verified")
                    ret,buf = cv2.imencode('.jpg', aadhaar_img) 
                    stream = io.BytesIO(buf)
                    response_detected_faces = face_client.face.detect_with_stream(
                        stream, 
                        return_face_id=True,
                        detection_model='detection_03',
                        recognition_model='recognition_04'
                    )
                    if response_detected_faces and len(response_detected_faces) == 1:
                        person1 = response_detected_faces[0]
                        print("Face Detected.")
                        return person1.face_id
    return False

def face_verification(id):
    cap=cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        ret,buf = cv2.imencode('.jpg', img) 
        stream = io.BytesIO(buf)
        response_detected_faces = face_client.face.detect_with_stream(
            stream, 
            return_face_id=True,
            detection_model='detection_03',
            recognition_model='recognition_04'
        )
        if response_detected_faces:
            person1 = response_detected_faces[0]
            id2 = person1.face_id
            face_verified = face_client.face.verify_face_to_face(
                face_id1=id,
                face_id2=id2
            )
            return face_verified.is_identical
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    cap.release()
    return False

def logout(request):
    request.session.flush()
    messages.success(request, ("Logged Out Successfully."))
    return redirect('register')

def details(request):
    return render(request, 'details.html')