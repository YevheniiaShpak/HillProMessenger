from django.urls import path
from .views import (
    UserChatsView,
    ChatMessagesView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView
)

urlpatterns = [
    path('chats/', UserChatsView.as_view(), name='user-chats'),
    path('chats/<int:chat_id>/messages/', ChatMessagesView.as_view(), name='chat-messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message-edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),
]
