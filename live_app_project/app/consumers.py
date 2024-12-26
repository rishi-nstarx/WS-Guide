# https://channels.readthedocs.io/en/latest/topics/consumers.html#

from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
from asgiref.sync import async_to_sync
import asyncio
import json
import redis

from .models import Chat, Group


# # Works Synchronously
# class MySyncConsumer(SyncConsumer):

#     # The following are the handlers that are predefined in 'SyncConsumer' and are always called whenever an event is triggered.
#     # This 'websocket_connect' handler gets called when clients initialy open a connection and is about to finish WS handshake.
#     def websocket_connect(self, event):

#         print("Websocket Connected....",event)
#         # To make the connection persistent. So that it will not be closed instantly just after connecting.
#         self.send({
#             'type': 'websocket.accept',  # it is called events/messages. there are so many, which works under different handlers.
#             #  'type': 'websocket.connect',
#         })
            
    
#     # # This handler is called when data received from client.
#     # def websocket_receive(self, event):

#     #     print("Message Received....", event["text"])
#     #     # Here we are sending message to the client from server.
#     #     for i in range(50):
#     #         self.send({
#     #             'type': 'websocket.send',
#     #             # 'type': 'websocket.receive',
#     #             'text': str(f'This is the message from server {i}')
#     #         })
#     #         sleep(0.5)


#     # This handler is called when data received from client.
#     def websocket_receive(self, event):

#         print("Message Received....", event["text"])
#         # Here we are sending message to the client from server.
#         for i in range(50):
#             self.send({
#                 'type': 'websocket.send',
#                 # 'type': 'websocket.receive',
#                 'text': json.dumps({"count": i})
#             })
#             sleep(0.5)

#     # Always gets called whenever the connection gets lost/closed for any reason.
#     def websocket_disconnect(self, event):

#         print("Websocket disconnected....", event)
#         self.send({
#             # 'type': 'websocket.disconnect',
#             # 'type': 'websocket.close',
#         })
#         raise StopConsumer()




# Works Synchronously
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        # print("Websocket Connected....",event)
        # print("Channel layer ---->", self.channel_layer) # Default channel layer
        # print("Channel name ---->", self.channel_name) # channel name
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        # print("Group name--->", self.group_name) #Websocket url (routing.py)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name) # Be careful when you are using 'async_to_sync' with parenthesis.
        
        self.send({
            'type': 'websocket.accept',
        })



    def websocket_receive(self, event):
        print("Message Received from client....", event)
        group_name = self.scope['url_route']['kwargs']['group_name']

        group = Group.objects.get(name = self.group_name)
        print("User-------->", self.scope['user'])
        if self.scope['user'].is_authenticated:
            
            data = json.loads(event['text'])
            chat = Chat(content=data['msg'], group = group)
            chat.save()

            data['user'] = self.scope['user'].username

            async_to_sync(self.channel_layer.group_send)(group_name,{
                'type': 'chat.message', # custom event/messsage for 'chat_message'.
                'message': json.dumps(data)
            })
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Login Required!"}) # this 'msg' key is cutsom format from frontend.
            })

    # This is custom handler for 'chat.message' because we always replace '.' with '_' in handlers.
    # This will be repeatedly called for each channel.
    def chat_message(self, event):
        print('Event--->', event)
        print('Actual Data--->', event['message'], self.channel_name)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })



    def websocket_disconnect(self, event):
        print("Websocket disconnected....", event)
        print("Channel layer ---->", self.channel_layer) # Default channel layer
        print("Channel name ---->", self.channel_name) # channel name
        async_to_sync(self.channel_layer.group_discard)('programmers', self.channel_name)
        raise StopConsumer()





# # Works Asynchronously
# class MyAsyncConsumer(AsyncConsumer):

#     # Following are the called handlers which is predefined in 'SyncConsumer'.
#     async def websocket_connect(self, event):
#         print("Websocket Connected Asynchronously....", event)
#         # To make the connection persistent.
#         await self.send({
#             'type': 'websocket.accept'
#         })

#     async def websocket_receive(self, event):
#         print("Message Received Asynchronously....", event)

#         for i in range(50):
#             await self.send({
#                 'type': 'websocket.send',
#                 # 'type': 'websocket.receive',
#                 'text': str(f'Message sent to client {i}')
#             })
#             await asyncio.sleep(0.5)

#     async def websocket_disconnect(self, event):
#         print("Websocket disconnected....", event)
#         raise StopConsumer()


#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------





# from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


# Sync Generic Consumer
# class MyWebSocketConsumer(WebsocketConsumer):
#     # Called  when  client initially opens a connection and is about to finish the websocket handshake.
#     def connect(self):
#         self.accept() # To accept the connection.
#         print('Websocket conncted...')

#     def receive(self, text_data=None, bytes_data=None):
#         print('Message received from client...', text_data)
#         self.send(text_data="Message from server to client.")
#         # self.close(code=1234) # To close forcefully. 
#         # self.send() # To send binary frame to client.


#     def disconnect(self, code):
#         print('Websocket Disconnected...', code)





# # Async Generic Consumer.
# class MyAsyncWebSocketConsumer(AsyncWebsocketConsumer):
#     # Called  when  client initially opens a connection and is about to finish the websocket handshake.
#     async def connect(self):
#         await self.accept() # To accept the connection.
#         print('Websocket conncted...')

#     async def receive(self, text_data=None, bytes_data=None):
#         print('Message received from client...', text_data)
#         await self.send(text_data="Message from server to client.")
#         # await self.close(code=1234) # To close forcefully. 
#         # await self.send() # To send binary frame to client.


#     async def disconnect(self, code):
#         print('Websocket Disconnected...', code)


# All the events and handlres we can apply in generic consumers in the same way as we have applied in the
# non generic consumers.







# --------------JsonWebSocketConsumer(JsonWebsocketConsumer) Just for example not working--------------------

# from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer

# class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         print('Websocket Connected')
#         self.accept()

#     def receive_json(self, content, **kwargs):
#         print("Message received from client", content)
#         self.send_json({"message": "Message sent to client"})

#     def disconnect(self, code):
#         print("Websocket disconnect", code)


# class MyAsyncWebsocketConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         print('Websocket Connected')
#         await self.accept()

#     async def receive_json(self, content, **kwargs):
#         print("Message received from client", content)
#         self.send_json({"message": "Message sent to client"})

#     async def disconnect(self, code):
#         print("Websocket disconnect", code)