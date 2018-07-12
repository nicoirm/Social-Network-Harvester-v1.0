# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-07-12 16:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Youtube', '0001_initial'),
        ('AspiraUser', '0002_auto_20180712_1612'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ytChannelsToHarvest',
            field=models.ManyToManyField(blank=True, related_name='harvested_by', to='Youtube.YTChannel'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ytPlaylistsToHarvest',
            field=models.ManyToManyField(blank=True, related_name='harvested_by', to='Youtube.YTPlaylist'),
        ),
        migrations.AddField(
            model_name='tablerowsselection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tableRowsSelections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='selectionquery',
            name='selection_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to='AspiraUser.TableRowsSelection'),
        ),
    ]