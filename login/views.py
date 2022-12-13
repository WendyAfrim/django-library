from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    return HttpResponse('<h1>Formulaire de connexion</h1>')
