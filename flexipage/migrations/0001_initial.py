# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexiContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlexiPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('template_name', models.CharField(max_length=100, choices=[('start.html', 'start')])),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Flexi Page',
            },
            bases=('pages.page',),
        ),
        migrations.AddField(
            model_name='flexicontent',
            name='page',
            field=models.ForeignKey(related_name='flexi_content', to='flexipage.FlexiPage'),
        ),
    ]
