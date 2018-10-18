from tastypie.resources import ModelResource
from .models import User, Event, Device, Media
from tastypie.authorization import Authorization

# These files are used for the querying of data on the server side of the applications
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        authorization = Authorization()

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = "event"
        authorization = Authorization()

class DeviceResource(ModelResource):
    class Meta:
        queryset = Device.objects.all()
        resource_name = "device"
        authorization = Authorization()

class MediaResource(ModelResource):
    class Meta:
        queryset = Media.objects.all()
        resource_name = "media"
        authorization = Authorization()