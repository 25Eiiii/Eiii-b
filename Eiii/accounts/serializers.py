from rest_framework import serializers
from .models import CustomUser
import re
from .models import Profile

#회원가입
class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'password', 'password2', 'email', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
            raise serializers.ValidationError("비밀번호는 영문과 숫자를 포함해야 합니다.")
        if not (8 <= len(value) <= 20):
            raise serializers.ValidationError("비밀번호는 8~20자여야 합니다.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
#프로필 상세보기용
class ProfileSerializer(serializers.ModelSerializer):
    preferred_menu = serializers.ListField(child=serializers.CharField())
    dietary_restrictions = serializers.ListField(child=serializers.CharField())
    username = serializers.CharField(source='user.username', required=False)
    nickname = serializers.CharField(source='user.nickname', required=False)
    
    #쪽지 receiver용
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'nickname',
            'major',
            'year',
            'preferred_gender',
            'dining_style',
            'eating_speed',
            'meal_purpose',
            'dessert',
            'preferred_menu',
            'dietary_restrictions',
            'user_id',
        ]
        read_only_fields = ['id']  # user는 perform_create나 get_object에서 처리함

    def update(self, instance, validated_data):
        # user 관련 정보 분리
        user_data = validated_data.pop('user', {})

        # 프로필 정보 수정
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 유저 정보 수정
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance

#프로필 미리보기용
class ProfilePreviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'nickname',
            'username',
            'dining_style',
            'meal_purpose',
            'eating_speed',
            'dessert',  # 미리보기 정보 4개는 나중에 수정 가능
        ]

    def get_nickname(self, obj):
        return getattr(obj.user, 'nickname', None)
    def get_username(self, obj):
        return obj.user.username
