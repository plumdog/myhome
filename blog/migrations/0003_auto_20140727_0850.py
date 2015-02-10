# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_live'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-datetime']},
        ),
        migrations.AlterModelOptions(
            name='blogposttag',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='subtitle',
            field=models.CharField(null=True, max_length=255),
            preserve_default=True,
        ),
    ]
