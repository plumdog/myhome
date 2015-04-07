from urllib.parse import urlencode

from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from blog.models import BlogPost, BlogPostTag


class BlogPostSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(live=True).all()

    def lastmod(self, obj):
        return obj.datetime

    def location(self, obj):
        return reverse('blog:post', args=(obj.id,))


class BlogPostTagSitemap(Sitemap):
    priority = 0.3

    def items(self):
        return BlogPostTag.objects.all()

    def location(self, obj):
        return reverse('blog:index') + '?' + urlencode({'tag': obj.name})


class HomeSitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home:index', 'home:projects', 'blog:index']

    def location(self, obj):
        return reverse(obj)
