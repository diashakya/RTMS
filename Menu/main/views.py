"""
This module defines the views for the main application.
It handles rendering of different pages and user authentication.
"""
# ---------------Python Standard Library
from datetime import datetime

# --------------------Django Core - Generic
from django.shortcuts import render, redirect
from django.db import IntegrityError

# ------------------------Django Core - Auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import PasswordChangeForm    
from django.contrib.auth.decorators import login_required

# ------------------------Django Rest Framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SpecialSerializer,UserSerializer


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Foods, Special, Customer
import json


# -----------------------------------   Local Apps
from .models import Special

# Create your views here.

# ......................................................Main Views...............................

date = datetime.now()

def index(request):
    """Renders the index page with today's specials."""
    todays_specials = Special.objects.filter(date=date.today(), active=True)
    return render(request, 'main/index.html', {'data': date, 'todays_specials': todays_specials})

def about(request):
    """Renders the about page."""
    return render(request, 'main/about.html')

def contact(request):
    """Renders the contact page."""
    return render(request, 'main/contact.html')

from .models import Special, Foods

from .models import Special, Foods, Category

def menu(request):
    """Renders the menu page with food items and today's specials, filtered by category and search query."""
    todays_specials = Special.objects.filter(date=date.today(), active=True)
    categories = Category.objects.all()
    selected_category_name = request.GET.get('category')
    search_query = request.GET.get('q')

    try:
        if selected_category_name:
            selected_category = Category.objects.get(name=selected_category_name)
            foods = Foods.objects.filter(category=selected_category)
        else:
            foods = Foods.objects.all()
            selected_category = None
    except Category.DoesNotExist:
        messages.warning(request, f"Category '{selected_category_name}' not found.")
        foods = Foods.objects.all()
        selected_category = None

    if search_query:
        foods = foods.filter(title__icontains=search_query)

    context = {
        'todays_specials': todays_specials,
        'foods': foods,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'main/menu.html', context)

def services(request):
    """Renders the services page."""
    return render(request, 'main/services.html')


# ......................................................Authentication Views......................
def register(request):
    """Handles user registration."""
    if request.method == "POST":
        data = request.POST
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('Cpassword')

        # Check if user is already logged in
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Validate password match
        if password != confirm_password:
            messages.error(request, "Confirm password and password don't match")
            return redirect('register')

        # Check all required fields
        if not all([first_name, last_name, username, email, password]):
            messages.error(request, "All fields are required")
            return redirect('register')
        

        try:
            validate_password(password=password)
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
        # Handle password validation errors
        except ValidationError as e:
            
            messages.error(request, f"Password error: {e}")
            return redirect('register')
        # Handle IntegrityError if username already exists
        except IntegrityError:
            messages.error(request, "Username already exists")
            return redirect('register')

    return render(request, 'authenticate/register.html')

def login_view(request):
    """Handles user login."""
    # Redirect if already logged in
    # if request.user.is_authenticated:
    #     return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            # Set session expiry to 0 for session cookie (browser close)
            messages.success(request, "Logged in successfully!")
            return redirect('index')
        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'authenticate/login.html')

def log_out(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')

@login_required(login_url='login')
def change_password(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    return render(request, 'authenticate/change_pass.html',{'form': form}) 
# ------------------------------------------Authentication part ends here---------------------
# ......................................................API Views...............................
@api_view(['GET'])
def special_list(request):
    specials = Special.objects.all()
    serializer = SpecialSerializer(specials, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)




