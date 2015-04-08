from . import settings

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^robots\.txt$', include('robots.urls')),
)

from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogPostSitemap, BlogPostTagSitemap, HomeSitemap
sitemaps = {
    'blog_posts': BlogPostSitemap,
    'blog_tags': BlogPostTagSitemap,
    'home': HomeSitemap}
urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'))

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))
