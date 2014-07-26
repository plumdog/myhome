from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import BlogPost, BlogPostTag

def index(request):
    tag_id = request.GET.get('tag')
    
    if tag_id:
        tag = get_object_or_404(BlogPostTag, pk=tag_id)
        blog_posts = BlogPost.objects.filter(blog_post_tags__id=tag_id)
        
    else:
        tag = None
        blog_posts = BlogPost.objects

    blog_posts = blog_posts.filter(live=True).order_by('-datetime')
    context = {'blog_posts': blog_posts, 'tag': tag}
    return render(request, 'blog/index.html', context)

def post(request, post_id):
    blog_post = get_object_or_404(BlogPost, pk=post_id, live=True)
    context = {'bp': blog_post}
    return render(request, 'blog/blog_post.html', context)
