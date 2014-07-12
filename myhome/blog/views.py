from django.shortcuts import render
from django.http import HttpResponse

from .models import BlogPost

def index(request):
    blog_posts = BlogPost.objects.order_by('datetime')
    context = {'blog_posts': blog_posts}
    return render(request, 'blog/index.djhtml', context)
