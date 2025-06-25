from rest_framework import serializers
from .models import Post, Comment
from accounts.models import Profile

class PostSerializer(serializers.ModelSerializer):
    major = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'major', 'year', 'category', 'title', 'content', 'created_at']
        read_only_fields = ['user']  

    def get_major(self, obj):
        return getattr(obj.user.profile, 'major', None)

    def get_year(self, obj):
        return getattr(obj.user.profile, 'year', None)

    def get_nickname(self, obj):
        return getattr(obj.user, 'nickname', None)
    
class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    major = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'major', 'year', 'title', 'content', 'created_at']
        read_only_fields = ['user']  

    def get_major(self, obj):
        return getattr(obj.user.profile, 'major', None)

    def get_year(self, obj):
        return getattr(obj.user.profile, 'year', None)

    def get_nickname(self, obj):
        return getattr(obj.user, 'nickname', None)
