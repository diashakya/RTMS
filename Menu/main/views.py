from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Special
from datetime import datetime

# Create your views here.

# ......................................................Main Views...............................

date = datetime.now()

def index(request):
    todays_specials = Special.objects.filter(date=date.today(), active=True)
    return render(request, 'main/index.html', {'data': date, 'todays_specials': todays_specials})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def menu(request):
    todays_specials = Special.objects.filter(date=date.today(), active=True)
    return render(request, 'main/menu.html', {'todays_specials': todays_specials})
    
def services(request):
    return render(request, 'main/services.html')


# ......................................................Authentication Views......................

def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        Cpassword = data.get('Cpassword')

        # Validate password match
        if password != Cpassword:
            messages.error(request, "Confirm password and password don't match")
            return redirect('register')

        # Check all required fields
        if not all([first_name, last_name, username, email, password]):
            messages.error(request, "All fields are required")
            return redirect('register')

        try:
            # Create new user
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Username already exists")
            return redirect('register')

    return render(request, 'authenticate/register.html')

def login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'authenticate/login.html')

def log_out(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')

# -------------------------------Authentication part ends here---------------------