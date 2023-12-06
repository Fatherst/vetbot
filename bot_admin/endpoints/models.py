from django.db import models
from client_auth.models import Client

class Kind(models.Model):
    id = models.IntegerField(primary_key=True)
    enote_id = models.CharField(max_length=200)
    name = models.CharField(max_length=250)

class Breed(models.Model):
    id = models.IntegerField(primary_key=True)
    enote_id = models.CharField(max_length=150)
    name = models.CharField(max_length=200)
    kind = models.ForeignKey(Kind,on_delete=models.CASCADE)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    enote_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    birth_date = models.DateField()
    weight = models.CharField(max_length=20)
    time_of_death = models.DateTimeField(default='')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    kind = models.ForeignKey(Kind, on_delete=models.PROTECT)

class VisitKind(models.Model):
    enote_id = models.CharField(max_length=250)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)

class Specialization(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)

class Doctor(models.Model):
    client_enote_id = models.CharField(max_length=150)
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, default="")
    middle_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT)
    position = models.CharField(max_length=250)
    photo = models.ImageField()
    detail_info = models.TextField(default='')


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    enote_id = models.CharField(max_length=200)
    type = models.CharField(max_length=250,default='')
    new_client = models.BooleanField(default=True)
    status = models.CharField(max_length=250,default='')
    date = models.DateField()
    start_time = models.TimeField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    visit_kind = models.ForeignKey(VisitKind,on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor,on_delete=models.PROTECT)
