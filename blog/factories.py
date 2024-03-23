import factory
from .models import Post, Comment

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=6)
    content = factory.Faker('paragraph')

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    text = factory.Faker('paragraph')
    email = factory.Faker('email')
