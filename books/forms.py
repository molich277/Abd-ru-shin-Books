from django import forms
from django.contrib.auth.models import User # <-- ADD THIS LINE
from .models import UserProfile # Import your UserProfile model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture'] # Add the fields you want users to be able to edit on their profile.
                                             # For example: 'bio', 'profile_picture', 'address', etc.
                                             # Make sure these fields exist in your UserProfile model in models.py
   
    # Add this form for the User model's fields
class UserForm(forms.ModelForm):
    class Meta:
        model = User # <-- Make sure this is correctly pointing to the User model
        # THIS IS THE MOST IMPORTANT PART FOR RENDERING FIELDS:
        # Make sure 'fields' is not empty, or 'exclude' is not excluding everything.
        fields = ['username', 'email', 'first_name', 'last_name']
        # OR:
        # exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']
        # DO NOT use both 'fields' and 'exclude' in the same Meta class.
        
# Add this new class for the ContactForm:
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
