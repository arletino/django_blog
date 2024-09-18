from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    '''Model of posts create post with title, slug, body'''

    class Status(models.TextChoices): # Subclass based on Enum
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey( 
                               User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts' # back relation to get posts by User
                               )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(
                              max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT
                              )


    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    objects = models.Manager() # manager by default
    published = PublishManager() # exactly used manager (конкретный прикладной менеджер)


    class Meta: # Metadata of model for change global setting of model
        ordering = ['-publish'] # preparing sorting by field 'publish' DESC before out
        indexes = [
            models.Index(fields=['-publish']), # Setup index for field publish for fast search(MYSQL is not supported DESC index will be add normal index)
        ]

    def __str__(self) -> str:
        return self.title
    