from django.urls import path
from book import views

urlpatterns = [
    path('book/add', views.createBook, name='book_add'),
    path('book/<int:id>', views.detail, name='book_detail'),
]
