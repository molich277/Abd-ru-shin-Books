from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('other-writings/', views.other_writings, name='other_writings'),
    path('audio/', views.audio_page, name='audio'),
    path('contact/', views.contact, name='contact'),
]
