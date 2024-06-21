from django.core.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from messeng.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessageDetailSerializer


class UserChatsView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class ChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id, chat__participants=self.request.user)


class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer
    permission_classes = [IsAuthenticated]


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MessageUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this message")
        serializer.save()


class MessageDeleteView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this message")
        instance.delete()

