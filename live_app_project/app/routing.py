# We  can write all this code in asgi.py file also but it is the most preferable
# and standard way to write here in routing.py file.


from django.urls import path
from channels.routing import URLRouter
from . import consumers


# You can name it whatever you want instead of 'websocket_urlpatterns'.
# You will have to mention this in asgi.py file also.
websocket_urlpatterns = [
    # path('ws/sc/', consumers.MySyncConsumer.as_asgi()),
    path('ws/sc/<str:group_name>/', consumers.MySyncConsumer.as_asgi()),
    # path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     # path('ws/wsc/', consumers.MyWebSocketConsumer.as_asgi()),
#     path('ws/awsc/', consumers.MyAsyncWebSocketConsumer.as_asgi()),
    
# ]