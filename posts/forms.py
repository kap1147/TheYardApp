from django import forms
from .models import Post, Image
from django.forms import BaseFormSet

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content', 'price']

class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Image
        fields = ('image',)

        def clean_image(self, *args, **kwargs):
            from PIL import Image
            from io import BytesIO
            from django.core.files.uploadedfile import InMemoryUploadedFile
            from sys import getsizeof

            image = form.cleaned_data["image"]
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

            form.cleaned_data['image'] = image
            form.instance.image = image
            return image

class BaseImageFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        super().clean()
        for form in self.forms:
            from PIL import Image
            from io import BytesIO
            from django.core.files.uploadedfile import InMemoryUploadedFile
            from sys import getsizeof

            try:
                image = form.cleaned_data["image"]
            except:
                break
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

            form.cleaned_data['image']= image
            form.instance.image = image
