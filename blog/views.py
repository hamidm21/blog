from rest_framework import generics, viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostUpdateSerializer
from ninja import NinjaAPI, Schema
from typing import List
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404


# APIs Developed with Django Rest Framework

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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
def list_posts(request):
    queryset = Post.objects.all()
    return queryset

@api.get("/comments", response=List[CommentSchema], tags=['comments'], description="List all comments")
def list_comments(request):
    queryset = Comment.objects.all()
    return queryset

@api.post("/posts", tags=['posts'])
def create_post(request, payload: PostInSchema):
    """
    To create a post please provide:
    - **title** 
    - **content**
    """
    post = Post.objects.create(**payload.dict())
    return {"id": post.id}

@api.post("/comments", tags=['comments'])
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
def get_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post

@api.delete("/posts/{int:post_id}", tags=['posts'], description="Delete a post")
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"success": True}