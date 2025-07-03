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
