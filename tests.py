from datetime import datetime
from dateutil.tz import tzutc

from backend import get_post


def test_backend_parsing():
    content = '''Title: Example title

Subtitle: Example subtitle

Tags: tag1, tag2

Datetime: 2016-02-07 15:25:30+00:00

Live: True

Content:

Content here
'''
    post = get_post(content.splitlines())
    assert post.title == 'Example title'
    assert post.subtitle == 'Example subtitle'
    assert post.tags == ['tag1', 'tag2']
    assert post.datetime == datetime(2016, 2, 7, 15, 25, 30, tzinfo=tzutc())


def test_backend_parsing_no_tags():
    content = '''Title: Example title

Subtitle: Example subtitle

Datetime: 2016-02-07 15:25:30+00:00

Content:

Content here
'''
    post = get_post(content.splitlines())
    assert post.title == 'Example title'
    assert post.subtitle == 'Example subtitle'
    assert not post.tags
    assert post.datetime == datetime(2016, 2, 7, 15, 25, 30, tzinfo=tzutc())
    assert post.content.strip() == 'Content here'


def test_backend_parsing_multiline_content():
    content = '''Title: Example title

Subtitle: Example subtitle

Datetime: 2016-02-07 15:25:30+00:00

Content:

Content here

more here
'''
    post = get_post(content.splitlines())
    assert post.title == 'Example title'
    assert post.subtitle == 'Example subtitle'
    assert not post.tags
    assert post.datetime == datetime(2016, 2, 7, 15, 25, 30, tzinfo=tzutc())
    assert post.content.strip() == 'Content here\n\nmore here'
