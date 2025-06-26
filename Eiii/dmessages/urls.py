from django.urls import path
from .views import (
    MessageRequestView,
    ReceivedRequestListView,
    RespondToRequestView,
    AcceptedMessagesView,
)

urlpatterns = [
    path('request/', MessageRequestView.as_view(), name='message-request'),
    path('request/received/', ReceivedRequestListView.as_view(), name='received-requests'),
    path('request/<int:pk>/respond/', RespondToRequestView.as_view(), name='respond-request'),
    path('accepted/', AcceptedMessagesView.as_view(), name='accepted-messages'),
]