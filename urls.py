import os

from slugify import slugify
from settings import ASSET_TAG


def get_path(name, **kwargs):
    url = get_url(name, **kwargs)
    if not url.endswith('.html'):
        return os.path.join(url, 'index.html')
    return url


def get_url(name, **kwargs):
    if name == 'index':
        return '/'
    if name == 'projects':
        return '/projects/'
    if name == 'blog':
        return '/blog/'
    if name == 'post':
        post = kwargs['post']
        return '/post/{}.html'.format(slugify(post.title))
    if name == 'tag':
        tag = kwargs['tag']
        return '/post/tag/{}.html'.format(slugify(tag))
    if name == 'static':
        path = kwargs['path']
        return '/static/{path}?_/{asset_tag}'.format(
            path=path, asset_tag=ASSET_TAG)
