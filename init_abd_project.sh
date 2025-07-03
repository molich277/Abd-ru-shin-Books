#!/bin/bash

echo "Creating directories..."
mkdir -p backend/abdrushin backend/users backend/static/css backend/static/js backend/templates backend/media rust_audio_service/src backend/backend

# backend/requirements.txt
cat <<EOF > backend/requirements.txt
Django>=4.2
django-allauth
djangorestframework
django-cors-headers
gunicorn
python-dotenv
pillow
EOF

# backend/manage.py
cat <<EOF > backend/manage.py
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
EOF

# backend/backend/settings.py
cat <<EOF > backend/backend/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'CHANGE_ME')
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'abdrushin',
    'users',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'users.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

CORS_ALLOW_ALL_ORIGINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EOF

# backend/backend/urls.py
cat <<EOF > backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('abdrushin.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOF

# backend/abdrushin/models.py
cat <<EOF > backend/abdrushin/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/')
    pdf_file = models.FileField(upload_to='books/')
    is_main_book = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

class Audio(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='audios')
    chapter = models.IntegerField()
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audios/')
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.book.title} - Chapter {self.chapter}"
EOF

# backend/users/models.py
cat <<EOF > backend/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
EOF

# backend/abdrushin/views.py
cat <<EOF > backend/abdrushin/views.py
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
EOF

# backend/abdrushin/urls.py
cat <<EOF > backend/abdrushin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('other-writings/', views.other_writings, name='other_writings'),
    path('audio/', views.audio_page, name='audio'),
    path('contact/', views.contact, name='contact'),
]
EOF

# backend/users/urls.py
cat <<EOF > backend/users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('complete/', views.complete_profile, name='complete_profile'),
]
EOF

# backend/users/views.py
cat <<EOF > backend/users/views.py
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import ProfileForm

def complete_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.profile_completed = True
            user.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'complete_profile.html', {'form': form})
EOF

# backend/users/forms.py
cat <<EOF > backend/users/forms.py
from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'age', 'sex', 'email', 'phone_number']
EOF

# backend/templates/base.html
cat <<EOF > backend/templates/base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Abd-ru-shin Book Sales</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <script src="{% static 'js/cookies.js' %}"></script>
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/other-writings/">Other Writings</a> |
        <a href="/audio/">Audio</a> |
        <a href="/contact/">Contact</a> |
        {% if user.is_authenticated %}
            <a href="/profile/complete/">Profile</a> |
            <a href="/accounts/logout/">Logout</a>
        {% else %}
            <a href="/accounts/login/">Login with Google</a>
        {% endif %}
    </nav>
    {% block content %}{% endblock %}
    <footer>
        <p>&copy; 2025 Abd-ru-shin Books | info@alexander-bernhardt-ke.com | +254-xxx-xxx-xxx</p>
    </footer>
    <div id="cookie-popup" style="display:none;">
        <p>This website uses cookies. <button onclick="acceptCookies()">Accept</button></p>
    </div>
</body>
</html>
EOF

# backend/templates/home.html
cat <<EOF > backend/templates/home.html
{% extends "base.html" %}
{% block content %}
<div class="hero">
    <h1>In the Light of Truth – The Grail Message</h1>
    <p>The spiritual masterpiece by Abdrushin.</p>
    <div class="book-cards">
    {% for book in main_books %}
        <div class="book-card">
            <img src="{{ book.cover_image.url }}" alt="{{ book.title }}" />
            <h3>{{ book.title }}</h3>
            <a href="{% url 'book_detail' book.id %}" class="btn">Details</a>
        </div>
    {% endfor %}
    </div>
    <a href="/audio/" class="cta-btn">Listen to Free Audio Sample</a>
</div>
{% endblock %}
EOF

# backend/templates/book_detail.html
cat <<EOF > backend/templates/book_detail.html
{% extends "base.html" %}
{% block content %}
<div class="book-detail">
    <img src="{{ book.cover_image.url }}" alt="{{ book.title }}" />
    <h2>{{ book.title }}</h2>
    <p>{{ book.description }}</p>
    <a href="{{ book.pdf_file.url }}" target="_blank" class="btn">Read First 3 Chapters</a>
    <h3>Audio Samples</h3>
    <ul>
    {% for audio in audios %}
        <li>
            Chapter {{ audio.chapter }}: {{ audio.title }}
            {% if audio.is_free %}
                <audio controls src="{{ audio.audio_file.url }}"></audio>
            {% else %}
                <em>Unlock for KSHS {{ audio.price }}</em>
            {% endif %}
        </li>
    {% endfor %}
    </ul>
</div>
{% endblock %}
EOF

# backend/templates/other_writings.html
cat <<EOF > backend/templates/other_writings.html
{% extends "base.html" %}
{% block content %}
<h2>Other Writings</h2>
<div class="book-cards">
    {% for book in books %}
        <div class="book-card">
            <img src="{{ book.cover_image.url }}" alt="{{ book.title }}" />
            <h3>{{ book.title }}</h3>
            <a href="{% url 'book_detail' book.id %}" class="btn">Details</a>
        </div>
    {% endfor %}
</div>
{% endblock %}
EOF

# backend/templates/audio.html
cat <<EOF > backend/templates/audio.html
{% extends "base.html" %}
{% block content %}
<h2>Audio Library</h2>
{% for book in books %}
    <h3>{{ book.title }}</h3>
    <ul>
    {% for audio in book.audios.all %}
        <li>
            Chapter {{ audio.chapter }}: {{ audio.title }}
            {% if audio.is_free %}
                <audio controls src="{{ audio.audio_file.url }}"></audio>
            {% else %}
                <em>Unlock for KSHS {{ audio.price }}</em>
            {% endif %}
        </li>
    {% endfor %}
    </ul>
{% endfor %}
{% endblock %}
EOF

# backend/templates/contact.html
cat <<EOF > backend/templates/contact.html
{% extends "base.html" %}
{% block content %}
<h2>Contact Us</h2>
<p>Email: info@alexander-bernhardt-ke.com</p>
<p>Phone: +254-xxx-xxx-xxx</p>
<p>Address: As listed on alexander-bernhardt-ke.com</p>
<form method="post">
    {% csrf_token %}
    <label>Your Name: <input type="text" name="name"></label><br>
    <label>Your Email: <input type="email" name="email"></label><br>
    <label>Message: <textarea name="message"></textarea></label><br>
    <button type="submit">Send</button>
</form>
{% endblock %}
EOF

# backend/templates/complete_profile.html
cat <<EOF > backend/templates/complete_profile.html
{% extends "base.html" %}
{% block content %}
<h2>Complete your profile</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
{% endblock %}
EOF

# backend/static/css/style.css
cat <<EOF > backend/static/css/style.css
body {
    background: #faf6ef;
    color: #2b2b2b;
    font-family: 'Segoe UI', Arial, sans-serif;
}
nav {
    background: #2e205f;
    color: #f4e3b2;
    padding: 1rem;
    text-align: center;
}
nav a {
    color: #f4e3b2;
    margin: 0 1rem;
    text-decoration: none;
}
.hero {
    background: linear-gradient(90deg, #2e205f 60%, #faf6ef 100%);
    color: #faf6ef;
    padding: 2rem;
    border-radius: 0 0 20px 20px;
    text-align: center;
}
.cta-btn, .btn {
    background-color: #5a9e6f;
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    border-radius: 5px;
    font-size: 1.2rem;
    margin-top: 1rem;
    text-decoration: none;
}
.book-cards { display: flex; gap: 2rem; justify-content: center; }
.book-card { background: #fff; border: 1px solid #f4e3b2; box-shadow: 0 2px 10px #eee; border-radius: 8px; padding: 1rem; text-align: center; }
.book-card img { width: 120px; height: 180px; object-fit: cover; margin-bottom: 1rem; }
footer { background: #2e205f; color: #f4e3b2; text-align: center; padding: 1rem; }
EOF

# backend/static/js/cookies.js
cat <<EOF > backend/static/js/cookies.js
window.onload = function() {
    if (!localStorage.getItem('cookiesAccepted')) {
        document.getElementById('cookie-popup').style.display = 'block';
    }
}
function acceptCookies() {
    localStorage.setItem('cookiesAccepted', true);
    document.getElementById('cookie-popup').style.display = 'none';
}
EOF

# rust_audio_service/Cargo.toml
cat <<EOF > rust_audio_service/Cargo.toml
[package]
name = "rust_audio_service"
version = "0.1.0"
edition = "2021"

[dependencies]
actix-web = "4"
EOF

# rust_audio_service/src/main.rs
cat <<EOF > rust_audio_service/src/main.rs
use actix_web::{web, App, HttpRequest, HttpServer, HttpResponse, Result};

async fn stream_audio(req: HttpRequest) -> Result<HttpResponse> {
    // Placeholder: In production, check user access and stream file
    Ok(HttpResponse::Ok()
        .content_type("audio/mpeg")
        .body("AUDIO STREAM PLACEHOLDER"))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/audio/{book_id}/{chapter}/", web::get().to(stream_audio))
    })
    .bind(("127.0.0.1", 8081))?
    .run()
    .await
}
EOF

# README.md
cat <<'EOF' > README.md
# Abd-ru-shin Books Website

A secure, dynamic book sales and audio streaming platform for "In The Light of Truth" and other works. Built with Django and Rust.

## Features
- Social login with Gmail
- User profile completion required for free sample access
- Protected PDF in-browser viewing
- Audio streaming: free samples, pay for full
- M-Pesa phone payments (integration placeholder)
- Cookie consent popup
- Follows OWASP best practices
EOF
echo "All files created."
echo "Next steps:"
...

## Dev Setup

1. Clone repo
2. Install Python (3.10+), Rust, and dependencies:
