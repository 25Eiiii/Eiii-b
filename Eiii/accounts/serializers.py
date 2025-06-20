from rest_framework import serializers
from .models import CustomUser
import re
from .models import Profile

#회원가입
class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email', 'phone']
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
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
#매칭 프로필 상세보기용
class ProfileSerializer(serializers.ModelSerializer):
    preferred_menu = serializers.ListField(child=serializers.CharField())
    dietary_restrictions = serializers.ListField(child=serializers.CharField())
    username = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        #exclude = ['user'] 해당 프로필을 소유한 사용자 ID 숨기려면 
        read_only_fields = ['user']    
    
    def get_nickname(self, obj):
        return getattr(obj.user, 'nickname', None)
    def get_username(self, obj):
        return obj.user.username

#매칭 프로필 미리보기용
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
