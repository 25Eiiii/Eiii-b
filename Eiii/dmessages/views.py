from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer, MessageRequestPreviewSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.

User = get_user_model()

#대화 신청(쪽지 요청) 보내기
class MessageRequestView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, is_request=True)

#내가 받은 쪽지 요청 목록
class ReceivedRequestListView(generics.ListAPIView):
    serializer_class = MessageRequestPreviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            receiver=self.request.user,
            is_request=True,
            is_accepted__isnull=True
        ).order_by('-timestamp')

#쪽지 수락, 거절
class RespondToRequestView(generics.UpdateAPIView):
    queryset = Message.objects.filter(is_request=True)
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        message = self.get_object()

        if message.receiver != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        decision = request.data.get("is_accepted")
        if decision not in [True, False]:
            return Response({"detail": "is_accepted는 true 또는 false여야 합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        message.is_accepted = decision
        message.save()
        return Response(MessageSerializer(message).data)

#쪽지 보관함(쪽지 요청 수락된 쪽지 목록)
class AcceptedMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            is_request=True,
            is_accepted=True
        ).filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by('-timestamp')