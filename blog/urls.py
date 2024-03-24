from django.urls import path
from .views import PostListAPIView, CommentListAPIView, PostRetrieveAPIView, PostCreateAPIView, CommentCreateAPIView, PostUpdateAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('posts/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),
]