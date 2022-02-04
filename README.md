# E-Voting-Platform #

A Microsoft Azure Based Web Application that can be used to conduct online voting.


## Microsoft Azure Services Used: ##

Serial Number | Azure Service        | Use
------------- | ---------------------|-------------
1             | Azure Web Apps       | Used for hosting the Web Application
2             | Azure Face API       | Used for face verification with the face on Aadhaar Card 
3             | Azure Custom Vision  | Used to detect and extract Aadhaar Card Image and QR code from the image uploaded by voter


## Links For Application:
#### For Voting: ####
  * https://e-voting-platform.azurewebsites.net/account/register
#### For Admin Login to view results: ####
  * https://e-voting-platform.azurewebsites.net/admin_account/login
    * Username: kashish
    * Password: adminlogin
    
## How To Vote: ##
1. Go to the link: https://e-voting-platform.azurewebsites.net/account/register
2. For face verification, click on "Capture Image For Face Verification" and capture a clear image of your face. Ensure that your face is visible properly in the captured image. After capturing image a form will appear.
3. Enter your 12 Digit Aadhaar Number
4. Enter your name as written on your Aadhaar Card.
5. Enter your DOB (Date of Birth)
6. Upload A Clear Image Of Your Aadhaar Card in jpg or png format only. The file size must not exceed 4MB.
7. After successful aadhaar and face verification you will be allowed to vote.

## How To Check Results: ##
1. Go to the link: https://e-voting-platform.azurewebsites.net/admin_account/login
2. Login using admin credentials given above.
3. Check the results.
