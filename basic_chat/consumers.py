# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.http import HttpResponse,JsonResponse,Http404
import json
from .models import Thread,UserThread,Message,DeletedMesssage
from django.contrib.auth.models import User
# from .custom.rsa_encryption import RSAEncrypt,PublicKey


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        try:
            self.thread = Thread.objects.get(pk=int(self.room_name))
            if (self.thread==None):
                await self.close()
                raise Http404
        except Exception as e:
            print(e) 
            await self.close()
            raise Http404
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accept the connection
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['msg']
        data_about = text_data_json['data_about']
        print(text_data_json)
        sender_id = text_data_json['sender_id']

        sender = User.objects.get(pk=sender_id)
        msg_id = await self.storeMessage(sender,msg)

        # msg_id = 1

        print('msg_id  ---------------------------------',msg_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg': msg,
                'msg_id' : msg_id,
                'sender_id' : sender_id, 
                'data_about': data_about,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        msg = event['msg']
        data_about = event['data_about']
        msg_id = event['msg_id']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data_about' : data_about,
            'msg': msg,
            'msg_id' : msg_id,
            'sender_id' : sender_id, 
        }))
        
    @database_sync_to_async
    def storeMessage(self,sender,msg):
        # return Message.objects.all()[0].id
        thread = UserThread.objects.filter(thread=self.thread)
        
        if (thread.count() >= 2) :
            msg = Message()
            msg.sender = sender
            msg.message = msg
            msg.save()
            print('msg_id -------------sdfsdf sdfsd-------------')
            print(msg.id)
            return msg.id
        else : 
            raise Http404
            return None