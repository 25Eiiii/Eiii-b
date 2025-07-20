from rest_framework import serializers
from .models import Message, ChatRoom
from accounts.models import CustomUser  # 사용자모델

class MessageSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.SerializerMethodField()
    receiver_nickname = serializers.SerializerMethodField()
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)
    sender_major = serializers.SerializerMethodField()
    sender_grade = serializers.SerializerMethodField()
    chatroom_id = serializers.SerializerMethodField()
    receiver = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',#메시지를 보낸 사용자 (자동 설정)
            'sender_nickname',
            'sender_id',
            'receiver',#메시지를 받을 사용자 (프론트에서 전달받음)
            'receiver_nickname',
            "sender_major", "sender_grade",
            'content',#쪽지 내용
            'timestamp',
            'is_read',#읽음 여부
            'is_request',#대화 신청 메시지 여부 (True면 대화 요청 메시지)
            'is_accepted',#수락(True), 거절(False), 아직 응답 없음(None)
            'chatroom_id',
        ]
        read_only_fields = [
            'id', 'sender', 'sender_nickname', 'receiver_nickname',
            'timestamp', 'sender_id', 'sender_major', 'sender_grade', 'chatroom_id'
        ]

    def get_sender_nickname(self, obj):
        return obj.sender.nickname

    def get_receiver_nickname(self, obj):
        return obj.receiver.nickname
    
    def get_sender_major(self, obj):
        return obj.sender.profile.major if hasattr(obj.sender, 'profile') else None

    def get_sender_grade(self, obj):
        return obj.sender.profile.year if hasattr(obj.sender, 'profile') else None
    
    def get_chatroom_id(self, obj):
        return obj.chatroom.id if hasattr(obj, 'chatroom') and obj.chatroom else None
    
    def validate(self, data):
        is_request = self.initial_data.get("is_request", False)
        content = self.initial_data.get("content", "").strip()  # 💡 여기 수정

        print("📍 validate() 진입")
        print("▶ is_request:", is_request)
        print("▶ content:", content)

        if not is_request and not content:
            raise serializers.ValidationError({"content": "쪽지 내용은 필수입니다."})

        return data

    
#쪽지 요청함에 들어갈 리스트 정보들
class MessageRequestPreviewSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.CharField(source='sender.nickname')
    sender_major = serializers.CharField(source='sender.profile.major')
    sender_year = serializers.CharField(source='sender.profile.year')
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_nickname', 'sender_major', 'sender_year', 'sender_id', 'timestamp']



class ChatRoomSerializer(serializers.ModelSerializer):
    other_participant_nickname = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'created_at', 'other_participant_nickname']

    def get_other_participant_nickname(self, obj):
        user = self.context['request'].user
        other = obj.participants.exclude(id=user.id).first()
        return other.nickname if other else None