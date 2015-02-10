from test_base import MyHomeTest


class HomeTest(MyHomeTest):
    def test_index_page(self):
        self._test_get('/', ins=['Andrew Plummer'])
