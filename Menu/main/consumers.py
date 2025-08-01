import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Order, Foods, Special

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'orders'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'order_update':
            # Send order update to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'order_update',
                    'order_id': text_data_json['order_id'],
                    'status': text_data_json['status'],
                    'message': text_data_json.get('message', '')
                }
            )

    async def order_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'order_id': event['order_id'],
            'status': event['status'],
            'message': event['message']
        }))

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.order_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def order_status_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_id': event['order_id'],
            'status': event['status'],
            'message': event['message'],
            'timestamp': event.get('timestamp')
        }))

class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Only allow staff/admin users
        user = self.scope["user"]
        if user.is_anonymous or not user.is_staff:
            await self.close()
            return
            
        self.room_group_name = 'admin_notifications'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def new_order(self, event):
        # Send new order notification to admin
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order_id': event['order_id'],
            'customer_name': event['customer_name'],
            'total': event['total'],
            'message': event['message']
        }))

class MenuConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'menu_updates'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'menu_update':
            # Send menu update to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'menu_update',
                    'item_id': text_data_json['item_id'],
                    'item_type': text_data_json['item_type'],
                    'action': text_data_json['action'],
                    'data': text_data_json.get('data', {})
                }
            )

    async def menu_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'menu_update',
            'item_id': event['item_id'],
            'item_type': event['item_type'],
            'action': event['action'],
            'data': event['data']
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            "notifications",
            {
                'type': 'notification_message',
                'message': message
            }
        )

    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class WaiterNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "waiter_notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "waiter_notifications",
            self.channel_name
        )

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message']
        }))
