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
    path("library/<int:library_id>", views.library, name="library"),
    path("libraries", views.libraries, name="libraries"),
    path("reading-groups", views.reading_groups, name="reading_groups"),
    path("reading-groups/add", views.add_reading_group, name="reading_group_add"),
    path("reading-groups/<int:reading_group_id>", views.reading_group, name="reading_group"),
    # path("reading_group/<int:reading_group_id>/update", views.update_reading_group, name="reading_group_update"),
    path("reading-groups/<int:reading_group_id>/delete", views.delete_reading_group, name="reading_group_delete"),
    path("reading-groups/<int:reading_group_id>/join", views.join_reading_group, name="reading_group_join"),
    path("reading-groups/<int:reading_group_id>/leave", views.leave_reading_group, name="reading_group_leave"),
    path("dashboard", views.dashboard, name="dashboard"),
]