# books/admin.py
from django.contrib import admin
from .models import Book, Audio, FreePDF, UserProfile

# Register your models here.
admin.site.register(Book)
admin.site.register(Audio)
admin.site.register(FreePDF)
admin.site.register(UserProfile)
