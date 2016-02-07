import os
import shutil

# TODO: robots? Site maps? Don't forget css, fonts etc

from jinja2 import Environment, FileSystemLoader
from markdown import markdown as base_markdown

# from .project_euler_count import count as pec_count
from backend import (
    get_all_tags,
    get_posts_for_tag,
    get_posts,
    get_post_for_slug,
    slug_tag_to_readable,
)

from settings import BASE_DIR, HTML_DIR, ASSET_TAG
from urls import get_url, get_path


def markdown(text):
    return base_markdown(
        text,
        extensions=['markdown.extensions.codehilite',
                    'markdown.extensions.fenced_code'])


def get_all_pages():
    filters = {
        'markdown': markdown,
    }

    extra_globals = {
        'get_url': get_url,
    }

    env = Environment(loader=FileSystemLoader('templates'))

    env.filters.update(filters)
    env.globals.update(extra_globals)

    pages = {
        get_path('index'): render_template(env, 'home/index.html'),
        get_path('projects'): render_template(env, 'home/projects.html'),
        get_path('blog'): render_blog_index(env),
        # TODO: project euler count?
    }

    for post in get_posts():
        pages[get_path('post', post=post)] = render_post(env, post)

    for tag in get_all_tags():
        pages[get_path('tag', tag=tag)] = render_blog_index(env, tag=tag)

    return pages


def render_template(env, template_name, context=None):
    ctx = {
        'ASSET_TAG': ASSET_TAG
    }
    ctx.update(context or {})

    return env.get_template(template_name).render(**ctx)



def render_blog_index(env, tag=None):
    if tag:
        blog_posts = get_posts_for_tag(tag)
        tag = slug_tag_to_readable(tag)
    else:
        blog_posts = reversed(get_posts())
    context = {'blog_posts': blog_posts, 'tag': tag}
    return render_template(env, 'blog/index.html', context)
    

def render_post(env, blog_post):
    context = {'bp': blog_post, 'prev': blog_post.prev_post(), 'next': blog_post.next_post()}
    template = env.get_template('blog/blog_post.html')
    return template.render(**context)


def write_page(path, page):
    if not os.path.isdir(HTML_DIR):
        os.mkdir(HTML_DIR)

    path = path.lstrip('/')

    dir_path, fname = os.path.split(path)
    full_dir_path = os.path.join(HTML_DIR, dir_path)
    if not os.path.isdir(full_dir_path):
        os.makedirs(full_dir_path)
    with open(os.path.join(full_dir_path, fname), 'w') as f:
        f.write(page)


def main():
    for path, page in get_all_pages().items():
        write_page(path, page)
    # Static files
    shutil.copytree(os.path.join(BASE_DIR, 'static'),
                    os.path.join(HTML_DIR, 'static'))


if __name__ == '__main__':
    main()
