import logging
from django.db.models.signals import post_save
from django.contrib import messages
from .models import Message
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserStatus

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def log_message_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Message {instance.id} sent by {instance.author} in chat {instance.chat.id}")
        if instance.chat.participants.filter(is_superuser=True).exists():
            messages.add_message(instance.author, messages.SUCCESS, 'Ви успiшно надіслали повідомлення суперюзеру')


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': True})


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': False})