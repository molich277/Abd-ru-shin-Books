from .forms import UserForm
from .models import UserProfile
from .forms import UserProfileForm # Add this line
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from .models import Book
from .forms import ContactForm # <--- ADD THIS LINE
import json

# ... (existing views)

def home_view(request):
    # No complex logic needed for a simple static homepage
    return render(request, 'books/home.html')
    
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile) # request.FILES for profile_picture

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile was successfully updated!') # Consider adding Django messages
            return redirect('books:profile') # <--- CHANGE THIS LINE
        else:
            pass # Forms are invalid, they will display errors on the template
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'books/profile.html', context)
                
    # Get free PDFs for Book 1
    book_one = Book.objects.filter(title__icontains="In The Light of Truth - Book 1").first()
    free_chapters = []
    if book_one:
        free_chapters = FreePDF.objects.filter(book=book_one).order_by('chapter_number')[:3] # Get first 3

    return render(request, 'books/profile.html', {'form': form, 'free_chapters': free_chapters})

@login_required
def read_free_pdf(request, pdf_id):
    pdf_chapter = get_object_or_404(FreePDF, id=pdf_id)

    # Check if user has access (e.g., profile completed)
    if not request.user.userprofile.has_access_to_book_one_chapters:
        raise Http404("You do not have access to this chapter.")

    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_chapter.pdf_file.name)
    if not os.path.exists(pdf_path):
        raise Http404("PDF file not found.")

    with open(pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="%s"' % os.path.basename(pdf_path)
        return response

# Define how many recently viewed books to store
MAX_RECENTLY_VIEWED = 5

# books/views.py

# ... (your existing imports and other views) ...

def all_books(request):
    # Fetch ALL books, regardless of whether they are 'main_book' or not
    all_books_data = Book.objects.all().order_by('title')
    return render(request, 'books/all_books.html', {'books': all_books_data})

# ... (your other views like book_detail, profile_view, etc.) ...

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # --- Cookie Logic for Recently Viewed Books ---
    recently_viewed_ids = json.loads(request.COOKIES.get('recently_viewed_books', '[]'))

    # Add the current book's ID to the list, ensure uniqueness and order
    if book.id in recently_viewed_ids:
        recently_viewed_ids.remove(book.id) # Move to front if already exists
    recently_viewed_ids.insert(0, book.id) # Add to the beginning

    # Keep only the last N viewed books
    recently_viewed_ids = recently_viewed_ids[:MAX_RECENTLY_VIEWED]

    context = {
        'book': book,
        # You can add other context variables here if needed
    }
    response = render(request, 'books/book_detail.html', context)

    # Set the cookie on the response
    # max_age: e.g., 30 days (30 * 24 * 60 * 60 seconds)
    # httponly=True: Prevents JavaScript access, good for sensitive data but not strictly needed for this
    # secure=True: Ensures cookie is only sent over HTTPS (recommended for production)
    response.set_cookie(
        'recently_viewed_books',
        json.dumps(recently_viewed_ids),
        max_age=30 * 24 * 60 * 60, # 30 days
        httponly=False, # We might want JS to read this if we build client-side features
        secure=request.is_secure() # Use secure if the request is HTTPS
    )
    # --- End Cookie Logic ---

    return response

def recently_viewed_books_list(request):
    recently_viewed_ids = json.loads(request.COOKIES.get('recently_viewed_books', '[]'))
    
    # Filter books by IDs, maintaining the order of viewing
    # Using a list comprehension to preserve order
    viewed_books = []
    if recently_viewed_ids:
        # Fetch all books with those IDs in one query
        # Use Book.objects.in_bulk to get a dict mapping id to book object
        # then iterate over ordered IDs to retrieve books
        all_viewed_books_map = Book.objects.in_bulk(recently_viewed_ids)
        for book_id in recently_viewed_ids:
            if book_id in all_viewed_books_map:
                viewed_books.append(all_viewed_books_map[book_id])

    context = {
        'viewed_books': viewed_books,
    }
    return render(request, 'books/recently_viewed_books.html', context)

# Your existing home view (modify to display recently viewed books)
def home(request):
    main_books = Book.objects.filter(is_main_book=True).order_by('order')

    # Optionally, also display recently viewed books on the home page
    recently_viewed_ids = json.loads(request.COOKIES.get('recently_viewed_books', '[]'))
    viewed_books = []
    if recently_viewed_ids:
        all_viewed_books_map = Book.objects.in_bulk(recently_viewed_ids)
        for book_id in recently_viewed_ids:
            if book_id in all_viewed_books_map:
                viewed_books.append(all_viewed_books_map[book_id])

    context = {
        'main_books': main_books,
        'recently_viewed_books': viewed_books, # Pass this to the template
    }
    return render(request, 'books/home.html', context)
@login_required # Ensure this decorator is imported if used: from django.contrib.auth.decorators import login_required
def audio_page(request):
    books_with_audios = Book.objects.filter(audio__isnull=False).distinct()

    user_audio_access = {}
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        user_audio_access['book_one'] = user_profile.audio_access_book_one
        user_audio_access['book_two'] = user_profile.audio_access_book_two
        user_audio_access['book_three'] = user_profile.audio_access_book_three

    context = {
        'books': books_with_audios,
        'user_audio_access': user_audio_access,
    }
    return render(request, 'books/audio_page.html', context)
# books/views.py

# ... (other imports and views) ...

@login_required # Ensure this decorator is imported if used
def cart_view(request):
    # Your cart view logic here (currently just renders the template)
    return render(request, 'books/cart.html')
# books/views.py

# ... (your existing imports) ...

# ... (your existing views) ...

def cart_view(request):
    """
    Renders the shopping cart page.
    """
    return render(request, 'books/cart.html')
# books/views.py

# ... (your existing imports) ...

# ... (your existing views) ...

# books/views.py

# ... (your existing imports and other views) ...

def contact_view(request):
    success_message = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # For now, we'll just print to the console and set a success message.
            # Later, this is where you would send the email.
            print(f"Contact Form Submission:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Message: {message}")

            success_message = 'Your message has been sent successfully!'
            form = ContactForm() # Clear the form after successful submission
    else:
        form = ContactForm() # An empty form for GET requests

    context = {
        'form': form,
        'success_message': success_message,
    }
    return render(request, 'books/contact.html', context)

# ... (any other views below this) ...
# books/views.py

# ... (your existing imports at the top) ...

# ... (all your other existing views like home, all_books, book_detail, profile_view, audio_page, cart_view, contact_view, etc.) ...


def grail_message_view(request):
    """
    Renders the page about The Grail Message / Writings of Abd-ru-shin.
    """
    return render(request, 'books/grail_message.html')
# books/views.py

# ... (your existing imports at the top) ...

# ... (all your other existing views like home, all_books, book_detail, profile_view, audio_page, cart_view, contact_view, etc.) ...

def grail_message_view(request):
    """
    Renders the page about The Grail Message / Writings of Abd-ru-shin.
    """
    return render(request, 'books/grail_message.html')

# ADD THIS NEW FUNCTION DIRECTLY BELOW grail_message_view:
def in_the_light_of_truth_detail_view(request):
    """
    Renders the detail page for 'In the Light of Truth - The Grail Message'.
    """
    return render(request, 'books/in_the_light_of_truth_detail.html')

# ... (If you have any other views or code after this, keep them) ...
def privacy_policy_view(request):
    return render(request, 'books/privacy_policy.html')

def terms_of_use_view(request):
    return render(request, 'books/terms_of_use.html')
    
# ... (If you have any other views or code after this, keep them) ...
# ... (any other views below this) ...
# ... (any other views below this) ...
# ... (rest of your views) ...
# ... (rest of your views) ...
