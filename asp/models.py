from django.db import models
import datetime
# Create your models here.


class tasks(models.Model):
    taskname = models.CharField(max_length=150, unique=True)
    taskdesc = models.CharField(max_length=1000)
    inputs = models.CharField(max_length=5000)
    outputs = models.CharField(max_length=5000)
    category = models.CharField(max_length=300)
    testin = models.CharField(max_length=1200, default='тест не найден')
    testout = models.CharField(max_length=1200, default='тест не найден')


class Users(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    degree = models.IntegerField()
    letter = models.CharField(max_length=5)
    role = models.CharField(max_length=20, default="student")


class Solution(models.Model):
    time = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    task = models.ForeignKey(tasks, on_delete=models.CASCADE, default=None)
    points = models.IntegerField()
    status = models.CharField(max_length=50)
    file = models.FileField(default=None)
    lang = models.CharField(max_length=100, default=None)
    tests = models.CharField(max_length=2500, default="0")


class Compiler(models.Model):
    name = models.CharField(max_length=128)
    needCompilation = models.BooleanField()
    path = models.FilePathField()
    params = models.CharField(max_length=250, default='')
    extention = models.CharField(max_length=30, default='')


class Theme(models.Model):
    theme = models.CharField(max_length=1000)
