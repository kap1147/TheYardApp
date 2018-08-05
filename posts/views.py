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

@login_required(login_url='/accounts/login/')
def postCreateView(request):
    ImageFormset = formset_factory(form=ImageForm, formset=BaseImageFormset, extra=3)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.user = request.user
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
    city = request.POST.get('city', None)
    state = request.POST.get('state', None)
    country = request.POST.get('country', None)
    lng = request.POST.get('longitude', None)
    lat = request.POST.get('latitude', None)
    pk_ = request.POST.get('id', None)

    location, created = Location.objects.get_or_create(city=city, state=state, country=country)
    success = 'Location found'

    if created:
        location.latitude = lat
        location.longitude = lng
        location.save()
        success = 'Location added.'
    if pk_:
        post = get_object_or_404(Post, owner=request.user, pk=pk_)
        post.location = location
        post.save()

        data = {
            'success': success
        }
        return redirect("post")
