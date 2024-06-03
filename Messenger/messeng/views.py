from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Chat, Message
from .forms import MessageForm


@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'messeng/chat_list.html', {'chats': chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('chat_list')

    messages = chat.messages.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'messeng/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if not request.user.has_perm('messenger.can_edit_message') and request.user != message.author:
        raise PermissionDenied
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=message.chat.id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'messeng/edit_message.html', {'form': form})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if not request.user.has_perm('messenger.can_remove_message') and request.user != message.author:
        raise PermissionDenied
    chat_id = message.chat.id
    message.delete()
    return redirect('chat_detail', chat_id=chat_id)
