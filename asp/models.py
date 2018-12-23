import datetime

from django.db import models

# Create your models here.

class Users(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    degree = models.IntegerField()
    letter = models.CharField(max_length=3)


class tasks(models.Model):
    taskname = models.CharField(max_length=100, unique=True)
    taskdesc = models.CharField(max_length=600)
    inputs = models.CharField(max_length=300)
    outputs = models.CharField(max_length=300)