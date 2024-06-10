import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import Message

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def log_message_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Message {instance.id} sent by {instance.author} in chat {instance.chat.id}")
        if instance.chat.participants.filter(is_superuser=True).exists():
            messages.add_message(instance.author, messages.SUCCESS, 'Ви успiшно надіслали повідомлення суперюзеру')
