from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Custom_User(AbstractUser):
    pass


class NGOProfile(models.Model):
    user=models.OneToOneField(Custom_User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mission = models.TextField()
    # contact_email = models.EmailField() 
    verification_status = models.BooleanField(default=False)

class Verificationrequest(models.Model):
    ngo_profile=models.OneToOneField(NGOProfile,on_delete=models.CASCADE)
    document_upload = models.FileField(upload_to='verifications/documents/')
    status= models.CharField(max_length=20)
    

class SDG(models.Model):
    name = models.CharField(max_length=50)  
    description=models.TextField()

class Project(models.Model):
    title=models.CharField(max_length=150)
    description= models.TextField()
    ngo = models.ForeignKey(NGOProfile,on_delete=models.CASCADE)
    sdgs = models.ManyToManyField(SDG)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20)


class VolunteerApplication(models.Model):
    volunteer = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

class Donation(models.Model):
    donor_name=models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2)                
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    donation_date = models.DateField()

class Anayltics(models.Model):
    project = models.OneToOneField(Project,on_delete=models.CASCADE)
    volunteer_count= models.IntegerField(default=0)
    total_donations = models.DecimalField(max_digits=12,decimal_places=2,default=0.0)


