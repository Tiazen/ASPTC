from django.db import models
import datetime
# Create your models here.


class tasks(models.Model):
    taskname = models.CharField(max_length=100, unique=True)
    taskdesc = models.CharField(max_length=600)
    inputs = models.CharField(max_length=300)
    outputs = models.CharField(max_length=300)
    category = models.CharField(max_length=300)
    testin = models.CharField(max_length=300, default='тест не найден')
    testout = models.CharField(max_length=300, default='тест не найден')

class Users(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    degree = models.IntegerField()
    letter = models.CharField(max_length=3)
    role = models.CharField(max_length=20, default="student")

class Solution(models.Model):
    time = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    task = models.IntegerField(default=0)
    points = models.IntegerField()
    status = models.CharField(max_length=50)
    file = models.FileField(default=None)
    lang = models.CharField(max_length=100, default="Python 3.7.0")
