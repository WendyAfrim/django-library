from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render

from book.forms import BookForm
from book.models import Book

def createBook(request):

    if request.method == 'POST':
        
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return HttpResponseRedirect('book_detail', kwargs={'id' : book.id})
    else: 
        form = BookForm()
    return render(request, 'book/add.html', {
        'form' : form
    })


def detail(request, id):
    books = Book.objects.all()
    breakpoint()
    context = {
        'books' : books
    }
    return render(
        request, 
        'book/detail.html', 
        context
    )
