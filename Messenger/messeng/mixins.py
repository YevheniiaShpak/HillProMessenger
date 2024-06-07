from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View


#1
class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


#2
class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


#3
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


#4
class UserIsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        pass


#5
class UserInChatMixin:
    def dispatch(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, id=kwargs['chat_id'])
        if request.user not in chat.users.all():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


#6
class AddContextDataMixin:
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


#7
class FormHandleMixin:
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


#8
class UserHasPermissionMixin(UserPassesTestMixin):
    permission_required = None

    def test_func(self):
        return self.request.user.has_perm(self.permission_required)


#9
class AjaxRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


#10
class LogActionMixin:
    def dispatch(self, request, *args, **kwargs):
        print(f"Action by {request.user} on {request.path}")
        return super().dispatch(request, *args, **kwargs)
