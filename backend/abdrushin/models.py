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
