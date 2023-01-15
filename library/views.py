import base64
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from .util import get_book_cover_url, upload_image_to_imgbb
from .models import User, Book, Library


def index(request):
    trending_books = Book.objects.all().order_by("?")[:3]
    return render(request, "library/index.html", {"trending_books": trending_books})

def search(request):
    query = request.GET.get("q") if request.GET.get("q") else ""
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.none()
    context = {
        "query": query,
        "books": books,
    }
    return render(request, "library/search.html", context)

@user_passes_test(User.is_bookseller)
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    libraries = Library.objects.all()
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        if request.FILES.get("cover"):
            b64 = base64.b64encode(request.FILES.get("cover").read())
            imgbb_url = upload_image_to_imgbb(b64) or book.cover
            book.cover = imgbb_url
        book.editor = request.POST.get("editor")
        book.collection = request.POST.get("collection")
        book.gender = request.POST.get("gender")
        libraries = request.POST.getlist("libraries")
        book.libraries.clear()
        for library_id in libraries:
            library = Library.objects.get(id=library_id)
            book.libraries.add(library)
        book.was_borrowed = request.POST.get("was_borrowed") == "on"
        book.save()
        return redirect("book", book_id=book.id)
    return render(request, "library/book_update.html", {"book": book, "libraries": libraries})

@user_passes_test(User.is_bookseller)
def add_book(request):
    libraries = Library.objects.all()
    if request.method == "POST":
        book = Book()
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        if request.FILES.get("cover"):
            b64 = base64.b64encode(request.FILES.get("cover").read())
            imgbb_url = upload_image_to_imgbb(b64) or book.cover
            book.cover = imgbb_url
        else:
            book.cover = get_book_cover_url(request.POST.get("title"), request.POST.get("author"))
        book.editor = request.POST.get("editor")
        book.collection = request.POST.get("collection")
        book.gender = request.POST.get("gender")
        libraries = request.POST.getlist("libraries")
        for library_id in libraries:
            library = Library.objects.get(id=library_id)
            book.libraries.add(library)
        book.was_borrowed = request.POST.get("was_borrowed") == "on"
        book.save()
        return redirect("book", book_id=book.id)
    return render(request, "library/book_add.html", {"libraries": libraries})

@user_passes_test(User.is_bookseller)
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect("books")

def books(request):
    books = Book.objects.all()
    return render(request, "library/books.html", {"books": books})

def book(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "library/book.html", {"book": [book]})
