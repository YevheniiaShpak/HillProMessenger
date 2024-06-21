from rest_framework import serializers
from messeng.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'participants']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'content', 'timestamp']


class MessageDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'content', 'timestamp']
