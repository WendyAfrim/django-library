from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("books", views.books, name="books"),
    path("book/<int:book_id>", views.book, name="book"),
    path("books/add", views.add_book, name="book_add"),
    path("book/<int:book_id>/update", views.update_book, name="book_update"),
    path("book/<int:book_id>/delete", views.delete_book, name="book_delete"),
]