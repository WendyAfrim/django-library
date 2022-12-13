from django.db import models
# from login.models import User
from book.models import Book

class Library(models.Model):
    name          = models.fields.CharField(max_length=100)
    department    = models.fields.IntegerField()


class ReadingGroups(models.Model):
    name          = models.fields.CharField(max_length=100)
    capacity      = models.IntegerField()
    description   = models.TextField()

class Session(models.Model):
    name           = models.fields.CharField(max_length=100)
    time           = models.IntegerField()
    reading_groups = models.ForeignKey(ReadingGroups, on_delete=models.CASCADE)


class Borrowing(models.Model):
    user        = models.ForeignKey('login.User', on_delete=models.CASCADE)
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at  = models.DateField()
    due_at      = models.DateField()
