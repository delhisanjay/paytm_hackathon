from django.contrib.auth.models import User
from django.db import models

class Patient_Detail(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    adhar = models.IntegerField(null=True, blank=True)
    email= models.EmailField(max_length=50, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    gender=models.CharField(max_length=6)
    dob=models.CharField(max_length=20)
    age=models.IntegerField(null=True, blank=True)
    report=models.FileField(upload_to = 'report')

    def __str__(self):
        return str(self.adhar)

class Doctor_Detail(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo=models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpg')
    adhar = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.first_name


class Doctor_Profile(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True, blank=True)
    city=models.CharField(max_length=50)
    category=models.CharField(max_length=50)


class Appointment(models.Model):
    doctor_name = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=50)
    time=models.CharField(max_length=50)
    phone=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.patient_name