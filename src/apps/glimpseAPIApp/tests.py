from __future__ import unicode_literals

from django.test import TestCase
from views import *
from models import *
from datetime import datetime

# Create your tests here.
class UserTests(TestCase):
	def setUp(self):
		User.objects.create(user_name="xx_mouseyboi_xx", first_name="mickey", last_name="mouse", email="mickmouse@mousemail.com", 
			phone="(678) 999-8212", password="hunter2")

	def test_jsonify_user(self):
		user = User.objects.get(first_name="mickey", last_name="mouse")
		createdAt = user.created_at
		updatedAt = user.updated_at
		expectedJson = "{'users': [{'phone': u'(678) 999-8212', 'first_name': u'mickey', 'last_name': u'mouse', 'created_at': '%s', 'password': u'hunter2', 'user_name': u'xx_mouseyboi_xx', 'email': u'mickmouse@mousemail.com', 'updated_at': '%s'}]}" % (createdAt, updatedAt)
		self.assertEqual(str(jsonifyUserData([user])), expectedJson.encode('ascii','ignore'))

class DeviceTests(TestCase):
	def setUp(self):
		Device.objects.create(user_id=1, device_number=1, serial_number=1)

	def test_jsonify_device(self):
		device = Device.objects.get(user_id=1)
		createdAt = device.created_at
		updatedAt = device.updated_at
		expectedJson = "{'devices': [{'serial_number': u'1', 'created_at': '%s', 'user_id': 1, 'updated_at': '%s', 'device_number': 1}]}" % (createdAt, updatedAt)
		self.assertEqual(str(jsonifyDeviceData([device])), expectedJson.encode('ascii','ignore'))

class EventTests(TestCase):
	date = datetime(1901, 01, 01)

	def setUp(self):
		Event.objects.create(name="test event", address="123 pillsberry lane", 
			start_date=self.date, end_date=self.date, long=0.1, lat=0.1)

	def test_jsonify_event(self):
		event = Event.objects.get(name="test event")
		createdAt = event.created_at
		updatedAt = event.updated_at
		expectedJson = "{'name': u'test event', 'end_date': '1901-01-01 00:00:00+00:00', 'address': u'123 pillsberry lane', 'lat': '0.100', 'created_at': '%s', 'start_date': '1901-01-01 00:00:00+00:00', 'long': '0.100', 'updated_at': '%s'}" % (createdAt, updatedAt)
		self.assertEqual(str(jsonifyEventData(event)), expectedJson.encode('ascii','ignore'))

class MediaTests(TestCase):
	def setUp(self):
		Media.objects.create(user_id=1, device_id=1, event_id=1, media_type="image", 
			link="a.com", raw_or_edited="raw", downloaded=0, ranking=1, gif_link="a.com")

	def test_jsonify_media(self):
		media = Media.objects.get(user_id=1)
		createdAt = media.created_at
		updatedAt = media.updated_at
		expectedJson = "{'media': [{'ranking': 1, 'updated_at': '%s', 'downloaded': 0, 'link': u'a.com', 'device_id': '1', 'user_id': '1', 'event_id': '1', 'created_at': '%s', 'raw_or_edited': u'raw', 'media_type': u'image', 'gif_link': u'a.com'}]}" % (updatedAt, createdAt)
		self.assertEqual(str(jsonifyMediaData([media])), expectedJson.encode('ascii','ignore'))