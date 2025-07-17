from django.urls import path
from .views import (
    MessageRequestView,
    ReceivedRequestListView,
    RespondToRequestView,
    AcceptedMessagesView,
    ChatRoomListView,
    ChatRoomMessageListView,
    SendMessageView,
    ReadMessageView
)

urlpatterns = [
    path('request/', MessageRequestView.as_view(), name='message-request'),
    path('request/received/', ReceivedRequestListView.as_view(), name='received-requests'),
    path('request/<int:pk>/respond/', RespondToRequestView.as_view(), name='respond-request'),
    path('accepted/', AcceptedMessagesView.as_view(), name='accepted-messages'),
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:chatroom_id>/messages/', ChatRoomMessageListView.as_view(), name='chatroom-messages'),
    path('chatrooms/<int:chatroom_id>/messages/send/', SendMessageView.as_view(), name='send-message'),
    path('<int:pk>/read/', ReadMessageView.as_view(), name='read-message'),
]