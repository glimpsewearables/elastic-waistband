from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class User(models.Model):
    # UserId = models.IntegerField()
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    phone = models.CharField(max_length = 45)
    password = models.CharField(max_length = 245)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Device(models.Model):
    # DeviceId = models.IntegerField()
    UserId = models.ForeignKey(User, related_name="devices", null=True)
    device_number = models.IntegerField()
    serial_number = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    # EventId = models.IntegerField()
    name = models.CharField(max_length = 245)
    address = models.CharField(max_length = 245)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Media(models.Model):
    # MediaId = models.IntegerField()
    UserId = models.ForeignKey(User, related_name="uploads", null=True)
    DeviceId = models.ForeignKey(Device, related_name="content", null=True)
    event = models.ForeignKey(Event, related_name="media_at_event", null=True)
    media_type = models.CharField(max_length=10)# either image, or video
    link = models.CharField(max_length=245)
    raw_or_edited = models.CharField(max_length=45)
    downloaded = models.IntegerField(default=False)
    ranking = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class UserEvent(models.Model):
    user_id = models.ForeignKey(User, related_name="user_at_events", null=True)
    event_id = models.ForeignKey(Event, related_name="event_attending", null=True)

def __str__(self):
        return '%s %s' % (self.title, self.body)
