from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.all_books, name='all_books'),
    path('profile/', views.profile_view, name='profile'),
    path('audio/', views.audio_page, name='audio_page'),
    path('cart/', views.cart_view, name='cart'),
]

