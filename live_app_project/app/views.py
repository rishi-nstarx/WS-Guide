from django.shortcuts import render, HttpResponse
from .models import Chat, Group
from channels.consumer import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
def check(request, group_name):
    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group(name=group_name)
        group.save()
    return render(request, 'app/index.html', {'groupname': group_name, 'chats': chats})


def msg_from_outside(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'indian',
        {
            'type': 'chat.message',
            'message': 'Message from outside consumer'
        }
    )
    return HttpResponse("Message sent from view to consumer.")