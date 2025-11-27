from django.urls import path
from .views import SignUpView, ProfileCreateView, ProfileByUserIdView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, MatchView, ProfileDetailView, MyProfileView, MyProfilePreviewView, ProfilePreviewView 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/me/', MyProfileView.as_view(), name='my-profile'),
    path('profile/me/preview/', MyProfilePreviewView.as_view(), name='my-profile-preview'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('match/', MatchView.as_view(), name='match'),
    path('profile/<int:pk>/preview/', ProfilePreviewView.as_view(), name='profile-preview'),  # 다른 사람 미리보기
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),            # 다른 사람 상세
    path('profile/user/<int:user_id>/', ProfileByUserIdView.as_view(), name='profile-by-user'),
]
