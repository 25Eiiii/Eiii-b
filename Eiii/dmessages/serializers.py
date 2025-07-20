from rest_framework import serializers
from .models import Message, ChatRoom
from accounts.models import CustomUser  # 사용자모델

class MessageSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.SerializerMethodField()
    receiver_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',#메시지를 보낸 사용자 (자동 설정)
            'sender_nickname',
            'receiver',#메시지를 받을 사용자 (프론트에서 전달받음)
            'receiver_nickname',
            'content',#쪽지 내용
            'timestamp',
            'is_read',#읽음 여부
            'is_request',#대화 신청 메시지 여부 (True면 대화 요청 메시지)
            'is_accepted',#수락(True), 거절(False), 아직 응답 없음(None)
        ]
        read_only_fields = ['id', 'sender', 'sender_nickname', 'receiver_nickname','timestamp']

    def get_sender_nickname(self, obj):
        return obj.sender.nickname

    def get_receiver_nickname(self, obj):
        return obj.receiver.nickname
    
    def validate(self, data):
        
        #content는 쪽지 요청이 아닐 때만 필수로 설정
        is_request = self.initial_data.get("is_request", True)  # 기본 True로 간주
        content = data.get("content")

        if not is_request and not content:
            raise serializers.ValidationError({"content": "쪽지 내용은 필수입니다."})

        return data
    
#쪽지 요청함에 들어갈 리스트 정보들
class MessageRequestPreviewSerializer(serializers.ModelSerializer):
    sender = serializers.IntegerField(source='sender.id') 
    sender_nickname = serializers.CharField(source='sender.nickname')
    sender_major = serializers.CharField(source='sender.profile.major')
    sender_year = serializers.CharField(source='sender.profile.year')

    class Meta:
        model = Message
        fields = ['id', 'sender','sender_nickname', 'sender_major', 'sender_year', 'timestamp']



class ChatRoomSerializer(serializers.ModelSerializer):
    other_participant_nickname = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'created_at', 'other_participant_nickname']

    def get_other_participant_nickname(self, obj):
        user = self.context['request'].user
        other = obj.participants.exclude(id=user.id).first()
        return other.nickname if other else None