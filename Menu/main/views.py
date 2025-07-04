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
from django.utils import timezone

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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .forms import CheckoutForm, AddToCartForm
from .serializers import SpecialSerializer,UserSerializer, FavoriteSerializer, FoodsSerializer
from rest_framework.permissions import IsAuthenticated

# ------------------------Django Core - AJAX/JSON
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

# ------------------------Models
from .models import Order, OrderItem, Foods, Special, Customer, Favorite, Cart, CartItem

# -----------------------------------   Local Apps
from .models import Special
from .realtime_utils import send_new_order_notification, send_order_update, send_user_notification, send_order_status_notification

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    food_id = request.data.get('food_id')
    if not food_id:
        return Response({'error': 'food_id required'}, status=400)
    favorite, created = Favorite.objects.get_or_create(user=request.user, food_id=food_id)
    if created:
        return Response({'success': True, 'id': favorite.id})
    else:
        return Response({'success': False, 'error': 'Already favorited'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_favorite(request):
    food_id = request.data.get('food_id')
    if not food_id:
        return Response({'error': 'food_id required'}, status=400)
    try:
        favorite = Favorite.objects.get(user=request.user, food_id=food_id)
        favorite.delete()
        return Response({'success': True})
    except Favorite.DoesNotExist:
        return Response({'success': False, 'error': 'Not favorited'}, status=400)



# ......................................................Cart & Order Views.......................

def get_or_create_cart(request):
    """Get or create cart for user or session, with cart merging for login"""
    if request.user.is_authenticated:
        # Get user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        # If user just logged in and has a session cart, merge it
        if request.session.session_key:
            try:
                session_cart = Cart.objects.get(session_key=request.session.session_key)
                # Merge session cart items into user cart
                for session_item in session_cart.items.all():
                    user_item, item_created = CartItem.objects.get_or_create(
                        cart=user_cart,
                        food=session_item.food,
                        special=session_item.special,
                        defaults={'quantity': session_item.quantity}
                    )
                    if not item_created:
                        user_item.quantity += session_item.quantity
                        user_item.save()
                # Delete session cart after merging
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
        
        return user_cart
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

def cart_view(request):
    """Renders the cart page with items and handles cart operations."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    # Handle form submissions
    if request.method == 'POST':
        if 'update_quantity' in request.POST:
            return handle_update_quantity(request, cart)
        elif 'remove_item' in request.POST:
            return handle_remove_item(request, cart)
        elif 'checkout' in request.POST:
            return handle_checkout(request, cart)
    
    # Create checkout form
    checkout_form = CheckoutForm()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price,
        'total_items': cart.total_items,
        'checkout_form': checkout_form,
    }
    return render(request, 'main/cart.html', context)

@csrf_exempt
def add_to_cart(request):
    """Add item to cart via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        item_type = data.get('type')  # 'food' or 'special'
        item_id = data.get('id')
        quantity = int(data.get('quantity', 1))
        
        cart = get_or_create_cart(request)
        
        if item_type == 'food':
            food = Foods.objects.get(id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                food=food,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            item_name = food.title
                
        elif item_type == 'special':
            special = Special.objects.get(id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                special=special,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            item_name = special.name
        else:
            return JsonResponse({'success': False, 'message': 'Invalid item type'}, status=400)
        
        return JsonResponse({
            'success': True,
            'message': f'Added {quantity} x {item_name} to cart!',
            'cart_count': cart.total_items
        })
        
    except Foods.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Food item not found'}, status=404)
    except Special.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Special item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
def update_cart_item(request):
    """Update cart item quantity"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        quantity = int(data.get('quantity'))
        
        cart = get_or_create_cart(request)
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_count': cart.total_items,
                'cart_total': float(cart.total_price)
            })
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
            # Calculate item total
            item_price = cart_item.food.price if cart_item.food else cart_item.special.price
            item_total = float(item_price) * quantity
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated successfully',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price),
            'item_total': item_total
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
def remove_from_cart(request):
    """Remove item from cart"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        
        cart = get_or_create_cart(request)
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

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

@csrf_exempt
def checkout_api(request):
    """Handle checkout process and create order from cart"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        payment_method = data.get('payment_method')
        customer_name = data.get('customer_name')
        customer_phone = data.get('customer_phone')
        customer_address = data.get('customer_address')
        order_notes = data.get('order_notes', '')
        
        # Validate required fields
        if not all([payment_method, customer_name, customer_phone, customer_address]):
            return JsonResponse({'success': False, 'message': 'All customer details are required'}, status=400)
        
        # Get user's cart
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        if not cart_items:
            return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)
        
        # Create or get customer
        customer, created = Customer.objects.get_or_create(
            phone=customer_phone,
            defaults={
                'name': customer_name,
                'address': customer_address
            }
        )
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            user=request.user if request.user.is_authenticated else None,
            notes=f"Payment Method: {payment_method.title()}\nDelivery Address: {customer_address}\n{order_notes}".strip(),
            status='pending',
            total=cart.total_price
        )
        
        # Create order items from cart
        for cart_item in cart_items:
            if cart_item.food:
                OrderItem.objects.create(
                    order=order,
                    food=cart_item.food,
                    quantity=cart_item.quantity,
                    price=cart_item.food.price
                )
            elif cart_item.special:
                price = cart_item.special.discounted_price if cart_item.special.discounted_price else cart_item.special.price
                OrderItem.objects.create(
                    order=order,
                    special=cart_item.special,
                    quantity=cart_item.quantity,
                    price=price
                )
        
        # Clear the cart
        cart_items.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully!',
            'order_id': order.id,
            'order_total': float(order.total)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error processing order: {str(e)}'}, status=500)

@login_required
def order_history(request):
    """Display user's order history with pagination and filters."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter in ['pending', 'completed', 'cancelled']:
        orders = orders.filter(status=status_filter)
    
    # Add pagination
    from django.core.paginator import Paginator
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj,
        'status_filter': status_filter,
        'total_orders': orders.count()
    }
    return render(request, 'main/order_history.html', context)

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
            
            # Send real-time notifications
            try:
                send_order_update(order.id, new_status, f'Order status updated to {new_status}')
                send_order_status_notification(order, new_status)
            except Exception as e:
                print(f"Failed to send real-time notification: {e}")
            
            # Send status update email
            send_order_status_email(order, new_status)
            
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

def favorites_view(request):
    """Renders the favorites page with user's favorite items."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    favorites = Favorite.objects.filter(user=request.user).select_related('food')
    context = {
        'favorites': favorites,
        'total_favorites': favorites.count(),
    }
    return render(request, 'main/favorites.html', context)

@csrf_exempt
def toggle_favorite(request):
    """Toggle favorite status for an item via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        food_id = data.get('food_id')
        
        food = Foods.objects.get(id=food_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            food=food,
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': f'Added {food.title} to favorites!',
                'action': 'added',
                'favorites_count': Favorite.objects.filter(user=request.user).count()
            })
        else:
            favorite.delete()
            return JsonResponse({
                'success': True,
                'message': f'Removed {food.title} from favorites!',
                'action': 'removed',
                'favorites_count': Favorite.objects.filter(user=request.user).count()
            })
        
    except Foods.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Food item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
def remove_favorite(request):
    """Remove item from favorites"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        favorite_id = data.get('favorite_id')
        
        favorite = Favorite.objects.get(id=favorite_id, user=request.user)
        food_name = favorite.food.title
        favorite.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Removed {food_name} from favorites!',
            'favorites_count': Favorite.objects.filter(user=request.user).count()
        })
        
    except Favorite.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Favorite not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
def list_favorites(request):
    """List user's favorites via AJAX"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    favorites = Favorite.objects.filter(user=request.user).select_related('food')
    favorites_data = []
    
    for favorite in favorites:
        favorites_data.append({
            'id': favorite.id,
            'food': favorite.food.id,
            'food_title': favorite.food.title,
            'food_price': float(favorite.food.price),
            'food_image': favorite.food.image.url if favorite.food.image else None,
        })
    
    return JsonResponse(favorites_data, safe=False)

@csrf_exempt  
def food_detail(request, pk):
    """Get food item details via AJAX"""
    try:
        food = Foods.objects.get(pk=pk)
        food_data = {
            'id': food.id,
            'title': food.title,
            'price': float(food.price),
            'image': food.image.url if food.image else None,
            'category': food.category.name if food.category else None,
            'description': food.description or '',
            'is_spicy': food.is_spicy,
            'is_vegetarian': food.is_vegetarian,
            'rating': float(food.rating) if food.rating else 0,
        }
        return JsonResponse(food_data)
    except Foods.DoesNotExist:
        return JsonResponse({'error': 'Food not found'}, status=404)

def handle_update_quantity(request, cart):
    """Handle quantity update form submission"""
    try:
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return redirect('cart')
        
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully!')
        
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item not found.')
    except Exception as e:
        messages.error(request, 'Error updating cart.')
    
    return redirect('cart')

def handle_remove_item(request, cart):
    """Handle item removal form submission"""
    try:
        cart_item_id = request.POST.get('cart_item_id')
        
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        item_name = cart_item.food.title if cart_item.food else cart_item.special.name
        cart_item.delete()
        messages.success(request, f'Removed {item_name} from cart.')
        
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item not found.')
    except Exception as e:
        messages.error(request, 'Error removing item from cart.')
    
    return redirect('cart')

def handle_checkout(request, cart):
    """Handle checkout form submission"""
    form = CheckoutForm(request.POST)
    if form.is_valid():
        # Get cart items
        cart_items = cart.items.all()
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')
        
        # Create or get customer
        customer_data = {
            'customer_firstname': form.cleaned_data['customer_firstname'],
            'customer_lastname': form.cleaned_data['customer_lastname'],
            'customer_mobileno': form.cleaned_data['customer_mobileno'],
            'customer_address': form.cleaned_data['customer_address'],
            'customer_email': form.cleaned_data['customer_email'],
            'customer_dob': timezone.now().date()  # Default DOB, you may want to add this to the form
        }
        customer, created = Customer.objects.get_or_create(
            customer_mobileno=customer_data['customer_mobileno'],
            defaults=customer_data
        )
        
        # Create order
        payment_method = form.cleaned_data['payment_method']
        order_notes = form.cleaned_data['order_notes']
        
        order = Order.objects.create(
            customer=customer,
            user=request.user if request.user.is_authenticated else None,
            notes=f"Payment Method: {payment_method.title()}\n{order_notes}".strip(),
            status='pending',
            total=cart.total_price
        )
        
        # Create order items from cart
        for cart_item in cart_items:
            if cart_item.food:
                OrderItem.objects.create(
                    order=order,
                    food=cart_item.food,
                    quantity=cart_item.quantity,
                    price=cart_item.food.price
                )
            elif cart_item.special:
                price = cart_item.special.discounted_price if cart_item.special.discounted_price else cart_item.special.price
                OrderItem.objects.create(
                    order=order,
                    special=cart_item.special,
                    quantity=cart_item.quantity,
                    price=price
                )
        
        # Clear the cart
        cart_items.delete()
        
        # Send order confirmation email
        send_order_confirmation_email(order)
        
        # Send real-time notifications
        send_new_order_notification(order)
        if order.user:
            send_order_status_notification(order, 'pending')
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('thank_you', order_id=order.id)
    else:
        messages.error(request, 'Please fill in all required fields correctly.')
        return redirect('cart')

def add_to_cart_form(request):
    """Handle add to cart via form submission (server-side)"""
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data['item_type']
            item_id = form.cleaned_data['item_id']
            quantity = form.cleaned_data['quantity']
            
            cart = get_or_create_cart(request)
            
            try:
                if item_type == 'food':
                    food = Foods.objects.get(id=item_id)
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        food=food,
                        defaults={'quantity': quantity}
                    )
                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()
                    item_name = food.title
                        
                elif item_type == 'special':
                    special = Special.objects.get(id=item_id)
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        special=special,
                        defaults={'quantity': quantity}
                    )
                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()
                    item_name = special.name
                
                messages.success(request, f'🛒 Added {quantity} x {item_name} to cart! Total items: {cart.total_items}')
                
            except (Foods.DoesNotExist, Special.DoesNotExist):
                messages.error(request, 'Item not found.')
        else:
            messages.error(request, 'Invalid form data.')
    
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

@csrf_exempt
@api_view(['POST'])
@login_required
def cancel_order(request, order_id):
    """Cancel an order (only if pending)"""
    try:
        order = Order.objects.get(id=order_id, user=request.user, status='pending')
        order.status = 'cancelled'
        order.save()
        
        # Send notification email
        send_order_status_email(order, 'cancelled')
        
        return JsonResponse({
            'success': True,
            'message': 'Order cancelled successfully'
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found or cannot be cancelled'
        }, status=404)

@csrf_exempt
@api_view(['POST'])
@login_required
def reorder(request, order_id):
    """Add all items from a previous order to current cart"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        cart = get_or_create_cart(request)
        
        items_added = 0
        for order_item in order.items.all():
            if order_item.food:
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    food=order_item.food,
                    defaults={'quantity': order_item.quantity}
                )
                if not created:
                    cart_item.quantity += order_item.quantity
                    cart_item.save()
                items_added += 1
            elif order_item.special:
                # Check if special is still active
                if order_item.special.active:
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        special=order_item.special,
                        defaults={'quantity': order_item.quantity}
                    )
                    if not created:
                        cart_item.quantity += order_item.quantity
                        cart_item.save()
                    items_added += 1
        
        return JsonResponse({
            'success': True,
            'message': f'Added {items_added} items to cart',
            'cart_count': cart.total_items
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found'
        }, status=404)

@login_required
def order_receipt(request, order_id):
    """Generate and display order receipt"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'main/order_receipt.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('order_history')

# Email notification functions
def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.conf import settings
        
        if order.customer and order.customer.customer_email:
            subject = f'Order Confirmation - Order #{order.id}'
            html_message = render_to_string('emails/order_confirmation.html', {'order': order})
            plain_message = f'''
            Dear {order.customer.customer_firstname},
            
            Thank you for your order! Your order #{order.id} has been confirmed.
            
            Order Total: Rs {order.total}
            
            We'll notify you when your order is ready.
            
            Best regards,
            Restaurant Team
            '''
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer.customer_email],
                html_message=html_message,
                fail_silently=False,
            )
    except Exception as e:
        print(f"Error sending email: {e}")

def send_order_status_email(order, status):
    """Send order status update email"""
    try:
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.conf import settings
        
        if order.customer and order.customer.customer_email:
            status_messages = {
                'pending': 'Your order is being prepared',
                'completed': 'Your order is ready for pickup/delivery!',
                'cancelled': 'Your order has been cancelled'
            }
            
            subject = f'Order Update - Order #{order.id}'
            html_message = render_to_string('emails/order_status.html', {
                'order': order,
                'status': status,
                'status_message': status_messages.get(status, 'Order status updated')
            })
            plain_message = f'''
            Dear {order.customer.customer_firstname},
            
            Your order #{order.id} status has been updated to: {status.upper()}
            
            {status_messages.get(status, 'Order status updated')}
            
            Order Total: Rs {order.total}
            
            Best regards,
            Restaurant Team
            '''
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer.customer_email],
                html_message=html_message,
                fail_silently=False,
            )
    except Exception as e:
        print(f"Error sending status email: {e}")




