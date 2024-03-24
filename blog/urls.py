from django.urls import path
from .views import PostListAPIView, CommentListAPIView, PostRetrieveAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
]