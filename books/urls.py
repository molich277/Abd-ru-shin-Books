# books/urls.py

from django.urls import path
from . import views

app_name = 'books' # Make sure this line exists for {% url 'books:...' %}

urlpatterns = [
    path('', views.home_view, name='home'),
    path('all-books/', views.all_books, name='all_books'), # Ensure this line is present
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('recently-viewed/', views.recently_viewed_books_list, name='recently_viewed_books'),
    path('profile/', views.profile_view, name='profile'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'), # <--- ADD THIS
    path('terms-of-use/', views.terms_of_use_view, name='terms_of_use'),  
    path('audio/', views.audio_page, name='audio_page'), # <--- ADD THIS LINE
    path('cart/', views.cart_view, name='cart'), # <--- ADD THIS LINE
    path('contact/', views.contact_view, name='contact'),
    path('grail-message/', views.grail_message_view, name='grail_message'),
    path('grail-message/in-the-light-of-truth/', views.in_the_light_of_truth_detail_view, name='in_the_light_of_truth_detail'), # <--- THIS LINE WAS MISSING 
    # ... any other paths you have or will add later ...
    # ... other paths ...
]
