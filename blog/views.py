from typing import List

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from rest_framework import generics, permissions, viewsets

from .models import Comment, Post
from .serializers import (CommentSerializer, PostSerializer,
                          PostUpdateSerializer)


# APIs Developed with Django Rest Framework
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


# APIs Developed with Django Ninja
api = NinjaAPI()

class PostOutSchema(Schema):
    id : int
    title: str
    content: str

class PostInSchema(Schema):
    title: str = None
    content: str = None

class CommentSchema(Schema):
    post_id: int
    text: str
    email: str

@api.get('/posts', response=List[PostOutSchema], tags=['posts'], description="List all posts")
@login_required()
def list_posts(request):
    queryset = Post.objects.all()
    return queryset

@api.get("/comments", response=List[CommentSchema], tags=['comments'], description="List all comments")
@login_required
def list_comments(request):
    queryset = Comment.objects.all()
    return queryset

@api.post("/posts", tags=['posts'])
@login_required
def create_post(request, payload: PostInSchema):
    """
    To create a post please provide:
    - **title** 
    - **content**
    """
    post = Post.objects.create(**payload.dict())
    return {"id": post.id}

@api.post("/comments", tags=['comments'])
@login_required
def create_comment(request, payload: CommentSchema):
    """
    To create a comment please provide:
    - **post_id**
    - **text**
    - **email**
    """
    comment = Comment.objects.create(**payload.dict())
    return {"id": comment.id}

@api.put("/posts/{int:post_id}", tags=['posts'])
@login_required
def update_post(request, post_id: int, payload: PostInSchema):
    """
    To update a post please provide:
    - **post_id**
    - **title**
    - **content**
    """
    post = get_object_or_404(Post, id=post_id)
    for attr, value in payload.dict().items():
        if value is not None:  
            setattr(post, attr, value)
    post.save()
    return {"success": True}

@api.get("/posts/{int:post_id}", response=PostOutSchema, tags=['posts'], description="Get a post")
@login_required
def get_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post

@api.delete("/posts/{int:post_id}", tags=['posts'], description="Delete a post")
@login_required
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"success": True}