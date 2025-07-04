"""
Context processors for making cart and favorites data available in all templates
"""
from .models import Cart, Favorite

def cart_context(request):
    """Add cart information to template context"""
    cart_count = 0
    favorites_count = 0
    
    if hasattr(request, 'user') and request.user.is_authenticated:
        # Get user's cart count
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
            
        # Get user's favorites count
        favorites_count = Favorite.objects.filter(user=request.user).count()
    else:
        # Get session cart count
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                cart_count = 0
    
    return {
        'cart_count': cart_count,
        'favorites_count': favorites_count,
    }
