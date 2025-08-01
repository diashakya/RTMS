"""
This module defines the views for the main application.
It handles rendering of different pages and user authentication.
"""
# ---------------Python Standard Library
from datetime import datetime, date
from io import BytesIO
import base64

# --------------------Django Core - Generic
from django.shortcuts import render, redirect, get_object_or_404
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
from .models import Order, OrderItem, Foods, Special, Customer, Favorite, Cart, CartItem, Category, Table

# -----------------------------------   Local Apps
from .models import Special
from .realtime_utils import send_new_order_notification, send_order_update, send_user_notification, send_order_status_notification
from .realtime_order_utils import notify_order_status_change, notify_new_order, get_order_status_display, get_order_progress_percentage

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
    """Contact page with functional contact form"""
    if request.method == 'POST':
        from .forms import ContactForm
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send notification email to admin (optional)
            try:
                send_contact_notification_email(contact_message)
            except Exception as e:
                print(f"Error sending notification email: {e}")
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        from .forms import ContactForm
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us'
    }
    return render(request, 'main/contact.html', context)

def menu(request):
    """Renders the menu page with food items and today's specials, filtered by category and search query."""
    # Restrict waiter users
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'waiter':
        return redirect('waiter_dashboard')
    
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
    try:
        cart = get_or_create_cart(request)
        if not cart:
            # If cart creation fails, create empty context
            context = {
                'cart': None,
                'cart_items': [],
                'total_price': 0,
                'total_items': 0,
                'checkout_form': CheckoutForm(),
            }
            return render(request, 'main/cart.html', context)
        
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
        
        # Safely get cart properties
        try:
            total_price = cart.total_price
        except (AttributeError, TypeError):
            total_price = 0
            
        try:
            total_items = cart.total_items
        except (AttributeError, TypeError):
            total_items = 0
        
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'total_items': total_items,
            'checkout_form': checkout_form,
        }
        return render(request, 'main/cart.html', context)
        
    except Exception as e:
        print(f"Error in cart_view: {e}")
        # Return a safe fallback context
        context = {
            'cart': None,
            'cart_items': [],
            'total_price': 0,
            'total_items': 0,
            'checkout_form': CheckoutForm(),
            'error': str(e)
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
        
        # Validate cart_items is a list and not None
        if not cart_items or not isinstance(cart_items, list):
            return JsonResponse({'success': False, 'message': 'Cart is empty or invalid'})
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            notes=notes,
            status='pending'
        )
        
        total = 0
        valid_items_count = 0
        
        # Create order items with improved error handling
        for item in cart_items:
            try:
                # Validate item is a dictionary
                if not isinstance(item, dict):
                    continue
                
                # Get item ID and validate it's not None/empty
                item_id = item.get('id')
                if not item_id or str(item_id).strip() == '':
                    continue
                
                # Get quantity and price with defaults
                quantity = item.get('quantity', 1)
                price = item.get('price', 0)
                
                # Validate quantity is positive integer
                try:
                    quantity = int(quantity) if quantity is not None else 1
                    if quantity <= 0:
                        quantity = 1
                except (ValueError, TypeError):
                    quantity = 1
                
                # Validate price is numeric
                try:
                    price = float(price) if price is not None else 0
                    if price < 0:
                        price = 0
                except (ValueError, TypeError):
                    price = 0
                
                # Check if it's a special or regular food item
                item_id_str = str(item_id).lower()
                if 'special' in item_id_str:
                    # It's a special item
                    special_id = item_id_str.replace('special-', '')
                    try:
                        special = Special.objects.get(id=special_id)
                        order_price = special.discounted_price if special.discounted_price else special.price
                        
                        OrderItem.objects.create(
                            order=order,
                            special=special,
                            quantity=quantity,
                            price=order_price or price
                        )
                        valid_items_count += 1
                    except (Special.DoesNotExist, ValueError):
                        continue
                else:
                    # It's a regular food item
                    try:
                        food = Foods.objects.get(id=item_id)
                        
                        OrderItem.objects.create(
                            order=order,
                            food=food,
                            quantity=quantity,
                            price=food.price or price
                        )
                        valid_items_count += 1
                    except (Foods.DoesNotExist, ValueError):
                        continue
                
                # Calculate total with validated values
                total += float(price) * int(quantity)
                
            except Exception as item_error:
                # Log individual item errors but continue processing
                print(f"Error processing cart item: {item_error}")
                continue
        
        # Check if at least one item was processed successfully
        if valid_items_count == 0:
            order.delete()  # Clean up empty order
            return JsonResponse({'success': False, 'message': 'No valid items found in cart'})
        
        # Update order total
        order.total = total
        order.save()
        
        # Send real-time notifications
        try:
            # Notify staff about new order
            notify_new_order(order.id)
            print(f"Real-time notification sent for new order {order.id}")
            
            # Send confirmation notification to customer if logged in
            if order.user:
                notify_order_status_change(
                    order.id, 
                    'pending', 
                    f'Your order #{order.id} has been placed successfully!'
                )
        except Exception as notification_error:
            # Don't fail the order if notification fails
            print(f"Failed to send real-time notification: {notification_error}")
        
        return JsonResponse({
            'success': True, 
            'order_id': order.id,
            'total': float(total),
            'items_count': valid_items_count,
            'message': 'Order placed successfully!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Order processing error: {str(e)}'})

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
        if not cart:
            return JsonResponse({'success': False, 'message': 'Unable to access cart'}, status=500)
        
        cart_items = cart.items.all()
        
        if not cart_items:
            return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)
        
        # Create or get customer
        customer, created = Customer.objects.get_or_create(
            customer_mobileno=customer_phone,
            defaults={
                'customer_firstname': customer_name.split()[0] if customer_name else 'Guest',
                'customer_lastname': ' '.join(customer_name.split()[1:]) if customer_name and len(customer_name.split()) > 1 else '',
                'customer_address': customer_address,
                'customer_email': 'guest@restaurant.com',  # Default email for API orders
                'customer_dob': timezone.now().date()  # Default DOB
            }
        )
        
        # Create order
        try:
            cart_total = cart.total_price or 0
        except (AttributeError, TypeError):
            cart_total = 0
            
        order = Order.objects.create(
            customer=customer,
            user=request.user if request.user.is_authenticated else None,
            notes=f"Payment Method: {payment_method.title()}\nDelivery Address: {customer_address}\n{order_notes}".strip(),
            status='pending',
            total=cart_total
        )
        
        # Create order items from cart with improved null safety
        valid_items_count = 0
        for cart_item in cart_items:
            try:
                # Validate cart_item exists and has required attributes
                if not cart_item:
                    continue
                    
                # Ensure quantity is valid (CartItem.quantity cannot be None due to DB constraint)
                quantity = getattr(cart_item, 'quantity', 1)
                if quantity is None or quantity <= 0:
                    quantity = 1
                
                if cart_item.food:
                    # Validate food item exists and has valid price
                    if hasattr(cart_item.food, 'price') and cart_item.food.price is not None:
                        OrderItem.objects.create(
                            order=order,
                            food=cart_item.food,
                            quantity=quantity,
                            price=cart_item.food.price
                        )
                        valid_items_count += 1
                elif cart_item.special:
                    # Validate special item exists and has valid price
                    if hasattr(cart_item.special, 'price') and cart_item.special.price is not None:
                        price = cart_item.special.discounted_price if cart_item.special.discounted_price else cart_item.special.price
                        OrderItem.objects.create(
                            order=order,
                            special=cart_item.special,
                            quantity=quantity,
                            price=price
                        )
                        valid_items_count += 1
            except (AttributeError, TypeError, ValueError) as item_error:
                print(f"Error processing cart item in API: {item_error}")
                continue
        
        # Verify at least one item was processed successfully
        if valid_items_count == 0:
            return JsonResponse({'success': False, 'message': 'No valid items found in cart'}, status=400)
        
        # Clear the cart
        cart_items.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully!',
            'order_id': order.id,
            'order_total': float(order.total)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error processing order: {str(e)}', 'error': str(e)}, status=500)

@login_required(login_url='login')
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

def thank_you(request, order_id=None):
    """Thank you page after successful order."""
    # Try to get order_id from URL parameter first, then from GET parameter
    if not order_id:
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
        
        # Get new status from request data
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            new_status = data.get('status')
        else:
            new_status = request.GET.get('status')
        
        # Validate status
        valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
        if new_status in valid_statuses:
            old_status = order.status
            order.status = new_status
            order.save()
            
            # Send real-time notifications using new utilities
            try:
                notify_order_status_change(order.id, new_status)
                print(f"Real-time notification sent for order {order.id}: {old_status} -> {new_status}")
            except Exception as e:
                print(f"Failed to send real-time notification: {e}")
            
            # Send status update email
            try:
                send_order_status_email(order, new_status)
            except Exception as e:
                print(f"Failed to send email notification: {e}")
            
            return JsonResponse({
                'success': True, 
                'message': 'Order status updated',
                'status': new_status,
                'status_display': get_order_status_display(new_status)
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid status'})
            
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})

# ......................................................Admin Dashboard Views........................

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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
    """Handle checkout form submission with support for delivery and dine-in orders"""
    form = CheckoutForm(request.POST)
    if form.is_valid():
        # Get cart items with null safety
        if not cart:
            messages.error(request, 'Cart not found.')
            return redirect('cart')
            
        try:
            cart_items = cart.items.all()
            # Filter out any None items and validate cart_items is iterable
            cart_items = [item for item in cart_items if item is not None] if cart_items else []
        except (AttributeError, TypeError):
            cart_items = []
            
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')
        
        # Get order type and related data
        order_type = form.cleaned_data['order_type']
        table_number = form.cleaned_data.get('table_number', '')
        
        # Create or get customer
        customer_data = {
            'customer_firstname': form.cleaned_data['customer_firstname'],
            'customer_lastname': form.cleaned_data['customer_lastname'],
            'customer_mobileno': form.cleaned_data['customer_mobileno'],
            'customer_address': form.cleaned_data['customer_address'] if order_type == 'delivery' else '',
            'customer_email': form.cleaned_data['customer_email'],
            'customer_dob': timezone.now().date()  # Default DOB, you may want to add this to the form
        }
        customer, created = Customer.objects.get_or_create(
            customer_mobileno=customer_data['customer_mobileno'],
            defaults=customer_data
        )
        
        # Create order with order type information
        payment_method = form.cleaned_data['payment_method']
        order_notes = form.cleaned_data['order_notes']
        
        # Prepare order notes with payment method and order type info
        notes_parts = [f"Payment Method: {payment_method.title()}"]
        if order_type == 'dine_in':
            notes_parts.append(f"Table Number: {table_number}")
        if order_notes:
            notes_parts.append(order_notes)
        
        # Calculate cart total with null checks
        try:
            cart_total = cart.total_price if cart else 0
        except (AttributeError, TypeError):
            cart_total = 0
        
        order = Order.objects.create(
            customer=customer,
            user=request.user if request.user.is_authenticated else None,
            order_type=order_type,
            delivery_address=form.cleaned_data['customer_address'] if order_type == 'delivery' else '',
            table_number=table_number if order_type == 'dine_in' else '',
            customer_name=f"{customer_data['customer_firstname']} {customer_data['customer_lastname']}",
            customer_phone=customer_data['customer_mobileno'],
            notes="\n".join(notes_parts),
            status='pending',
            total=cart_total
        )
        
        # Create order items from cart with improved error handling
        valid_items_count = 0
        for cart_item in cart_items:
            try:
                # Validate cart_item exists and has required attributes
                if not cart_item:
                    continue
                    
                # Ensure quantity is valid
                quantity = getattr(cart_item, 'quantity', None)
                if quantity is None or quantity <= 0:
                    quantity = 1
                
                if cart_item.food:
                    # Validate food item exists and has price
                    if hasattr(cart_item.food, 'price') and cart_item.food.price is not None:
                        OrderItem.objects.create(
                            order=order,
                            food=cart_item.food,
                            quantity=quantity,
                            price=cart_item.food.price
                        )
                        valid_items_count += 1
                elif cart_item.special:
                    # Validate special item exists and has price
                    if hasattr(cart_item.special, 'price') and cart_item.special.price is not None:
                        price = cart_item.special.discounted_price if cart_item.special.discounted_price else cart_item.special.price
                        OrderItem.objects.create(
                            order=order,
                            special=cart_item.special,
                            quantity=quantity,
                            price=price
                        )
                        valid_items_count += 1
            except (AttributeError, TypeError, ValueError) as item_error:
                print(f"Error processing cart item: {item_error}")
                continue
        
        # Verify at least one item was processed
        if valid_items_count == 0:
            messages.error(request, 'No valid items found in cart.')
            return redirect('cart')
        
        # Clear the cart
        cart_items.delete()
        
        # Send order confirmation email
        send_order_confirmation_email(order)
        
        # Send real-time notifications
        send_new_order_notification(order)
        if order.user:
            send_order_status_notification(order, 'pending')
        
        # Success message based on order type
        if order_type == 'delivery':
            messages.success(request, f'Delivery order #{order.id} placed successfully! Your order will be delivered to your address.')
        else:
            messages.success(request, f'Dine-in order #{order.id} placed successfully! Please wait at table {table_number}.')
        
        return redirect('thank_you', order_id=order.id)
    else:
        # Show form errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
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
def cancel_order(request, order_id):
    """Cancel an order (only if pending or confirmed)"""
    try:
        # Get order - allow both authenticated and guest orders
        if request.user.is_authenticated:
            order = Order.objects.get(
                id=order_id, 
                user=request.user, 
                status__in=['pending', 'confirmed']
            )
        else:
            # For guest orders, we might need session verification
            order = Order.objects.get(
                id=order_id, 
                status__in=['pending', 'confirmed']
            )
        
        order.status = 'cancelled'
        order.save()
        
        # Send real-time notification
        try:
            notify_order_status_change(order.id, 'cancelled', 'Order has been cancelled by customer')
        except Exception as e:
            print(f"Failed to send real-time notification: {e}")
        
        # Send notification email
        try:
            send_order_status_email(order, 'cancelled')
        except Exception as e:
            print(f"Failed to send email notification: {e}")
        
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
def reorder(request, order_id):
    """Add all items from a previous order to current cart"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Please log in to reorder'
        }, status=401)
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        cart = get_or_create_cart(request)
        
        items_added = 0
        for order_item in order.orderitem_set.all():
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
            'message': f'{items_added} items added to your cart',
            'items_added': items_added
        })
        
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found'
        }, status=404)

@login_required(login_url='login')
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


from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import ObjectDoesNotExist as RelatedObjectDoesNotExist

@login_required(login_url='login')
def send_status_email(request, order_id):
    """Send status email for specific order (admin only)."""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff privileges required.')
        return redirect('admin:main_order_changelist')
    try:
        order = Order.objects.get(id=order_id)
        send_order_status_email(order, order.status)
        messages.success(request, f'Status email sent for Order #{order_id}.')
    except Order.DoesNotExist:
        messages.error(request, f'Order #{order_id} not found.')
    except Exception as e:
        messages.error(request, f'Error sending email: {str(e)}')
    return redirect('admin:main_order_changelist')

def send_contact_notification_email(contact_message):
    """Send email notification to admin when new contact message is received"""
    subject = f"New Contact Message from {contact_message.name}"
    message = f"""
    New contact message received:
    
    Name: {contact_message.name}
    Email: {contact_message.email}
    Phone: {contact_message.phone}
    
    Message:
    {contact_message.message}
    
    Submitted at: {contact_message.submitted_at}
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['admin@restaurant.com']
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def make_reservation(request):
    from .forms import ReservationForm
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Your reservation request has been submitted! We will confirm soon.')
            return redirect('make_reservation')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReservationForm()
    return render(request, 'main/reservation.html', {'form': form, 'page_title': 'Make Reservation'})

def catering_request(request):
    from .forms import CateringRequestForm
    if request.method == 'POST':
        form = CateringRequestForm(request.POST)
        if form.is_valid():
            catering = form.save()
            messages.success(request, 'Your catering inquiry has been submitted! We will contact you soon.')
            return redirect('catering_request')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CateringRequestForm()
    return render(request, 'main/catering.html', {'form': form, 'page_title': 'Catering Services'})

def gift_card_request(request):
    from .forms import GiftCardRequestForm
    if request.method == 'POST':
        form = GiftCardRequestForm(request.POST)
        if form.is_valid():
            gift_card = form.save()
            messages.success(request, 'Your gift card request has been submitted! We will process it soon.')
            return redirect('gift_card_request')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GiftCardRequestForm()
    return render(request, 'main/gift_card.html', {'form': form, 'page_title': 'Gift Cards'})

# ----------------------------------- Waiter Views -----------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Table, Order

class WaiterRequiredMixin:
    """Verify that the current user is authenticated and is a waiter"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            if request.user.profile.user_type != 'waiter':
                raise PermissionDenied("You must be a waiter to access this page.")
        except (AttributeError, RelatedObjectDoesNotExist):
            raise PermissionDenied("Waiter profile not found.")
        return super().dispatch(request, *args, **kwargs)

class WaiterDashboardView(WaiterRequiredMixin, TemplateView):
    template_name = 'main/waiter_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        context['waiter'] = self.request.user.profile
        return context

@login_required
def order_details_ajax(request, order_id):
    """AJAX view for loading order details"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/partials/order_details.html', {'order': order})

# ------------------------Order Tracking Views
def order_tracking(request, order_id):
    """Display real-time order tracking page"""
    try:
        order = Order.objects.get(id=order_id)
        # Calculate progress percentage
        progress_percentage = get_order_progress_percentage(order.status)
        # Get user-friendly status display
        status_display = get_order_status_display(order.status)
        # Default status messages
        status_messages = {
            'pending': 'Your order has been received and is pending confirmation.',
            'confirmed': 'Your order has been confirmed and will be prepared soon.',
            'preparing': 'Your order is being prepared by our kitchen staff.',
            'ready': 'Your order is ready for pickup/delivery!',
            'completed': 'Your order has been completed. Thank you!',
            'cancelled': 'Your order has been cancelled.',
        }
        status_message = status_messages.get(order.status, f'Order status: {order.status}')
        context = {
            'order': order,
            'progress_percentage': progress_percentage,
            'status_display': status_display,
            'status_message': status_message,
        }
        return render(request, 'main/order_tracking.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('menu')

def track_order_api(request, order_id):
    """API endpoint for order tracking data"""
    try:
        order = Order.objects.get(id=order_id)
        # Get order items
        order_items = []
        for item in order.orderitem_set.all():
            order_items.append({
                'name': item.food.name if item.food else item.special.name,
                'quantity': item.quantity,
                'price': float(item.total_price()),
                'type': 'food' if item.food else 'special'
            })
        data = {
            'id': order.id,
            'status': order.status,
            'status_display': get_order_status_display(order.status),
            'progress_percentage': get_order_progress_percentage(order.status),
            'customer_name': order.customer_name or (order.customer.name if order.customer else 'Guest'),
            'customer_phone': order.customer_phone,
            'order_type': order.get_order_type_display(),
            'delivery_address': order.delivery_address,
            'table_number': order.table_number,
            'total': float(order.total),
            'created_at': order.created_at.isoformat(),
            'notes': order.notes,
            'items': order_items,
        }
        return JsonResponse({'success': True, 'order': data})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'})




