from django.contrib import admin
from .models import CustomUser, Profile

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'nickname', 'is_staff', 'is_superuser')
    search_fields = ('username', 'nickname', 'email')

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'major', 'year', 'preferred_gender')
    search_fields = ('user__username', 'major')