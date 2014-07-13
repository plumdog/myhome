from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns(
    '',
    url(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
    url(r'^$', views.index, name='index'))
