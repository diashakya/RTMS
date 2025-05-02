from django.shortcuts import render,redirect

from datetime import datetime

from django.contrib.auth.models import User

from django.contrib import messages

from django.db import IntegrityError
from .models import Special
# Create your views here.

date = datetime.now()
def index(request):
    return render(request,'main/index.html',{'data':date})

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')

def menu(request):
    todays_specials = Special.objects.filter(date=date.today(), active=True)
    return render(request, 'main/menu.html', {'todays_specials': todays_specials})
    
def services(request):
    return render(request,'main/services.html')


# ......................................................authenticate part ......................
def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        Cpassword = data.get('Cpassword')

        
        if password != Cpassword:
            messages.error(request,"confrim password and password doesnt match")
            return redirect('register')

        if not all([first_name, last_name, username, email, password]):
            return render(request, 'authenticate/register.html', {'error': 'All fields are required'})

        try:
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            return redirect('log_in')  # Replace 'login' with the name of your login URL
        except IntegrityError:
            return render(request, 'authenticate/register.html', {'error': 'Username already exists'})

    return render(request, 'authenticate/register.html')


def log_in(request):
    return render(request,'authenticate/login.html')
