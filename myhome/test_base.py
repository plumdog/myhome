from django.test import SimpleTestCase, Client


class MyHomeTest(SimpleTestCase):
    def _test_get(self, url, *, ins=(), notins=()):
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

        content = r.content.decode('utf-8')
        for in_ in ins:
            self.assertIn(in_, content)
        for notin_ in notins:
            self.assertNotIn(notin_, content)
