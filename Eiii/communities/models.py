from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from accounts.models import Profile

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('offhand', '즉석밥약'),
        ('mentoring', '선후배밥약'),
        ('regular', '정기밥약'),
        ('classmate', '같은수업밥약'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(verbose_name="사진",
                              blank=True, null=True, upload_to='post_photo')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    #답댓글 기능을 위한 부모 댓글 ID 생성
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )

    def __str__(self):
        return f"{self.user.nickname} - {self.content[:20]}"
