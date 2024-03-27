from django.test import TestCase
from .factories import CommentFactory, PostFactory
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer, PostUpdateSerializer

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

class PostViewTestCase(TestCase):
    def setUp(self):
        self.post_data = {"title": "Test Post", "content": "This is a test post."}
        self.post = Post.objects.create(title=self.post_data['title'], content=self.post_data['content'])
    
    def test_post_list(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.post_data['title'])
        self.assertEqual(response.data[0]['content'], self.post_data['content'])
    
    def test_post_detail(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.post_data['title'])
        self.assertEqual(response.data['content'], self.post_data['content'])

    def test_post_create(self):
        response = self.client.post('/api/posts/create/', data=self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], self.post_data['title'])
        self.assertEqual(response.data['content'], self.post_data['content'])

    def test_post_update(self):
        serializer = PostUpdateSerializer(instance=self.post, data=self.post_data)
        self.assertTrue(serializer.is_valid())
        response = self.client.put(f'/api/posts/{self.post.id}/update/', data=self.post_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

class CommentViewTestCase(TestCase):
    def setUp(self):
        self.post_data = {"title": "Test Post", "content": "This is a test post."}
        self.post = Post.objects.create(title=self.post_data['title'], content=self.post_data['content'])
        self.comment_data = {"post": self.post.id, "text": "Test comment", "email": "test@example.com"}
        self.comment = Comment.objects.create(post=self.post, text=self.comment_data['text'], email=self.comment_data['email'])
    
    def test_comment_list(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['post'], self.post.id)
        self.assertEqual(response.data[0]['text'], self.comment_data['text'])
        self.assertEqual(response.data[0]['email'], self.comment_data['email'])
    
    def test_comment_create(self):
        response = self.client.post('/api/comments/create/', data=self.comment_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['post'], self.post.id)
        self.assertEqual(response.data['text'], self.comment_data['text'])
        self.assertEqual(response.data['email'], self.comment_data['email']) 

class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.post_data = {"title": "Test Post", "content": "This is a test post."}
        self.post = Post.objects.create(title=self.post_data['title'], content=self.post_data['content'])
    
    def test_post_list(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.post_data['title'])
        self.assertEqual(response.data[0]['content'], self.post_data['content'])

    def test_post_detail(self):
        response = self.client.get(f'/api/articles/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.post_data['title'])
        self.assertEqual(response.data['content'], self.post_data['content'])

    def test_post_create(self):
        response = self.client.post('/api/articles/', data=self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], self.post_data['title'])
        self.assertEqual(response.data['content'], self.post_data['content'])
    
    def test_post_update(self):
        serializer = PostUpdateSerializer(instance=self.post, data=self.post_data)
        self.assertTrue(serializer.is_valid())
        response = self.client.put(f'/api/articles/{self.post.id}/', data=self.post_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)



        
        
    