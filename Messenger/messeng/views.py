from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from django.urls import reverse_lazy
from .models import Chat, Message
from .mixins import (
    LoginRequiredMixin,
    UserIsAuthorMixin,
    UserInChatMixin,
    SuperUserRequiredMixin,
    AddContextDataMixin,
    FormHandleMixin
)
from .forms import MessageForm


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'messeng/chat_list.html'
    context_object_name = 'chats'


class ChatDetailView(LoginRequiredMixin, UserInChatMixin, AddContextDataMixin, DetailView):
    model = Chat
    template_name = 'messeng/chat_detail.html'
    context_object_name = 'chat'
    extra_context = {'form': MessageForm()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(chat=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        chat = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', chat.id)
        context = self.get_context_data(object=chat)
        context['form'] = form
        return self.render_to_response(context)


class MessageEditView(LoginRequiredMixin, UserIsAuthorMixin, FormHandleMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messeng/edit_message.html'

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'pk': self.object.chat.id})


class MessageDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    model = Message
    template_name = 'messeng/delete_message.html'

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'pk': self.object.chat.id})


class ChatForm:
    pass


class ChatCreateView(LoginRequiredMixin, SuperUserRequiredMixin, FormHandleMixin, CreateView):
    model = Chat
    form_class = ChatForm
    template_name = 'messeng/create_chat.html'
    success_url = reverse_lazy('chat_list')


class UserAddForm:
    pass


class AddUserToChatView(LoginRequiredMixin, SuperUserRequiredMixin, FormView):
    form_class = UserAddForm
    template_name = 'messeng/add_user_to_chat.html'

    def form_valid(self, form):
        chat = get_object_or_404(Chat, pk=self.kwargs['pk'])
        user = form.cleaned_data['user']
        chat.users.add(user)
        return redirect('chat_detail', pk=chat.pk)


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
