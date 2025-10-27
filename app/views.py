from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import SignupForm

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

@login_required
def chat_view(request):
    return render(request, 'chat.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html') 

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup Successfull")
            return redirect('chat')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')