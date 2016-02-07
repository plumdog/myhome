from urls_base import Urls

from slugify import slugify
from settings import ASSET_TAG


urls = Urls()
urls.add('index', '/')
urls.add('projects', '/projects/')
urls.add('blog', '/blog/')
urls.add('post', '/post/{slug}.html',
         format_func=lambda **kwargs: dict(slug=slugify(kwargs['post'].title)))
urls.add('tag', '/post/tag/{slug}.html',
         format_func=lambda **kwargs: dict(slug=slugify(kwargs['tag'])))
urls.add('static', '/static/{path}?_/{asset_tag}',
         format_func=lambda **kwargs: dict(asset_tag=ASSET_TAG))


get_url = urls.get_url
get_path = urls.get_path
