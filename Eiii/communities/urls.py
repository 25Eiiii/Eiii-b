# communities/urls.py
from django.urls import path
from communities import views

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<str:category>/', views.CommunityListView.as_view(), name='community-list'),
    # path('community/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]
