from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Like(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    # updated_at = models.DateTimeField(auto_now=True)
    # content = models.TextField()

    class Meta:
        ordering = ['created_at']
        unique_together = ['owner', 'post']

    def __str__(self):
        return self.content

lucka 5  7522