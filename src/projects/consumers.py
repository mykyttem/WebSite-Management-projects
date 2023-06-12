import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatTeam, MessagesChatTeam

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        login_user = self.scope['session']['user-login']


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message,
                'login_user': login_user
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        login_user = event['login_user']
        session_login = self.scope['session'].get('user-login')
        
        await self.save_message(chat_id=self.room_name, login_author=login_user, message=message)


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            'login_user': login_user,
            'session_login': session_login
        }))


    @database_sync_to_async
    def save_message(self, chat_id, login_author, message):

        message = MessagesChatTeam(chat_id=chat_id, login_author=login_author, message=message)
        message.save()   
