from django.db import models

class BlogPostTag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    datetime = models.DateTimeField()
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True)
    content = models.TextField()
    live = models.BooleanField(default=False)

    blog_post_tags = models.ManyToManyField(BlogPostTag, blank=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        if self.live:
            return self.title
        else:
            return self.title + ' - (not live)'

    def __repr__(self):
        return '<BlogPost id=%d, datetime=%s, title=%s>' % (self.id, self.datetime, self.title)

    def prev_post(self):
        prev_datetime = BlogPost.objects.filter(live=True, datetime__lt=self.datetime).aggregate(models.Max('datetime'))['datetime__max']
        try:
            return BlogPost.objects.filter(datetime=prev_datetime)[0]
        except IndexError:
            return None

    def next_post(self):
        next_datetime = BlogPost.objects.filter(live=True, datetime__gt=self.datetime).aggregate(models.Min('datetime'))['datetime__min']
        try:
            return BlogPost.objects.filter(datetime=next_datetime)[0]
        except IndexError:
            return None
