from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversations_list, name='chat'),
    path('start/<uuid:item_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]
