from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings #프로파일 모델용
# Create your models here.

#관리자 계정
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, phone=None, nickname=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=email or '',
            phone=phone or '',
            nickname=nickname or '',
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username=username, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'nickname']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    major = models.CharField(max_length=100) #학과
    year = models.CharField(max_length=10) #학년
    preferred_gender = models.CharField(max_length=20) # 성별선호   
    dining_style = models.CharField(max_length=20) #식사 스타일
    eating_speed = models.CharField(max_length=20) #식사 속도
    meal_purpose = models.CharField(max_length=20) #밥약 목적
    dessert = models.CharField(max_length=20) # 디저트 여부
    preferred_menu = models.JSONField()  #선호메뉴(다중 선택으로)
    dietary_restrictions = models.JSONField()  #특이사항(다중 선택으로)

    def __str__(self):
        return f"{self.user.username}'s profile"