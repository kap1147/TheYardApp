from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
		path('add/', views.createJob, name='job_create'),
]
