from django.db import models

class BlogPost(models.Model):
    datetime = models.DateTimeField()
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return 'Posted at: %s, title: %s' % (str(self.datetime), self.title)

    def __repr__(self):
        return '<BlogPost id=%d, datetime=%s, title=%s>' % (self.id, self.datetime, self.title)
