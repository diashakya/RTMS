from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Special, Foods, Category, Favorite, Order, OrderItem, Customer, Cart, CartItem

# Enhanced Order Item Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('food', 'special', 'quantity', 'price', 'total_price')

# Enhanced Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'order_type_display', 'user', 'status', 'total', 'created_at', 'order_actions')
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
    
    def order_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View Receipt</a>&nbsp;'
            '<a class="button" href="{}">Send Status Email</a>',
            reverse('order_receipt', args=[obj.id]),
            reverse('send_status_email', args=[obj.id])
        )
    order_actions.short_description = "Actions"
    order_actions.allow_tags = True
    
    actions = ['mark_completed', 'mark_cancelled', 'send_confirmation_emails']
    
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

@admin.register(Foods)
class FoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'is_spicy', 'rating')
    list_filter = ('category', 'is_spicy')
    search_fields = ('title',)
    list_editable = ('price', 'is_spicy', 'rating')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_count', 'special_count')
    search_fields = ('name',)
    
    def food_count(self, obj):
        return obj.foods_set.count()
    food_count.short_description = "Foods"
    
    def special_count(self, obj):
        return obj.special_set.count()
    special_count.short_description = "Specials"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'food__title')

# Admin site customization
admin.site.site_header = "Restaurant Management System"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Welcome to Restaurant Management"