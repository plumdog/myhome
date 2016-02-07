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


class Parser(object):

    TITLE = 'Title:'
    SUBTITLE = 'Subtitle:'
    TAGS = 'Tags:'
    DATETIME = 'Datetime:'
    CONTENT = 'Content:'

    TITLE_KEY = 'title'
    SUBTITLE_KEY = 'subtitle'
    TAGS_KEY = 'tags'
    DATETIME_KEY = 'datetime'
    CONTENT_KEY = 'content'

    sections = {
        TITLE_KEY: TITLE,
        SUBTITLE_KEY: SUBTITLE,
        TAGS_KEY: TAGS,
        DATETIME_KEY: DATETIME,
        CONTENT_KEY: CONTENT,
    }

    MULTILINE_SECTIONS = [
        CONTENT,
    ]

    def __init__(self, lines):
        self.lines = lines

        self.last_line_blank = True
        self.current_section = None

        self.output = {
            self.TITLE_KEY: [],
            self.SUBTITLE_KEY: [],
            self.TAGS_KEY: [],
            self.DATETIME_KEY: [],
            self.CONTENT_KEY: [],
        }

    def handle_line(self, line):
        if self.last_line_blank:

            if self.current_section not in self.MULTILINE_SECTIONS:
                self.current_section = None

            for section in self.sections.values():
                if line.startswith(section):
                    self.current_section = section
                    line = line[len(section):].strip()
                    break

        if self.current_section:
            self._append_line_to_current_section(line)
        

    def _get_output(self, section):
        mapping = {v: k for k, v in self.sections.items()}
        section_key = mapping[section]
        return self.output[section_key]

    def _append_line_to_current_section(self, line):
        output = self._get_output(self.current_section)
        output.append(line)

    def get_post(self):
        for line in self.lines:
            self.handle_line(line)

        title = ' '.join(self.output[self.TITLE_KEY])
        subtitle = ' '.join(self.output[self.SUBTITLE_KEY])
        tags_lines = self.output[self.TAGS_KEY]
        tags = [t.strip() for t in ','.join(tags_lines).split(',') if t.strip()]
        datetime = parse_datetime(' '.join(self.output[self.DATETIME_KEY]))
        content = '\n'.join(self.output[self.CONTENT_KEY])

        post = BlogPost()
        post.title = title
        post.subtitle = subtitle
        post.tags = tags
        post.datetime = datetime
        post.content = content
        return post


def get_post(lines):
    return Parser(lines).get_post()


@functools.lru_cache(maxsize=None)
def get_posts():
    posts_dir = POSTS_DIR
    posts = []
    for fpath in os.listdir(posts_dir):
        full_fpath = os.path.join(posts_dir, fpath)
        if (not fpath.startswith('.')) and full_fpath.endswith('.txt'):
            with open(full_fpath) as f:
                lines = f.read().splitlines()
                posts.append(get_post(lines))
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
