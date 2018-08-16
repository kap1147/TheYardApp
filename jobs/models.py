from django.db import models
from django.contrib.auth.models import User

from posts.models import Post

class Job(models.Model):
    contractor	= models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    post	= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='jobs')
    active	= models.BooleanField(default=True)
    timestamp	= models.DateTimeField(auto_now=True)
