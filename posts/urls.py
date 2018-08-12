from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDetailView, PostDeleteView, ajaxSetPostLocation, PostListView, postUserListView, postCreateView, ajaxCreatePost

app_name="posts"

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('add/', postCreateView, name='post_add'),
#    path('add/', PostCreateView.as_view(), name='post_add'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/', postUserListView, name='post_user_list'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('ajax/location', ajaxSetPostLocation, name='ajax_location'),
    path('ajax/post', ajaxCreatePost, name='ajax_post'),
]
