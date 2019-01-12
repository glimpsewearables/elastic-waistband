from __future__ import unicode_literals
from django.db import models
import sys, os, socket, requests
import re, bcrypt
# from currentEvent import getCurrentEventId

class User(models.Model):
    # UserId = models.IntegerField()
    user_name = models.CharField(max_length = 45)
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    phone = models.CharField(max_length = 45)
    password = models.CharField(max_length = 245)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Device(models.Model):
    # DeviceId = models.IntegerField()
    user_id = models.IntegerField(default=False)
    device_number = models.IntegerField()
    serial_number = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    event_id = models.IntegerField()
    name = models.CharField(max_length = 245)
    address = models.CharField(max_length = 245)
    header_image = models.CharField(max_length = 245)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Media(models.Model):
    # Adding features to allow more functionality with the front end
    views = models.IntegerField(default = 0)
    starred = models.IntegerField(default = 0)
    user_id = models.IntegerField(default=False)
    device_id = models.IntegerField(default=False)
    
    # the event_id needs to be able to be manipulated to the id that we want it to be
    # event_id = models.IntegerField(default=getCurrentEventId()) # default value is the value that will be passed to all of the incoming api posts for new media
    event_id = models.IntegerField(default=3)
    media_type = models.CharField(max_length=10) # either image, or video 
    link = models.CharField(max_length=245)
    raw_or_edited = models.CharField(max_length=45) # either raw, edited, or curated
    downloaded = models.IntegerField(default=False)
    ranking = models.IntegerField(default=1)
    date = models.CharField(max_length = 245)
    date_time = models.CharField(max_length = 245)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    gif_link = models.CharField(max_length=245)

class UserEvent(models.Model):
    user_id = models.IntegerField(default=False)
    event_id = models.IntegerField(default=False)

class MediaComment(models.Model):
    user_id = models.IntegerField(default=False)
    media_id = models.IntegerField(default=False)
    comment = models.TextField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class MediaLike(models.Model):
    user_id = models.IntegerField(default=False)
    media_id = models.IntegerField(default=False)
    comment = models.TextField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class MediaComment(models.Model):
    user_id = models.IntegerField(default=False)
    media_id = models.IntegerField(default=False)
    comment = models.TextField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class MediaLike(models.Model):
    user_id = models.IntegerField(default=False)
    media_id = models.IntegerField(default=False)
    # comment = models.TextField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return '%s %s' % (self.title, self.body)
