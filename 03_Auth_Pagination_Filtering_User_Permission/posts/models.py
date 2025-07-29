from django.db import models

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_publish_post", "Can Publish Post"),
        ]

    def __str__(self) -> str:
        return self.title
