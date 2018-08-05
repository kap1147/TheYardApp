from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.urls import reverse

from random import randint

from locations.models import Location
from .utils import upload_image_path


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Image(models.Model):
    title = models.CharField(max_length=60)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_image_path)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title + 'image'

    def save(self, *args, **kwargs):
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from sys import getsizeof

        image = self.image
        if not image:
            image = None
            return image

        size = (850,850)

        im = Image.open(image)
        output = BytesIO()
        im.resize(size, Image.ANTIALIAS)
        try:
            im.save(output, format='JPEG', quality=100)
            output.seek(0)
            image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %image.name.split('.')[0], 'image/jpeg', getsizeof(output), None)
        except:
            im.save(output, format='PNG', quality=100)
            output.seek(0)
            image = InMemoryUploadedFile(output,'ImageField', "%s.png" %image.name.split('.')[0], 'image/png', getsizeof(output), None)
        super().save(*args, **kwargs)
