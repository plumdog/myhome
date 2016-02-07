import os


class Urls(object):
    patterns = {}

    def add(self, name, url, path=None, format_func=None):
        self.patterns[name] = (name, url, path, format_func)

    def get_url(self, name, **kwargs):
        pattern = self.patterns[name]
        name, url, path, format_func = pattern

        if format_func:
            format_kwargs = format_func(**kwargs)
            kwargs.update(format_kwargs)

        return url.format(**kwargs)

    def _get_path_from_url(self, url):
        if not url.endswith('.html'):
            return os.path.join(url, 'index.html')
        else:
            return url

    def get_path(self, name, **kwargs):
        pattern = self.patterns[name]
        name, url, path, format_func = pattern
        if not path:
            path = self._get_path_from_url(url)

        if format_func:
            format_kwargs = format_func(**kwargs)
            kwargs.update(format_kwargs)
        return path.format(**kwargs)
