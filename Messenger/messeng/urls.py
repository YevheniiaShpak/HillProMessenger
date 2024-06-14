from django.urls import path
from . import views
from .views import UserStatusDetail


urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('api/status/<str:user__username>/', UserStatusDetail.as_view(), name='user-status-detail'),
]
