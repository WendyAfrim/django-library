from django.http import HttpResponse
from django.shortcuts import render

from book.models import Library

def catalog(request):
    return HttpResponse('<h1>Hello Django!</h1>')

def login(request):
    return HttpResponse('<h1>Formulaire de connexion</h1>')

def librairies(request):
    librairies = Library.objects.all()
    return render(request, 'book/index.html', {
        'librairies' : librairies
    })