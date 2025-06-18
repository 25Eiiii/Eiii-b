from django.urls import path
from .views import SignUpView, ProfileCreateView
from .views import SignUpView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileCreateView.as_view(), name='profile-create'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
