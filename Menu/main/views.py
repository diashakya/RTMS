"""
This module defines the views for the main application.
It handles rendering of different pages and user authentication.
"""
# ---------------Python Standard Library
from datetime import datetime
from io import BytesIO
import base64

# --------------------Django Core - Generic
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db import models

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
# from .realtime_utils import send_new_order_notification, send_order_update, send_user_notification  # Temporarily commented out

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

# ......................................................Cart & Order Views.......................

def cart_view(request):
    """Renders the cart page."""
    return render(request, 'main/cart.html')

@csrf_exempt
@api_view(['POST'])
def checkout(request):
    """Handle checkout process and create order."""
    try:
        data = json.loads(request.body)
        cart_items = data.get('cart', [])
        notes = data.get('notes', '')
        
        if not cart_items:
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            notes=notes,
            status='pending'
        )
        
        total = 0
        # Create order items
        for item in cart_items:
            try:
                # Check if it's a special or regular food item
                if 'special' in str(item.get('id', '')).lower():
                    # It's a special item
                    special_id = item['id'].replace('special-', '')
                    special = Special.objects.get(id=special_id)
                    price = special.discounted_price if special.discounted_price else special.price
                    
                    OrderItem.objects.create(
                        order=order,
                        special=special,
                        quantity=item['quantity'],
                        price=price
                    )
                else:
                    # It's a regular food item
                    food = Foods.objects.get(id=item['id'])
                    
                    OrderItem.objects.create(
                        order=order,
                        food=food,
                        quantity=item['quantity'],
                        price=food.price
                    )
                
                total += float(item['price']) * int(item['quantity'])
                
            except (Foods.DoesNotExist, Special.DoesNotExist):
                continue
        
        # Update order total
        order.total = total
        order.save()
        
        # Send real-time notifications (temporarily disabled)
        try:
            # Notify staff about new order
            order_data = {
                'id': order.id,
                'customer': order.user.username if order.user else 'Guest',
                'total': float(order.total),
                'items_count': len(cart_items),
                'created_at': order.created_at.isoformat()
            }
            # send_new_order_notification(order_data)  # Temporarily commented out
            
            # Send notification to customer if logged in
            if order.user:
                pass
                # send_user_notification(  # Temporarily commented out
                #     order.user.id,
                #     'Order Confirmed',
                #     f'Your order #{order.id} has been placed successfully!',
                #     'success'
                # )
        except Exception as e:
            # Don't fail the order if notification fails
            print(f"Failed to send real-time notification: {e}")
        
        return JsonResponse({
            'success': True, 
            'order_id': order.id,
            'total': float(total),
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def order_history(request):
    """Display user's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})

def thank_you(request):
    """Thank you page after successful order."""
    order_id = request.GET.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass
    return render(request, 'main/thank_you.html', {'order': order})

@csrf_exempt
@api_view(['POST'])
def update_order_status(request, order_id):
    """Update order status (for staff/admin)."""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        
        if new_status in ['pending', 'completed', 'cancelled']:
            order.status = new_status
            order.save()
            
            # Send real-time notifications (temporarily disabled)
            try:
                # send_order_update(order.id, new_status, f'Order status updated to {new_status}')  # Temporarily commented out
                
                # Send notification to customer if order has a user
                if order.user:
                    status_messages = {
                        'pending': 'Your order is being prepared',
                        'completed': 'Your order is ready!',
                        'cancelled': 'Your order has been cancelled'
                    }
                    # send_user_notification(  # Temporarily commented out
                    #     order.user.id,
                    #     'Order Update',
                    #     f'Order #{order.id}: {status_messages.get(new_status, "Status updated")}',
                    #     'info' if new_status == 'pending' else 'success' if new_status == 'completed' else 'warning'
                    # )
            except Exception as e:
                print(f"Failed to send real-time notification: {e}")
            
            return JsonResponse({'success': True, 'message': 'Order status updated'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid status'})
            
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'})

# ......................................................Admin Dashboard Views........................

@login_required
def admin_dashboard(request):
    """Admin dashboard for managing restaurant."""
    if not request.user.is_staff:
        return redirect('index')
    
    # Get statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    total_revenue = Order.objects.filter(status='completed').aggregate(
        total=models.Sum('total')
    )['total'] or 0
    
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'main/admin_dashboard.html', context)

@login_required 
def manage_orders(request):
    """Manage all orders for staff."""
    if not request.user.is_staff:
        return redirect('index')
    
    status_filter = request.GET.get('status', 'all')
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    return render(request, 'main/manage_orders.html', {
        'orders': orders,
        'status_filter': status_filter
    })

# ......................................................QR Code Views............................

@login_required
def generate_qr_codes(request):
    """Generate QR codes for restaurant tables."""
    if not request.user.is_staff:
        return redirect('index')
    
    
    try:
        import qrcode
    except ImportError:
        return JsonResponse({'error': 'QR code library not installed. Run: pip install qrcode[pil]'})
    
    num_tables = int(request.GET.get('tables', 10))
    qr_codes = []
    
    for table_num in range(1, num_tables + 1):
        # Create QR code data - URL to menu with table number
        qr_data = f"{request.build_absolute_uri('/menu/')}?table={table_num}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        qr_codes.append({
            'table_number': table_num,
            'qr_data': qr_data,
            'qr_image': qr_base64
        })
    
    return render(request, 'main/qr_codes.html', {
        'qr_codes': qr_codes,
        'num_tables': num_tables
    })

def table_menu(request):
    """Menu view with table context from QR code."""
    table_number = request.GET.get('table')
    
    # Get menu data
    todays_specials = Special.objects.filter(date=date.today(), active=True)
    categories = Category.objects.all()
    foods = Foods.objects.all()
    
    context = {
        'todays_specials': todays_specials,
        'foods': foods,
        'categories': categories,
        'table_number': table_number,
        'is_table_order': bool(table_number)
    }
    return render(request, 'main/table_menu.html', context)

# ......................................................Call Waiter Views..........................

@csrf_exempt
@api_view(['POST'])
def call_waiter(request):
    """Handle call waiter requests from tables."""
    try:
        data = json.loads(request.body)
        table_number = data.get('table_number')
        message = data.get('message', f'Customer at table {table_number} needs assistance')
        
        # Send real-time notification to staff
        try:
            from .realtime_utils import send_staff_notification
            send_staff_notification('Call Waiter', message, 'warning')
        except:
            pass  # Don't fail if real-time notification fails
        
        # You could also save this to database for tracking
        # WaiterCall.objects.create(table_number=table_number, message=message)
        
        return JsonResponse({'success': True, 'message': 'Waiter has been notified'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})




