from django.db import models
from django.conf import settings
# Create your models here.

class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    place = models.CharField(max_length=200)
    memo = models.TextField(blank=True)
    date = models.DateField()  # 약속 날짜
    time = models.CharField(max_length=100)
    # time = models.TimeField(null=True, blank=True)  # 선택사항
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname} - {self.title} on {self.date}"