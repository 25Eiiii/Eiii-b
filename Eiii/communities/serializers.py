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
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'major', 'year', 'title', 'content', 'created_at', 'parent', 'replies']
        read_only_fields = ['user', 'replies']

    def get_major(self, obj):
        return getattr(obj.user.profile, 'major', None)

    def get_year(self, obj):
        return getattr(obj.user.profile, 'year', None)

    def get_nickname(self, obj):
        return getattr(obj.user, 'nickname', None)
    
    def get_replies(self, obj):
        replies = obj.replies.all().order_by('created_at')
        return CommentSerializer(replies, many=True).data

    def validate_parent(self, value):
        if value and value.parent is not None:
            raise serializers.ValidationError("답댓글의 답댓글은 작성할 수 없습니다.")
        return value
