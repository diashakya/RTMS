from django.urls import path
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('menu/',menu,name="menu"),
    path('favorites/',favorites_view,name="favorites"),
    path('services/',services,name="services"),


    # --------------------------------------------authentication urls-----------------------------
    path('register/',register,name='register'),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='log_out'),
    path('change_password/', change_password, name='change_password'),
    

    # ---------------------------cart and order urls---------------------------------
    path('cart/', cart_view, name='cart'),
    path('add-to-cart-form/', add_to_cart_form, name='add_to_cart_form'),
    path('api/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('api/update-cart-item/', update_cart_item, name='update_cart_item'),
    path('api/remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('api/checkout/', checkout_api, name='checkout_api'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('api/cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('api/reorder/<int:order_id>/', reorder, name='reorder'),
    path('order-receipt/<int:order_id>/', order_receipt, name='order_receipt'),
    path('thank-you/', thank_you, name='thank_you'),
    path('thank-you/<int:order_id>/', thank_you, name='thank_you'),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    
    # ---------------------------admin dashboard urls-----------------------------
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('sales-report/', sales_report, name='sales_report'),
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
    path('api/toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    path('api/remove-favorite/', remove_favorite, name='remove_favorite_api'),
    path('api/favorites/', list_favorites, name='list_favorites'),
    path('api/favorites/add/', toggle_favorite, name='add_favorite'),
    path('api/favorites/remove/', toggle_favorite, name='remove_favorite_toggle'),
    path('api/foods/<int:pk>/', food_detail, name='food_detail'),

    # Admin email functionality
    path('send-status-email/<int:order_id>/', send_status_email, name='send_status_email'),
    path('reservation/', make_reservation, name='make_reservation'),
    path('catering/', catering_request, name='catering_request'),
    path('gift-card/', gift_card_request, name='gift_card_request'),

    # Waiter URLs
    path('waiter/', WaiterDashboardView.as_view(), name='waiter_dashboard'),
    path('waiter/order/<int:order_id>/details/', order_details_ajax, name='waiter_order_details'),
    path('waiter/order/<int:order_id>/mark-served/', mark_order_served, name='waiter_mark_order_served'),
    path('waiter/table/<int:table_id>/clear/', clear_table, name='waiter_clear_table'),
]
