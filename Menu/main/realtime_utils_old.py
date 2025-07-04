from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

channel_layer = get_channel_layer()

def send_order_update(order_id, status, message=""):
    """Send order status update to all connected clients."""
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'orders',
            {
                'type': 'order_update',
                'order_id': order_id,
                'status': status,
                'message': message
            }
        )

def send_new_order_notification(order_data):
    """Send new order notification to staff."""
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'orders',
            {
                'type': 'new_order',
                'order': order_data
            }
        )

def send_menu_update(item_id, item_type, action, data=None):
    """Send menu update to all connected clients."""
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'menu_updates',
            {
                'type': 'menu_update',
                'item_id': item_id,
                'item_type': item_type,
                'action': action,  # 'updated', 'deleted', 'created', 'availability_changed'
                'data': data or {}
            }
        )

def send_user_notification(user_id, title, message, notification_type='info'):
    """Send notification to a specific user."""
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'notification',
                'title': title,
                'message': message,
                'notification_type': notification_type
            }
        )

def send_order_notification_to_user(user_id, order_id, status, message):
    """Send order-specific notification to a user."""
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'order_notification',
                'order_id': order_id,
                'status': status,
                'message': message
            }
        )

def send_staff_notification(title, message, notification_type='info'):
    """Send notification to all staff members."""
    if channel_layer:
        # Send to general staff channel
        async_to_sync(channel_layer.group_send)(
            'staff_notifications',
            {
                'type': 'notification',
                'title': title,
                'message': message,
                'notification_type': notification_type
            }
        )
