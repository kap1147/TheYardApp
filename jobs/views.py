from django.shortcuts import render
from django.http import HttpResponse

from .models import Job

from posts.models import Post

import json

def createJob(request):
    if request.method == 'POST':
        # retrieve vars from post
        post_id = request.POST.get('post_id')
        bid = request.POST.get('bid')
        
        # retrieve relevant post
        post = Post.objects.get(pk=post_id)

        # check if contractor has already made an offer
        if Job.objects.filter(post=post, contractor=request.user).exists():
            # redirect to job
            return HttpResponse(
                    json.dumps({'status':'Bid already exists.'}),
                    content_type='application/json'
            )
        # create new job
        job = Job(contractor=request.user, post=post)
        job.save()
        return HttpResponse(
            json.dumps({'status':'Create a bid.','job_id':job.id}),
            content_type='application/json'
        )
