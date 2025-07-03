from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile, Book

def home(request):
    main_books = Book.objects.filter(is_main_book=True).order_by('title') # Changed 'order' to 'title'
    context = {
        'main_books': main_books
    }
    return render(request, 'books/home.html', context)

def all_books(request):
    # Display other books
    other_books = Book.objects.filter(is_main_book=False).order_by('title')
    return render(request, 'books/all_books.html', {'other_books': other_books})

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('books:profile') # Redirect to profile page after save
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'books/profile.html', {'form': form})

@login_required
def audio_page(request):
    # Logic for free/paid audios will go here
    # For now, just a placeholder
    return render(request, 'books/audio_page.html')

@login_required
def cart_view(request):
    # Cart logic will go here
    return render(request, 'books/cart.html')
