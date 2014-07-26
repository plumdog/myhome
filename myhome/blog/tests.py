from test_base import MyHomeTest
from .models import BlogPost

class BlogTestCase(MyHomeTest):
    def setUp(self):
        BlogPost.objects.create(
            datetime='2014-01-01T12:00:00Z',
            title='livetitle',
            content='livecontent',
            live=True)
        BlogPost.objects.create(
            datetime='2014-01-01T12:00:00Z',
            title='hiddentitle',
            content='hiddencontent',
            live=False)

    def _test_404(self, url):
        g = self.client.get(url)
        self.assertEqual(g.status_code, 404)

    def test_view(self):
        self._test_get('/blog/', ins=['livetitle'], notins=['No Items', 'hiddentitle'])

    def test_view_one(self):
        self._test_get('/blog/post/1/', ins=['livetitle', 'livecontent'])

    def test_view_one_nonlive(self):
        self._test_404('/blog/post/2/')

    def test_view_miss(self):
        self._test_404('/blog/post/100/')
