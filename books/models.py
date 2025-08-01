from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Will be provided later
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    is_main_book = models.BooleanField(default=False) # For home page display
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True) # A text field for a short biography
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # For user profile images
    full_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)   
    # Email is already in User model, but can be here for consistency if needed
    # additional_info = models.TextField(blank=True) # Whatever else you deem required

    has_access_to_book_one_chapters = models.BooleanField(default=False)
    # Add fields for paid audio access later
    audio_access_book_one = models.BooleanField(default=False)
    audio_access_book_two = models.BooleanField(default=False)
    audio_access_book_three = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Signal to create UserProfile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Audio(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/')
    is_free = models.BooleanField(default=False) # For first three audios of Book 1

    def __str__(self):
        return f"{self.book.title} - Chapter {self.chapter_number}: {self.title}"

class FreePDF(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    pdf_file = models.FileField(upload_to='free_pdfs/')

    def __str__(self):
        return f"PDF: {self.book.title} - Chapter {self.chapter_number}"
