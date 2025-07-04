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
    

    # ---------------------------cart and order urls---------------------------------
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('thank-you/', thank_you, name='thank_you'),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    
    # ---------------------------admin dashboard urls-----------------------------
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manage-orders/', manage_orders, name='manage_orders'),
    path('generate-qr-codes/', generate_qr_codes, name='generate_qr_codes'),
    path('table-menu/', table_menu, name='table_menu'),
    path('call-waiter/', call_waiter, name='call_waiter'),

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
# --------------------api urls--------------------
    path('specials/', special_list, name='special_list'),
    path('users/', user_list, name='user_list'),
]
