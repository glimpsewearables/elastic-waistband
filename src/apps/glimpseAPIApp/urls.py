from django.conf.urls import url, include
from . import views, models
from .resources import UserResource, EventResource, MediaResource, DeviceResource

user_resource = UserResource()
event_resource = EventResource()
media_resource = MediaResource()
device_resource = DeviceResource()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^media$', views.mediaHome),
    url(r'^updateDatabase$', views.updateDatabase),
    url(r'^media/getAllImages$', views.getAllImages),
    url(r'^media/getAllVideos$', views.getAllVideos),
    url(r'^media/getAllUserImages/(?P<user_id>\d+)$', views.getAllUserImages),
    url(r'^media/getAllUserVideos/(?P<user_id>\d+)$', views.getAllUserVideos),
    url(r'^media/getAllImagesUserEvent/(?P<user_id>\d+)/(?P<event_id>\d+)$', views.getAllImagesUserEvent),
    url(r'^media/getAllVideosUserEvent/(?P<user_id>\d+)/(?P<event_id>\d+)$', views.getAllVideosUserEvent),
    url(r'^media/getAllUsers$', views.getAllUsers),
    url(r'^media/getSpecificUser/(?P<user_id>\d+)$', views.getSpecificUser),
    url(r'^media/getSpecificUserByEmail/(?P<user_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.getSpecificUserByEmail),
    url(r'^media/getAllEvents$', views.getAllEvents),
    url(r'^media/getSpecificEvent/(?P<event_id>\d+)$', views.getSpecificEvent),
    url(r'^media/getAllDevices$', views.getAllDevices),
    url(r'^media/getSpecificDevice/(?P<device_id>\d+)$', views.getSpecificDevice),
    # Api function calls 
    url(r'^api/', include(user_resource.urls)),
    url(r'^api/', include(device_resource.urls)),
    url(r'^api/', include(media_resource.urls)),
    url(r'^api/', include(event_resource.urls)),
]  