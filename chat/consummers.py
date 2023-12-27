import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Document
from channels.db import database_sync_to_async

#consumer for chat

class ChatConsummer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.room_id = ''
        
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat-{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_id,'chat')
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'send_msg',
                'receive_dict': receive_dict
            }
        )

    async def send_msg(self, event):
        receive_dict = event['receive_dict']
        await self.send(text_data=json.dumps(receive_dict))




#consumer for Document sharing

class DocumentConsummer(AsyncWebsocketConsumer):
    
    def __init__(self):
        super().__init__()
        self.room_id = ''
        
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"document-{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_id,'doc')
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'send_doc',
                'document': 'all'
            }
        )
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'send_doc',
                'document': 'all'
            }
        )

    async def send_doc(self, event):
        print('doc send')
        documents = event['document']
        # if documents == 'all':
        queryset = await self.getDoc()
        
        print(queryset)
           
        await self.send(text_data=json.dumps(queryset))
        
    @database_sync_to_async
    def getDoc(self):
        return list(Document.objects.values().filter(room_id = self.room_id))