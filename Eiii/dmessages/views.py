from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Message, ChatRoom
from .serializers import (
    MessageSerializer, MessageRequestPreviewSerializer,
    ChatRoomSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import PermissionDenied

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

        # 수락 시 채팅방 생성 + 연결
        if decision is True:
            chatroom = ChatRoom.objects.create()
            chatroom.participants.set([message.sender, message.receiver])
            message.chatroom = chatroom

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
    

#채팅방 목록 조회
class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user).order_by('-created_at')


class ChatRoomMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']
        return Message.objects.filter(
            chatroom_id=chatroom_id,
            is_request=False,  
        ).order_by('timestamp')

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chatroom_id = self.kwargs['chatroom_id']
        chatroom = ChatRoom.objects.get(id=chatroom_id)

        # 유저가 대화 참여자인지 확인
        if not chatroom.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied("이 채팅방에 접근 권한이 없습니다.")

        receiver = chatroom.participants.exclude(id=self.request.user.id).first()
        serializer.save(sender=self.request.user, receiver=receiver, chatroom=chatroom, is_request=False)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("❌ serializer.errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 유효하면 원래의 post 로직대로 진행 → perform_create() 호출됨
        return super().post(request, *args, **kwargs)
class ReadMessageView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer  

    def patch(self, request, *args, **kwargs):
        message = self.get_object()

        # 본인이 받은 메시지만 읽음 처리 가능
        if message.receiver != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        if message.is_read:
            return Response({"detail": "이미 읽은 메시지입니다."}, status=status.HTTP_400_BAD_REQUEST)

        message.is_read = True
        message.save()
        return Response(self.get_serializer(message).data)