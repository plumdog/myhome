from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import BlogPost

def index(request):
    blog_posts = BlogPost.objects.order_by('-datetime')
    context = {'blog_posts': blog_posts}
    return render(request, 'blog/index.djhtml', context)

def post(request, post_id):
    blog_post = get_object_or_404(BlogPost, pk=post_id)
    context = {'bp': blog_post}
    return render(request, 'blog/blog_post.djhtml', context)
