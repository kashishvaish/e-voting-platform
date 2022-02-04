# E-Voting-Platform #

A Microsoft Azure Based Web Application that can be used to conduct online voting.


## Microsoft Azure Services Used: ##

Serial Number | Azure Service        | Use
------------- | ---------------------|-------------
1             | Azure Web Apps       | Used for hosting Web Application
2             | Azure Face API       | Used for face verification with Aadhaar Image 
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
2. Enter your correct details, these details will be verified by scanning your Aadhaar QR code.
3. Upload a clear scanned image of your Aadhaar Card, your QR code must be clear in the uploaded image.
4. Click on "Capture Image for Face Verification" and click your image, your face must be clearly visible.
5. Click on proceed.
4. After successful aadhaar and face verification you will be allowed to vote.

## How To Check Results: ##
1. Go to the link: https://e-voting-platform.azurewebsites.net/admin_account/login
2. Login using admin credentials given above.
3. Check the results.
