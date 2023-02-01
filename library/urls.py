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
    path("book/<int:book_id>/borrow", views.borrow_book, name="book_borrow"),
    path("book/<int:book_id>/return", views.return_book, name="book_return"),
    path("libraries", views.libraries, name="libraries"),
    path("dashboard", views.dashboard, name="dashboard"),
]