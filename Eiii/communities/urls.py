# communities/urls.py
from django.urls import path
from communities import views

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<str:category>/', views.CommunityListView.as_view(), name='community-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:post_id>/like/', views.LikeView.as_view(), name='post-like'),
    path('post/<int:post_id>/scrap/', views.ScrapView.as_view(), name='post-scrap'),
    path('post/liked/', views.LikedPostsView.as_view(), name='liked-posts'),
    path('post/scrapped/', views.ScrappedPostsView.as_view(), name='scrapped-posts'),
    path('<int:post_id>/comments/', views.CommentView.as_view(), name='comment-list-create'),
    path('<int:post_id>/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('comments/my/', views.MyCommentListView.as_view(), name='my_comments'),
]
