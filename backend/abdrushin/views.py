from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Audio

def home(request):
    main_books = Book.objects.filter(is_main_book=True)
    other_books = Book.objects.filter(is_main_book=False)
    return render(request, "home.html", {
        "main_books": main_books,
        "other_books": other_books,
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    audios = book.audios.all()
    return render(request, "book_detail.html", {
        "book": book,
        "audios": audios,
    })

def other_writings(request):
    books = Book.objects.filter(is_main_book=False)
    return render(request, "other_writings.html", {"books": books})

def audio_page(request):
    books = Book.objects.all()
    return render(request, "audio.html", {"books": books})

def contact(request):
    return render(request, "contact.html")
