from django.test import TestCase
from django.db import models

# Create your tests here.
class ReadingGroup(models.Model):
    name          = models.fields.CharField(max_length=100)
    capacity      = models.IntegerField()
    description   = models.TextField()
    users        = models.ManyToManyField('User', related_name='reading_groups', blank=True)
    sessions      = models.ManyToManyField('Session', related_name='reading_groups', blank=True)

class User(models.Model):
    firstname       = models.fields.CharField(max_length=100)
    lastname        = models.fields.CharField(max_length=100)
    roles           = models.fields.CharField(max_length=100)

class Library(models.Model):
    name          = models.fields.CharField(max_length=100)
    department    = models.fields.IntegerField()
    address       = models.fields.CharField(max_length=100)

class Borrowing(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateField()
    due_at      = models.DateField()

class Book(models.Model):
    title           = models.fields.CharField(max_length=100)
    author          = models.fields.CharField(max_length=100)
    cover           = models.fields.CharField(max_length=100)
    editor          = models.fields.CharField(max_length=100)
    collection      = models.fields.CharField(max_length=100)
    gender          = models.fields.CharField(max_length=100)
    libraries       = models.ManyToManyField(Library)
    borrowing      = models.ForeignKey(Borrowing, on_delete=models.CASCADE)

class Session(models.Model):
    name           = models.fields.CharField(max_length=100)
    time           = models.IntegerField()
