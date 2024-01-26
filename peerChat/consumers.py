import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Thread, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        userId = self.scope['url_route']['kwargs']['userId']
        print(userId)
        chat_room = f'user_chatroom_{userId}'
        if self.scope['user'].is_anonymous:
            await self.close(code=4001)
            return
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        print('receive', text_data)
        received_data = json.loads(text_data)
        msg = received_data.get('message')
        vcall = received_data.get('videocall',None)
        sent_by_id = received_data.get('sent_by')
        sent_by_name = received_data.get('sent_by_name')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        media_type = received_data.get('media_type')
        media = received_data.get('media')
        
        other_user_chat_room = f'user_chatroom_{send_to_id}'
        
        if vcall:
            if vcall == 'call':
                response = {
                    'type': vcall,
                    'user_to': send_to_id,
                    'thread_id': thread_id,
                    'user_by_name':sent_by_name,
                    'user_by_id':sent_by_id
                }
                
            elif vcall == 'decline':
                response = {
                    'type': vcall,
                    
                }
            
            elif vcall == 'answer':
                response = {
                    'type': vcall,
                    'thread_id': thread_id,
                }
                
            await self.channel_layer.group_send(
                other_user_chat_room,
                {
                    'type': 'send_vcall',
                    'vcall': json.dumps(response)
                }
            )    
        elif media_type:
            print('media-',media['media'],' type-',media_type)
            
        else:
            if msg != 'delete':
                thread_obj = await self.get_thread(thread_id)
                if thread_obj.block_by:
                    return
                chat = await self.create_chat_message(thread_obj, sent_by_id, msg)

                response = {
                    'id':chat.id,
                    'message': msg,
                    'userId': sent_by_id,
                    'userName':sent_by_name,
                    'thread_id': thread_id
                }
            else:
                id = received_data.get('id')
                await self.delete_msg(id)
                
                response = {
                    'delete_by':sent_by_id,
                    'message': 'deleted',
                    
                }
                
            await self.channel_layer.group_send(
                other_user_chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )



    async def disconnect(self, event):
        print('disconnect', event)



    async def chat_message(self, event):
        print('chat_message', event)
        await self.send(text_data=event['text']) 
        
        
        
    async def send_vcall(self,event):
        print('vcall',event)
        await self.send(text_data=event['vcall'])





    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
            obj.hide_by_frst = False
            obj.hide_by_second = False
            obj.save()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        chat = ChatMessage.objects.create(thread=thread, userId=user, message=msg)
        return chat
    
    @database_sync_to_async
    def delete_msg(self, id):
        ChatMessage.objects.get(id=id).delete()
