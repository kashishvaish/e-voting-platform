from typing_extensions import Required
from django import forms

class CustomRegisterForm(forms.Form):
    aadhaar_no = forms.IntegerField(min_value=100000000000, max_value=999999999999)
    name = forms.CharField(max_length=50)
    dob = forms.DateField(input_formats=['%d/%m/%Y'])
    aadhaar_image = forms.ImageField()