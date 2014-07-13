from django.test import SimpleTestCase, Client
from .models import BlogPost

class BlogTestCase(SimpleTestCase):
    def setUp(self):
        BlogPost.objects.create(
            datetime='2014-01-01 12:00:00',
            title='title',
            content='content',
            live=True)

    def _test_get(self, url, *, ins=[], not_ins=[]):
        g = self.client.get(url)
        for in_ in ins:
            self.assertContains(g, in_)
        for nin_ in not_ins:
            self.assertNotContains(g, nin_)

    def _test_404(self, url):
        g = self.client.get(url)
        self.assertEqual(g.status_code, 404)

    def test_view(self):
        self._test_get('/blog/', ins=['title', 'content'], not_ins=['No Items'])

    def test_view_one(self):
        self._test_get('/blog/post/1/', ins=['title', 'content'])

    def test_view_miss(self):
        self._test_404('/blog/post/100/')
