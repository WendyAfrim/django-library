import email
from operator import mod
from time import time
from django.db import models

class Book(models.Model):
    title           = models.fields.CharField(max_length=100)
    author          = models.fields.CharField(max_length=100)
    cover           = models.fields.CharField(max_length=100)
    editor          = models.fields.CharField(max_length=100)
    collection      = models.fields.CharField(max_length=100)
    gender          = models.fields.CharField(max_length=100)
    libraries       = models.ForeignKey('library.Library', on_delete=models.CASCADE)
    was_borrowed    = models.fields.CharField(max_length=100)
