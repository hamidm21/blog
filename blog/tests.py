from django.test import TestCase
from .factories import CommentFactory, PostFactory
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer

class PostModelTestCase(TestCase):
    def test_post_creation(self):
        post = PostFactory()
        self.assertIsInstance(post, Post)

class CommentModelTestCase(TestCase):
    def test_comment_creation(self):
        comment = CommentFactory()
        self.assertIsInstance(comment, Comment)

class SerializerTestCase(TestCase):
    def setUp(self):
        self.post_data = {'title': 'Test Post', 'content': 'This is a test post.'}
        self.comment_data = {'post': None, 'text': 'Test comment', 'email': 'test@example.com'}
        self.post = Post.objects.create(title=self.post_data['title'], content=self.post_data['content'])
        self.comment_data['post'] = self.post

    def test_post_serializer(self):
        serializer = PostSerializer(instance=self.post)
        self.assertEqual(serializer.data['title'], self.post_data['title'])
        self.assertEqual(serializer.data['content'], self.post_data['content'])

    def test_comment_serializer(self):
        comment = Comment.objects.create(post=self.post, text=self.comment_data['text'], email=self.comment_data['email'])
        serializer = CommentSerializer(instance=comment)
        self.assertEqual(serializer.data['post'], self.post.id)
        self.assertEqual(serializer.data['text'], self.comment_data['text'])
        self.assertEqual(serializer.data['email'], self.comment_data['email'])

    def test_post_update_serializer(self):
        serializer = PostSerializer(instance=self.post, data=self.post_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(serializer.data['title'], self.post_data['title'])
        self.assertEqual(serializer.data['content'], self.post_data['content'])

