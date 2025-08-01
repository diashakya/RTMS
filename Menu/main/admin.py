from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Special, Foods, Category, Favorite, Order, OrderItem, Customer, Cart, CartItem, Contact, Reservation, CateringRequest, UserProfile

# Enhanced Order Item Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('food', 'special', 'quantity', 'price', 'total_price')
    
    def get_readonly_fields(self, request, obj=None):
        # Make total_price readonly
        readonly = list(self.readonly_fields)
        return readonly

# Enhanced Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'order_type_display', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'order_type', 'created_at', 'customer')
    search_fields = ('id', 'customer__customer_firstname', 'customer__customer_lastname', 'customer__customer_mobileno', 'table_number', 'customer_name')
    readonly_fields = ('created_at', 'total')
    inlines = [OrderItemInline]
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'user', 'status', 'total', 'created_at')
        }),
        ('Order Type & Location', {
            'fields': ('order_type', 'delivery_address', 'table_number')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
    
    def customer_info(self, obj):
        if obj.customer:
            return f"{obj.customer.customer_firstname} {obj.customer.customer_lastname}"
        elif obj.customer_name:
            return obj.customer_name
        return "Guest"
    customer_info.short_description = "Customer"
    
    def order_type_display(self, obj):
        if obj.order_type == 'delivery':
            return format_html('<span style="color: #007cba;"><i class="fas fa-truck"></i> Delivery</span>')
        elif obj.order_type == 'dine_in':
            location = f" (Table: {obj.table_number})" if obj.table_number else ""
            return format_html('<span style="color: #e68900;"><i class="fas fa-utensils"></i> Dine In{}</span>', location)
        return obj.get_order_type_display()
    order_type_display.short_description = "Order Type"
    order_type_display.allow_tags = True
    
    actions = ['mark_completed', 'mark_cancelled', 'send_confirmation_emails', 'delete_selected_orders']
    
    def mark_completed(self, request, queryset):
        count = queryset.update(status='completed')
        # Send emails for each order
        for order in queryset:
            try:
                from .views import send_order_status_email
                send_order_status_email(order, 'completed')
            except:
                pass
        self.message_user(request, f'{count} orders marked as completed and emails sent.')
    mark_completed.short_description = "Mark selected orders as completed"
    
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        # Send emails for each order
        for order in queryset:
            try:
                from .views import send_order_status_email
                send_order_status_email(order, 'cancelled')
            except:
                pass
        self.message_user(request, f'{count} orders cancelled and emails sent.')
    mark_cancelled.short_description = "Cancel selected orders"
    
    def send_confirmation_emails(self, request, queryset):
        for order in queryset:
            try:
                from .views import send_order_confirmation_email
                send_order_confirmation_email(order)
            except:
                pass
        self.message_user(request, f'Confirmation emails sent for {queryset.count()} orders.')
    send_confirmation_emails.short_description = "Send confirmation emails"
    
    def delete_selected_orders(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} orders deleted successfully.')
    delete_selected_orders.short_description = "⚠️ Delete selected orders (permanent)"

# Enhanced Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_firstname', 'customer_lastname', 'customer_mobileno', 'customer_email', 'order_count')
    search_fields = ('customer_firstname', 'customer_lastname', 'customer_mobileno', 'customer_email')
    list_filter = ('customer_dob',)
    
    def order_count(self, obj):
        count = obj.order_set.count()
        if count > 0:
            return format_html('<a href="{}?customer__id__exact={}">{} orders</a>',
                             reverse('admin:main_order_changelist'), obj.id, count)
        return "0 orders"
    order_count.short_description = "Orders"
    order_count.allow_tags = True

# Cart Item Inline
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price', 'added_at')

# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'total_items', 'total_price', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'total_items')
    inlines = [CartItemInline]

@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discounted_price', 'active', 'date')
    list_filter = ('category', 'active', 'date', 'is_vegetarian')
    search_fields = ('name', 'description')
    list_editable = ('active', 'price', 'discounted_price')
    date_hierarchy = 'date'
    actions = ['delete_selected_specials', 'deactivate_specials', 'activate_specials']
    
    def delete_selected_specials(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} special items deleted successfully.')
    delete_selected_specials.short_description = "Delete selected specials"
    
    def deactivate_specials(self, request, queryset):
        count = queryset.update(active=False)
        self.message_user(request, f'{count} specials deactivated.')
    deactivate_specials.short_description = "Deactivate selected specials"
    
    def activate_specials(self, request, queryset):
        count = queryset.update(active=True)
        self.message_user(request, f'{count} specials activated.')
    activate_specials.short_description = "Activate selected specials"

@admin.register(Foods)
class FoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'is_spicy', 'rating')
    list_filter = ('category', 'is_spicy')
    search_fields = ('title',)
    list_editable = ('price', 'is_spicy', 'rating')
    actions = ['delete_selected_foods', 'mark_as_unavailable']
    
    def delete_selected_foods(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} food items deleted successfully.')
    delete_selected_foods.short_description = "Delete selected food items"
    
    def mark_as_unavailable(self, request, queryset):
        # Note: This would require an 'is_available' field in the Foods model
        self.message_user(request, f'Feature not implemented yet - would mark {queryset.count()} items as unavailable.')
    mark_as_unavailable.short_description = "Mark selected items as unavailable"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_count', 'special_count')
    search_fields = ('name',)
    actions = ['delete_selected_categories']
    
    def food_count(self, obj):
        return obj.foods_set.count()
    food_count.short_description = "Foods"
    
    def special_count(self, obj):
        return obj.special_set.count()
    special_count.short_description = "Specials"
    
    def delete_selected_categories(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} categories deleted successfully.')
    delete_selected_categories.short_description = "Delete selected categories"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at', 'is_read', 'message_preview')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submitted_at',)
    list_editable = ('is_read',)
    ordering = ('-submitted_at',)
    actions = ['mark_as_read', 'mark_as_unread', 'delete_selected_messages']
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message Preview"
    
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} messages marked as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    def delete_selected_messages(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} contact messages deleted successfully.')
    delete_selected_messages.short_description = "Delete selected messages"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'food__title')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests', 'is_confirmed', 'submitted_at')
    list_filter = ('date', 'is_confirmed')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-submitted_at',)
    actions = ['mark_confirmed', 'mark_unconfirmed']

    def mark_confirmed(self, request, queryset):
        count = queryset.update(is_confirmed=True)
        self.message_user(request, f'{count} reservations marked as confirmed.')
    mark_confirmed.short_description = "Mark selected as confirmed"

    def mark_unconfirmed(self, request, queryset):
        count = queryset.update(is_confirmed=False)
        self.message_user(request, f'{count} reservations marked as unconfirmed.')
    mark_unconfirmed.short_description = "Mark selected as unconfirmed"

@admin.register(CateringRequest)
class CateringRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'event_type', 'guests', 'is_handled', 'submitted_at')
    list_filter = ('event_date', 'is_handled', 'event_type')
    search_fields = ('name', 'email', 'phone', 'event_type')
    ordering = ('-submitted_at',)
    actions = ['mark_handled', 'mark_unhandled']

    def mark_handled(self, request, queryset):
        count = queryset.update(is_handled=True)
        self.message_user(request, f'{count} requests marked as handled.')
    mark_handled.short_description = "Mark selected as handled"

    def mark_unhandled(self, request, queryset):
        count = queryset.update(is_handled=False)
        self.message_user(request, f'{count} requests marked as unhandled.')
    mark_unhandled.short_description = "Mark selected as unhandled"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'employee_id', 'phone')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'employee_id', 'phone')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # If this is an add form
            form.base_fields['user_type'].initial = 'waiter'
        return form

# Create a custom User admin that includes profile
from django.contrib.admin import TabularInline

class UserProfileInline(TabularInline):
    model = UserProfile
    extra = 1
    max_num = 1
    fields = ['user_type', 'phone', 'employee_id']

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin site customization
admin.site.site_header = "Restaurant Management System"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Welcome to Restaurant Management"

# Alternative registration method (backup)
# admin.site.register(Contact, ContactAdmin)