# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile

@login_required
def profile_edit_view(request):
    """ویو ویرایش پروفایل کاربر"""
    
    # دریافت یا ایجاد پروفایل کاربر
   # Get or create profile for the current user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to home page or dashboard after profile completion
            return redirect('dashboard:dashboard')  # or redirect to 'accounts:dashboard' or '/'
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'personal/profile.html', context)
