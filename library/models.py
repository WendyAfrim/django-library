from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

# Create your models here.
class ReadingGroup(models.Model):
    name          = models.fields.CharField(max_length=100)
    capacity      = models.IntegerField()
    description   = models.TextField()
    users        = models.ManyToManyField('User', related_name='reading_groups', blank=True)
    sessions      = models.ManyToManyField('Session', related_name='reading_groups', blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):

    def is_bookseller(self):
        return self.groups.filter(name='bookseller_grp').exists()

    def is_customer(self):
        return self.groups.filter(name='customer_grp').exists()

class Library(models.Model):
    name          = models.fields.CharField(max_length=100)
    department    = models.fields.CharField(max_length=100)
    address       = models.fields.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Borrowing(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    due_at      = models.DateTimeField()

class Book(models.Model):
    title           = models.fields.CharField(max_length=100)
    author          = models.fields.CharField(max_length=100)
    cover           = models.fields.URLField(null=True, blank=True)
    editor          = models.fields.CharField(max_length=100)
    collection      = models.fields.CharField(max_length=100)
    gender          = models.fields.CharField(max_length=100)
    libraries       = models.ManyToManyField(Library)
    borrowing       = models.OneToOneField(Borrowing, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Session(models.Model):
    name           = models.fields.CharField(max_length=100)
    datetime       = models.DateTimeField()

    def __str__(self):
        return self.name

