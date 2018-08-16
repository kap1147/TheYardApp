from django.shortcuts import render, redirect
from django.views.generic import (DetailView, TemplateView, 
                                  UpdateView, DeleteView, 
                                  CreateView, ListView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

#from allauth.account.models import Profile
from locations.models import Location
from .models import Post, Image
from .forms import PostCreateForm, BaseImageFormset, ImageForm
from django.forms import modelformset_factory, formset_factory
from django.http import HttpResponse
import json
from django.core import serializers


@login_required(login_url='/accounts/login/')
def postCreateView(request):
    ImageFormset = formset_factory(form=ImageForm, formset=BaseImageFormset, extra=3)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
<<<<<<< HEAD
=======
            i = request.POST['Post']
>>>>>>> bd847206117a6bb4430d257bbd7ab9aa2be634e6
            post.owner = request.user
            post.save()
            i = 1
            for instance in formset:
                try:
                    photo = Image(post=post, image=instance.cleaned_data['image'], title=str(i))
                    photo.save()
                    i = i + 1
                except Exception as e:
                     break
            return redirect('posts:post_list')
    else:
        form = PostCreateForm()
        formset = ImageFormset(Image.objects.none())
        formset = ImageFormset()
        context = {
     	        'form': form,
                'formset': formset,
        }
        return render(request, 'posts/post_form.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'price']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.location = Location.objects.get(pk=self.request.POST.get('location'))
        messages.success(self.request, "Post added.")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'price']
    
    def get_object(self, *args, **kwargs):
        instance = get_object_or_404(Post, owner=self.request.user, pk=self.kwargs['pk'])
        return instance

    def form_valid(self, form):
        messages.success(self.request, "Post updated.")
        return super().form_valid(form)

class PostDetailView(DetailView):
    template_name = "posts/post.html"
    
    def get_object(self, *args, **kwargs):
        try:
            instance = get_object_or_404(Post, pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            raise Http404('Post not found or has been removed.')
        except Post.MultipleObjectsReturned:
            qs = Post.objects.filter(pk=self.kwargs['pk'])
            instance = qs.first()
        except:
           raise Http404("Please contact support.")
        return instance

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:post_list')

@login_required(login_url='/accounts/login/')
def postUserListView(request, slug):
    template = "posts/post_list.html"
    qs = Post.objects.filter(owner=slug)
    return render(request, template, {'object_list': qs})


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(active=True)

def ajaxSetPostLocation(request):
    if request.method == 'POST':
        if request.is_ajax():
<<<<<<< HEAD
            l = []
            city = request.POST.get('city', None)
            l.append(city)
            state = request.POST.get('state', None)
            l.append(state)
            country = request.POST.get('country', None)
            l.append(country)
            lng = request.POST.get('lng', None)
            l.append(lng)
            lat = request.POST.get('lat', None)
            l.append(lat)
=======
            city = request.POST.get('city', None)
            state = request.POST.get('state', None)
            country = request.POST.get('country', None)
            lng = request.POST.get('lng', None)
            lat = request.POST.get('lat', None)
>>>>>>> bd847206117a6bb4430d257bbd7ab9aa2be634e6
            pk = request.POST.get('id', None)

            response_data = {}

            # create of get location
            location, created = Location.objects.get_or_create(city=city, state=state, country=country)

            if created:
                location.latitude = lat
                location.longitude = lng
                location.save()

            if pk != None:
                post = Post.objects.get(pk=pk)
<<<<<<< HEAD
                if not all(v is None for v in l):
                    post.location = location
                    post.save()
=======
                post.location = location
                post.save()
>>>>>>> bd847206117a6bb4430d257bbd7ab9aa2be634e6
                url = '/posts/' + str(post.id) + '/'
                response_data['status'] = 'Update Post'
                response_data['url'] = url
                return HttpResponse(
                        json.dumps(response_data),
                        content_type = 'application/json'
                )

            response_data['status'] = 'Create Post'
            response_data['location'] = location.id
            return HttpResponse(
                    json.dumps(response_data),
                    content_type='application/json'
            )


def ajaxCreatePost(request):
    if request.method == 'POST':
        location = request.POST.get('loc')
        success = 'success!'

        form = PostCreateForm(request.POST)
<<<<<<< HEAD
        ImageFormset = formset_factory(form=ImageForm, formset=BaseImageFormset, extra=3)
        if form.is_valid():
            _location = Location.objects.get(pk=location)
            post = form.save(commit=False)
            post.owner = request.user
            post.location = _location
            post.save()

            i = 1
            formset = ImageFormset(request.POST, request.FILES)
            for instance in formset:
                try:
                    photo = Image(post=post, image=instance.cleaned_data['image'], title=str(i))
                    photo.save()
                    i = i + 1
                except Exception as e:
                     break

=======
        if form.is_valid():
            post_location = Location.objects.get(pk=location)
            post = form.save(commit=False)
            post.owner = request.user
            post.location = post_location
            post.save()
>>>>>>> bd847206117a6bb4430d257bbd7ab9aa2be634e6
            url = '/posts/' + str(post.id) + '/'
            return HttpResponse(
                    json.dumps({'url': url}),
                    content_type='application/json'
            )

        return HttpResponse(
<<<<<<< HEAD
                json.dumps({'status': 'invalid'}),
                content_type='application/json'
=======
             json.dumps(request_data),
             content_type='application/json'
>>>>>>> bd847206117a6bb4430d257bbd7ab9aa2be634e6
        )

