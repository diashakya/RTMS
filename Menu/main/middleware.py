from django.shortcuts import redirect
from django.urls import resolve

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        current_url = resolve(request.path_info).url_name
        
        # Customer-only URLs
        customer_urls = ['add_to_cart', 'cart', 'checkout', 'place_order']
        # Waiter-only URLs
        waiter_urls = ['waiter_dashboard', 'table_management']

        try:
            if request.user.profile.user_type == 'waiter':
                if current_url in customer_urls:
                    return redirect('waiter_dashboard')
            else:  # customer or other roles
                if current_url in waiter_urls:
                    return redirect('menu')
        except:
            pass

        return self.get_response(request)