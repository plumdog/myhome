from django.db import models

class BlogPostTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    datetime = models.DateTimeField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    live = models.BooleanField(default=False)

    blog_post_tags = models.ManyToManyField(BlogPostTag, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.datetime)

    def __repr__(self):
        return '<BlogPost id=%d, datetime=%s, title=%s>' % (self.id, self.datetime, self.title)
