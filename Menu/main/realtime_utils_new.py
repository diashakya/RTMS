"""
Real-time utilities for WebSocket notifications
"""
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
import json

def send_new_order_notification(order):
    """Send new order notification to admin dashboard"""
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'admin_notifications',
            {
                'type': 'new_order',
                'order_id': order.id,
                'customer_name': f"{order.customer.customer_firstname} {order.customer.customer_lastname}" if order.customer else "Guest",
                'total': str(order.total),
                'message': f'New order #{order.id} received from {order.customer.customer_firstname if order.customer else "Guest"}'
            }
        )

def send_order_update(order_id, status, message):
    """Send order status update to specific order channel"""
    channel_layer = get_channel_layer()
    if channel_layer:
        # Send to specific order channel
        async_to_sync(channel_layer.group_send)(
            f'order_{order_id}',
            {
                'type': 'order_status_update',
                'order_id': order_id,
                'status': status,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Also send to general orders channel for admin
        async_to_sync(channel_layer.group_send)(
            'orders',
            {
                'type': 'order_update',
                'order_id': order_id,
                'status': status,
                'message': message
            }
        )

def send_user_notification(user_id, title, message, notification_type='info'):
    """Send notification to specific user"""
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user_id}',
            {
                'type': 'user_notification',
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'timestamp': datetime.now().isoformat()
            }
        )

def send_order_status_notification(order, status):
    """Send order status notification to customer if they're a user"""
    if order.user:
        status_messages = {
            'pending': {'title': 'Order Confirmed', 'message': f'Your order #{order.id} is being prepared', 'type': 'info'},
            'completed': {'title': 'Order Ready!', 'message': f'Your order #{order.id} is ready for pickup/delivery', 'type': 'success'},
            'cancelled': {'title': 'Order Cancelled', 'message': f'Your order #{order.id} has been cancelled', 'type': 'warning'}
        }
        
        if status in status_messages:
            msg = status_messages[status]
            send_user_notification(
                order.user.id,
                msg['title'],
                msg['message'],
                msg['type']
            )
