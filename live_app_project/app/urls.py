from django.urls import path
from . import views

urlpatterns = [
    path('<str:group_name>/', views.check),
    path('msg/outside/', views.msg_from_outside),
]