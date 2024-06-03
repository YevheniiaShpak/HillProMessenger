from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Chat(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("edit_message", "Can edit message"),
            ("delete_message", "Can delete message"),
        ]

    def __str__(self):
        return f'Message by {self.author} in {self.chat}'


@receiver(post_save, sender=Message)
def set_message_permissions(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(Message)
        permission_edit = Permission.objects.get(
            codename='edit_message', content_type=content_type)
        permission_delete = Permission.objects.get(
            codename='delete_message', content_type=content_type)
        instance.author.user_permissions.add(permission_edit)
        instance.author.user_permissions.add(permission_delete)
