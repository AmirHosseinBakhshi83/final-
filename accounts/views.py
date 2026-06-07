from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm
from personal.models import Profile 


# Create your views here.

def site_login (request):
    if not request.user.is_authenticated:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)
                    return redirect('/dashboard')  
        
        context = {'form':form}
        return render(request,'accounts/login.html' , context) 
    else:
        return redirect('/') 
    
@login_required
def site_logout (request):
    logout (request)
    return redirect('/')


def site_signup (request):
    if not request.user.is_authenticated:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()  
                login(request,user)
                return redirect('accounts:complete_profile')
        context = {'form':form}
        return render(request,'accounts/signup.html' , context) 
    else:
        return redirect('/')
    

@login_required
def complete_profile(request):
    # Get or create profile for the current user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to home page or dashboard after profile completion
            return redirect('dashboard:dashboard')  # or redirect to 'accounts:dashboard' or '/'
    else:
        form = ProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'accounts/complete_profile.html', context)
 
