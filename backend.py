import os
import functools


from slugify import slugify
from dateutil.parser import parse as parse_datetime

from settings import POSTS_DIR


class BlogPost(object):
    title = ''
    subtitle = ''
    tags = []
    datetime = None
    content = ''

    @property
    def slug_tags(self):
        return [slugify(t) for t in self.tags]

    @property
    def slug(self):
        return slugify(self.title)

    def __eq__(self, other):
        return self.slug == other.slug

    def adj_post(self, next=True):
        # This is currently horrible
        all_posts = get_posts()
        current_post_index = all_posts.index(self)
        if next:
            if current_post_index < len(all_posts) - 1:
                return all_posts[current_post_index + 1]
            return None
        else:
            if current_post_index > 0:
                return all_posts[current_post_index - 1]
            return None

    def next_post(self):
        return self.adj_post(next=True)

    def prev_post(self):
        return self.adj_post(next=False)


def goto_line(gen, startswith):
    while True:
        line = next(gen)
        if line.startswith(startswith):
            return line

def get_simple_section(gen, startswith):
    line = goto_line(gen, startswith)
    rest = line[len(startswith):].strip()
    matched_lines = [rest]
    line = next(gen)
    while line.strip():
        matched_lines.append(line)
        line = next(gen)
    return matched_lines


def get_post(content):
    lines = (l for l in content.splitlines())

    title_lines = get_simple_section(lines, 'Title:')
    subtitle_lines = get_simple_section(lines, 'Subtitle:')
    tags_lines = get_simple_section(lines, 'Tags:')
    datetime_lines = get_simple_section(lines, 'Datetime:')

    line = goto_line(lines, 'Content:')
    rest = line[len('Content:'):].strip()
    content_lines = []
    if rest:
        content_lines.append(rest)
    while True:
        try:
            line = next(lines)
        except StopIteration:
            break
        else:
            content_lines.append(line)

    title = ' '.join(title_lines)
    subtitle = ' '.join(subtitle_lines)
    tags = [t.strip() for t in ','.join(tags_lines).split(',') if t.strip()]
    datetime = parse_datetime(' '.join(datetime_lines))
    content = '\n'.join(content_lines)

    post = BlogPost()
    post.title = title
    post.subtitle = subtitle
    post.tags = tags
    post.datetime = datetime
    post.content = content
    return post


@functools.lru_cache(maxsize=None)
def get_posts():
    posts_dir = POSTS_DIR
    posts = []
    for fpath in os.listdir(posts_dir):
        full_fpath = os.path.join(posts_dir, fpath)
        if (not fpath.startswith('.')) and full_fpath.endswith('.txt'):
            with open(full_fpath) as f:
                content = f.read()
                posts.append(get_post(content))
    return sorted(posts, key=lambda p: p.datetime)

def get_all_tags():
    tags = set()
    posts = get_posts()
    for p in posts:
        for t in p.tags:
            tags.add(t)
    return tags


def slug_tag_to_readable(slug_tag):
    mapping = {slugify(tag): tag for tag in get_all_tags()}
    return mapping.get(slug_tag, slug_tag)


def get_posts_for_tag(tag):
    slug_tag = slugify(tag)
    posts = get_posts()
    return [p for p in posts if slug_tag in p.slug_tags]


def get_post_for_slug(slug):
    posts = get_posts()
    return next(p for p in posts if p.slug == slug)
