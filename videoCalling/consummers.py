from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoCallConsummer(AsyncWebsocketConsumer):
    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"video_call-{room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(room_id)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        message = receive_dict['message']
        action = receive_dict['action']

        if action == 'new-offer' or action == 'new-answer':
            receiver_channel_name = receive_dict['message']['receiver_channel_name']
            print('channel_name:', receiver_channel_name)
            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name, {
                    'type': 'send.sdp',
                    'message': message,
                    'receive_dict': receive_dict
                }
            )

            return

        receive_dict['message']['receiver_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'send.sdp',
                'message': message,
                'receive_dict': receive_dict
            }
        )

    async def send_sdp(self, event):
        receive_dict = event['receive_dict']

        await self.send(text_data=json.dumps(receive_dict))
