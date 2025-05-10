from django.urls import path
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('menu/',menu,name="menu"),
    path('services/',services,name="services"),


    # --------------------------------------------authentication urls-----------------------------
    path('register/',register,name='register'),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='log_out'),
    path('change_password/', change_password, name='change_password'),
    

     path('reset_password/', 
         auth_views.PasswordResetView.as_view(
             template_name="authenticate/password_reset.html"
         ), 
         name='reset_password'),
    
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name="authenticate/reset_password_sent.html"
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name="authenticate/password_reset_confirm.html"

         ), 
         name='password_reset_confirm'),
    
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name="authenticate/password_reset_complete.html"
         ), 
         name='password_reset_complete'),

    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('thank-you/', thank_you, name='thank_you'),
    path('cart/get_cart_items/', get_cart_items, name='get_cart_items'),
    path('cart/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear_cart/', clear_cart, name='clear_cart'),
# --------------------api urls--------------------
    path('specials/', special_list, name='special_list'),
    path('users/', user_list, name='user_list'),
]
