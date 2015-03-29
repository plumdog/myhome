from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import BlogPost, BlogPostTag

def index(request):
    tag = request.GET.get('tag')
    
    if tag:
        try:
            tag_id = int(tag)
        except ValueError:
            try:
                tag_id = BlogPostTag.objects.get(name=tag).id
            except BlogPostTag.DoesNotExist:
                tag_id = None
        tag = get_object_or_404(BlogPostTag, pk=tag_id)
        blog_posts = BlogPost.objects.filter(blog_post_tags__id=tag_id)
        
    else:
        tag = None
        blog_posts = BlogPost.objects



    blog_posts = blog_posts.filter(live=True)
    context = {'blog_posts': blog_posts, 'tag': tag}
    return render(request, 'blog/index.html', context)

def post(request, post_id):
    blog_post = get_object_or_404(BlogPost, pk=post_id, live=True)
    context = {'bp': blog_post, 'prev': blog_post.prev_post(), 'next': blog_post.next_post()}
    return render(request, 'blog/blog_post.html', context)
