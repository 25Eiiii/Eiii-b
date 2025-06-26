# communities/urls.py
from django.urls import path
from communities import views

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<str:category>/', views.CommunityListView.as_view(), name='community-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comments/', views.CommentView.as_view(), name='comment-list-create'),
    path('<int:post_id>/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]
