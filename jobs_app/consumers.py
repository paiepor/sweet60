import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        self.other_user_id = int(self.scope['url_route']['kwargs']['user_id'])
        ids = sorted([self.user.id, self.other_user_id])
        self.room_name = f'chat_{ids[0]}_{ids[1]}'

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('content', '').strip()
        if not content:
            return

        msg = await self.save_message(content)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'content': content,
                'sender_id': self.user.id,
                'timestamp': timezone.localtime(msg.timestamp).strftime('%H:%M'),
                'message_id': msg.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'content': event['content'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def save_message(self, content):
        other_user = User.objects.get(id=self.other_user_id)
        return ChatMessage.objects.create(
            sender=self.user,
            receiver=other_user,
            content=content,
        )
