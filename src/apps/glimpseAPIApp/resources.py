from tastypie.resources import ModelResource
from .models import User, UserEvent, Artist, ArtistEvent, Event, Device, Media, MediaComment, MediaLike
import requests
from tastypie.authorization import Authorization
from .currentEvent import getCurrentEventId

# These files are used for the querying of data on the server side of the applications
class UserResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        authorization = Authorization()

class UserEventResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put', "PATCH"]
    class Meta:
        queryset = UserEvent.objects.all()
        resource_name = "userevent"
        authorization = Authorization()

class ArtistResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = Artist.objects.all()
        resource_name = "artist"
        authorization = Authorization()

class EventResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = Event.objects.all()
        resource_name = "event"
        authorization = Authorization()
        # Event.event_id = getCurrentEventId(request)

class ArtistEventResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = ArtistEvent.objects.all()
        resource_name = "artistevent"
        authorization = Authorization()

class DeviceResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = Device.objects.all()
        resource_name = "device"
        authorization = Authorization()
class MediaResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = Media.objects.all()
        resource_name = "media"
        authorization = Authorization()

class CommentResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = MediaComment.objects.all()
        resource_name = "comment"
        authorization = Authorization()

class LikeResource(ModelResource):
    http_method_names = ['get', 'post', 'head', 'put']
    class Meta:
        queryset = MediaLike.objects.all()
        resource_name = "like"
        authorization = Authorization()