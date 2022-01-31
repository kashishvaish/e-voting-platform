from django.db import models

# Create your models here.
class VotersList(models.Model):
    aadhaar_no = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=70)
    dob = models.DateField()

class Votes(models.Model):
    candidate = models.CharField(max_length=100, primary_key=True)
    votes = models.IntegerField()