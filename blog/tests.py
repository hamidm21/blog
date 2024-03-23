from django.test import TestCase
from .factories import CommentFactory, PostFactory
from .models import Comment, Post

# Create your tests here.

class PostModelTestCase(TestCase):
    def test_post_creation(self):
        post = PostFactory()
        self.assertIsInstance(post, Post)

class CommentModelTestCase(TestCase):
    def test_comment_creation(self):
        comment = CommentFactory()
        self.assertIsInstance(comment, Comment)
