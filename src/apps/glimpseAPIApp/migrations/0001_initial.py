# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-23 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=45)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('profile_pic_link', models.CharField(max_length=245)),
                ('header_pic_link', models.CharField(max_length=245)),
                ('email', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=245)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArtistEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_id', models.IntegerField()),
                ('event_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=False)),
                ('device_number', models.IntegerField()),
                ('serial_number', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField()),
                ('name', models.CharField(max_length=245)),
                ('address', models.CharField(max_length=245)),
                ('header_image', models.CharField(max_length=245)),
                ('start_date', models.CharField(max_length=245)),
                ('end_date', models.CharField(max_length=245)),
                ('start_time', models.CharField(max_length=245)),
                ('long', models.DecimalField(decimal_places=3, max_digits=8)),
                ('lat', models.DecimalField(decimal_places=3, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0)),
                ('starred', models.IntegerField(default=0)),
                ('featured', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=False)),
                ('device_id', models.IntegerField(default=False)),
                ('event_id', models.IntegerField(default=0)),
                ('media_type', models.CharField(max_length=10)),
                ('link', models.CharField(max_length=245)),
                ('raw_or_edited', models.CharField(max_length=45)),
                ('downloaded', models.IntegerField(default=False)),
                ('ranking', models.IntegerField(default=1)),
                ('date', models.CharField(max_length=245)),
                ('date_time', models.CharField(max_length=245)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('gif_link', models.CharField(max_length=245)),
                ('media_length', models.DecimalField(decimal_places=3, default=0.0, max_digits=8)),
                ('media_size', models.DecimalField(decimal_places=3, default=0.0, max_digits=8)),
                ('user_rating', models.IntegerField(default=0)),
                ('curator_rating', models.IntegerField(default=0)),
                ('bitrate', models.IntegerField(default=0)),
                ('total_bitrate', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MediaComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=False)),
                ('media_id', models.IntegerField(default=False)),
                ('comment', models.TextField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=False)),
                ('media_id', models.IntegerField(default=False)),
                ('comment', models.TextField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=45)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('profile_pic_link', models.CharField(max_length=245)),
                ('email', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=245)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=False)),
                ('device_used_id', models.IntegerField(default=False)),
                ('event_id', models.IntegerField(default=False)),
            ],
        ),
    ]
