from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'age', 'sex', 'phone_number']
        # You can add 'additional_info' here if you decide to include it
