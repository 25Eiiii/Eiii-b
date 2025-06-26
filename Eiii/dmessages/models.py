from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_request = models.BooleanField(default=False)  # 대화 신청용 메시지 여부
    is_accepted = models.BooleanField(null=True, blank=True)  # 수락/거절 여부 저장

    def __str__(self):
        return f"{self.sender} ➝ {self.receiver}: {self.content[:20]}"