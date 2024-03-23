from django.core.management.base import BaseCommand
from blog.factories import PostFactory, CommentFactory

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Create 10 posts and 5 comments for each post
        for _ in range(10):
            post = PostFactory()
            for _ in range(5):
                CommentFactory(post=post)
        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))
