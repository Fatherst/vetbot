from django.db import models


class Client(models.Model):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    clientEnoteId = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=100, default="")
    middleName = models.CharField(max_length=100, default="")
    lastName = models.CharField(max_length=100, default="")
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12, default="")
    clientTelegramId = models.IntegerField(null=True)


class Patient(models.Model):
    patientEnoteId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    birthDate = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    timeOfDeath = models.DateTimeField()
    breedEnoteId = models.IntegerField()
    kindEnoteId = models.IntegerField()
    objectState = models.CharField(choices="", max_length=100)
    clientEnoteId = models.ForeignKey(Client, on_delete=models.CASCADE)


class Kind(models.Model):
    kindEnoteId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)


class Breed(models.Model):
    breedEnoteId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    kindEnoteId = models.ForeignKey(Kind, on_delete=models.CASCADE)

class Doctor(models.Model):
    doctorEnoteId = models.IntegerField(primary_key=True)


class VisitKind(models.Model):
    visitKindId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)


class Appointment(models.Model):
    appointmentType = models.CharField(max_length=150)
    appointmentStatus = models.CharField(max_length=150)
    clientEnoteId = models.ForeignKey(Client, on_delete=models.CASCADE)
    patientEnoteId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visitKindId = models.ForeignKey(VisitKind, on_delete=models.CASCADE)
    appointmentDate = models.DateField()
    startTime = models.TimeField()
    doctorEnoteId = models.ForeignKey(Doctor, on_delete=models.CASCADE)