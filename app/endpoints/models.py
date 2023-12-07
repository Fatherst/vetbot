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
    weight = models.FloatField()
    time_of_death = models.DateTimeField(default='')
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    kind = models.ForeignKey(Kind, on_delete=models.PROTECT)
