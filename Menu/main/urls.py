from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('menu/',menu,name="menu"),
    path('services/',services,name="services"),


    # authentication urls
    path('register/',register,name='register'),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='log_out'),
    path('change_password/', change_password, name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="main/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="main/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/reset_password_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="main/reset_password_complete.html"), name='password_reset_complete'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name="main/password_change_done.html"), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="main/password_change.html"), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name="main/password_change_done.html"), name='password_change_done'),
   
]