from celery import shared_task
import logging
from messenger.models import Message

logger = logging.getLogger(__name__)

@shared_task
def log_last_10_messages():
    messages = Message.objects.order_by('-timestamp')[:10]
    for message in messages:
        logger.info(f"{message.timestamp} - {message.author}: {message.content}")