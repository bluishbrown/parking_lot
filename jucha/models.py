from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title = models.SlugField(max_length=4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exit_at = models.DateTimeField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __Str__(self):
        return f'[{self.title}]{self.author}'

    def get_absolute_url(self):
        # 원래는 pk
        return f'/jucha/{self.title}/'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    # created_at = models.DatetimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}/'
