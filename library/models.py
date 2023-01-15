from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

# Create your models here.
class ReadingGroups(models.Model):
    name          = models.fields.CharField(max_length=100)
    capacity      = models.IntegerField()
    description   = models.TextField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    reading_groups  = models.ForeignKey(ReadingGroups, on_delete=models.CASCADE, null=True, blank=True)

    def is_bookseller(self):
        return self.groups.filter(name='bookseller_grp').exists()

    def is_customer(self):
        return self.groups.filter(name='customer_grp').exists()

class Library(models.Model):
    name          = models.fields.CharField(max_length=100)
    department    = models.fields.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title           = models.fields.CharField(max_length=100)
    author          = models.fields.CharField(max_length=100)
    cover           = models.fields.URLField(null=True, blank=True)
    editor          = models.fields.CharField(max_length=100)
    collection      = models.fields.CharField(max_length=100)
    gender          = models.fields.CharField(max_length=100)
    libraries       = models.ManyToManyField(Library)
    was_borrowed    = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Session(models.Model):
    name           = models.fields.CharField(max_length=100)
    datetime       = models.DateTimeField() 
    reading_groups = models.ForeignKey(ReadingGroups, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Borrowing(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at  = models.DateField()
    due_at      = models.DateField()
