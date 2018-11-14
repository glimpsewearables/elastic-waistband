# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-14 04:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('name', models.CharField(max_length=245)),
                ('address', models.CharField(max_length=245)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
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
                ('media_type', models.CharField(max_length=10)),
                ('link', models.CharField(max_length=245)),
                ('raw_or_edited', models.CharField(max_length=45)),
                ('downloaded', models.IntegerField(default=False)),
                ('ranking', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('DeviceId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content', to='glimpseAPIApp.Device')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
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
                ('event_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_attending', to='glimpseAPIApp.Event')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_at_events', to='glimpseAPIApp.User')),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='UserId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='glimpseAPIApp.User'),
        ),
        migrations.AddField(
            model_name='media',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media_at_event', to='glimpseAPIApp.Event'),
        ),
        migrations.AddField(
            model_name='device',
            name='UserId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='glimpseAPIApp.User'),
        ),
    ]
