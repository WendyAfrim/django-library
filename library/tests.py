from django.test import TestCase
from django.db import models

# Create your tests here.
class ReadingGroups(models.Model):
    name          = models.fields.CharField(max_length=100)
    capacity      = models.IntegerField()
    description   = models.TextField()

class User(models.Model):
    firstname       = models.fields.CharField(max_length=100)
    lastname        = models.fields.CharField(max_length=100)
    roles           = models.fields.CharField(max_length=100)
    reading_groups  = models.ForeignKey(ReadingGroups, on_delete=models.CASCADE)

class Library(models.Model):
    name          = models.fields.CharField(max_length=100)
    department    = models.fields.IntegerField()

class Book(models.Model):
    title           = models.fields.CharField(max_length=100)
    author          = models.fields.CharField(max_length=100)
    cover           = models.fields.CharField(max_length=100)
    editor          = models.fields.CharField(max_length=100)
    collection      = models.fields.CharField(max_length=100)
    gender          = models.fields.CharField(max_length=100)
    libraries       = models.ManyToManyField(Library)
    was_borrowed    = models.fields.CharField(max_length=100)

class Session(models.Model):
    name           = models.fields.CharField(max_length=100)
    time           = models.IntegerField()
    reading_groups = models.ForeignKey(ReadingGroups, on_delete=models.CASCADE)


class Borrowing(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at  = models.DateField()
    due_at      = models.DateField()
