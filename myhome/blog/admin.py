from django.contrib import admin
from blog.models import BlogPost, BlogPostTag

admin.site.register(BlogPost)
admin.site.register(BlogPostTag)
