from django.db import models
from django.contrib.auth.models import AbstractUser
from library.models import ReadingGroups

# Create your models here.
class User(AbstractUser):

    firstname       = models.fields.CharField(max_length=100)
    lastname        = models.fields.CharField(max_length=100)
    email           = models.fields.CharField(max_length=254, default='null')
    password        = models.fields.CharField(max_length=12, default='null')
    roles           = models.fields.CharField(max_length=100)
    reading_groups  = models.ForeignKey(ReadingGroups, on_delete=models.CASCADE)