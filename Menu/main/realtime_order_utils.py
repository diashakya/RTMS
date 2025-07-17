"""
Real-time Order Tracking Utilities
Provides functions to broadcast order status updates via WebSocket channels
"""
import json
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Order

class OrderNotificationManager:
    """Manages real-time order notifications via WebSocket channels"""
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def broadcast_order_update(self, order_id, status, message=None, user_id=None):
        """
        Broadcast order status update to all relevant channels
        
        Args:
            order_id (int): Order ID
            status (str): New order status
            message (str): Optional custom message
            user_id (int): Optional user ID for targeted notifications
        """
        if not self.channel_layer:
            return False
            
        try:
            order = Order.objects.get(id=order_id)
            timestamp = timezone.now().isoformat()
            
            # Default messages for each status
            default_messages = {
                'pending': 'Your order has been received and is pending confirmation.',
                'confirmed': 'Your order has been confirmed and will be prepared soon.',
                'preparing': 'Your order is being prepared by our kitchen staff.',
                'ready': 'Your order is ready for pickup/delivery!',
                'completed': 'Your order has been completed. Thank you!',
                'cancelled': 'Your order has been cancelled.',
            }
            
            notification_message = message or default_messages.get(status, f'Order status updated to {status}')
            
            # 1. Broadcast to specific order channel (for order tracking page)
            async_to_sync(self.channel_layer.group_send)(
                f'order_{order_id}',
                {
                    'type': 'order_status_update',
                    'order_id': str(order_id),
                    'status': status,
                    'message': notification_message,
                    'timestamp': timestamp,
                    'customer_name': order.customer_name or (order.customer.name if order.customer else 'Guest'),
                    'total': str(order.total)
                }
            )
            
            # 2. Broadcast to general orders channel (for admin dashboard)
            async_to_sync(self.channel_layer.group_send)(
                'orders',
                {
                    'type': 'order_update',
                    'order_id': str(order_id),
                    'status': status,
                    'message': notification_message,
                    'timestamp': timestamp,
                    'customer_name': order.customer_name or (order.customer.name if order.customer else 'Guest'),
                    'total': str(order.total)
                }
            )
            
            # 3. Send notification to admin users
            async_to_sync(self.channel_layer.group_send)(
                'admin_notifications',
                {
                    'type': 'new_order',
                    'order_id': str(order_id),
                    'customer_name': order.customer_name or (order.customer.name if order.customer else 'Guest'),
                    'total': str(order.total),
                    'message': f'Order #{order_id} status changed to {status}'
                }
            )
            
            # 4. Send personal notification to user if they're registered
            if order.user_id:
                async_to_sync(self.channel_layer.group_send)(
                    f'user_{order.user_id}',
                    {
                        'type': 'order_notification',
                        'order_id': str(order_id),
                        'status': status,
                        'message': notification_message,
                        'timestamp': timestamp
                    }
                )
            
            return True
            
        except Order.DoesNotExist:
            print(f"Order {order_id} not found")
            return False
        except Exception as e:
            print(f"Error broadcasting order update: {e}")
            return False
    
    def broadcast_new_order(self, order_id):
        """
        Broadcast new order notification to admin users
        
        Args:
            order_id (int): Order ID
        """
        if not self.channel_layer:
            return False
            
        try:
            order = Order.objects.get(id=order_id)
            
            async_to_sync(self.channel_layer.group_send)(
                'admin_notifications',
                {
                    'type': 'new_order',
                    'order_id': str(order_id),
                    'customer_name': order.customer_name or (order.customer.name if order.customer else 'Guest'),
                    'total': str(order.total),
                    'message': f'New order #{order_id} received from {order.customer_name or "Guest"}'
                }
            )
            
            return True
            
        except Order.DoesNotExist:
            print(f"Order {order_id} not found")
            return False
        except Exception as e:
            print(f"Error broadcasting new order: {e}")
            return False

# Global instance
order_notification_manager = OrderNotificationManager()

# Helper functions for easy use
def notify_order_status_change(order_id, new_status, message=None):
    """
    Helper function to notify order status change
    
    Args:
        order_id (int): Order ID
        new_status (str): New order status
        message (str): Optional custom message
    """
    return order_notification_manager.broadcast_order_update(order_id, new_status, message)

def notify_new_order(order_id):
    """
    Helper function to notify about new order
    
    Args:
        order_id (int): Order ID
    """
    return order_notification_manager.broadcast_new_order(order_id)

def get_order_status_display(status):
    """
    Get user-friendly status display text
    
    Args:
        status (str): Order status
        
    Returns:
        str: User-friendly status text
    """
    status_display = {
        'pending': '🕐 Pending',
        'confirmed': '✅ Confirmed',
        'preparing': '👨‍🍳 Preparing',
        'ready': '🍽️ Ready',
        'completed': '✅ Completed',
        'cancelled': '❌ Cancelled',
    }
    return status_display.get(status, status.title())

def get_order_progress_percentage(status):
    """
    Get order progress percentage for progress bars
    
    Args:
        status (str): Order status
        
    Returns:
        int: Progress percentage (0-100)
    """
    progress_map = {
        'pending': 10,
        'confirmed': 25,
        'preparing': 60,
        'ready': 90,
        'completed': 100,
        'cancelled': 0,
    }
    return progress_map.get(status, 0)
