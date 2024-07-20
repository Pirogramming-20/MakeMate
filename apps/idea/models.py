from django.db import models
from apps.group.models import Idea
from apps.common.models import User

# Create your models here.
class Comment(models.Model):
    idea = models.ForeignKey(Idea, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content