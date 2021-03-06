from django.conf.urls import url, include
from . import views, models, adding, rendering, currentEvent, fixingErrors
from .resources import UserResource, UserEventResource, ArtistResource, ArtistEventResource, EventResource, MediaResource, DeviceResource, CommentResource, LikeResource
from django.conf import settings
from django.conf.urls.static import static

user_resource = UserResource()
user_event_resource = UserEventResource()
artist_resource = ArtistResource()
artist_event_resource = ArtistEventResource()
event_resource = EventResource()
media_resource = MediaResource()
device_resource = DeviceResource()
comment_resource = CommentResource()
like_resource = LikeResource()

urlpatterns = [
    url(r'^$', rendering.index),
    url(r'^media$', views.mediaHome),
    url(r'^updateDatabase$', adding.updateDatabase),
    # url(r'^fixDatabase$', adding.fixDatabase),
    url(r'^checkUrls$', views.checkUrls),
    url(r'^removeDuplicates$', views.removeDuplicates),
    url(r'^logout$', views.logout),
    url(r'^media/getAllImages$', views.getAllImages),
    url(r'^media/getAllVideos$', views.getAllVideos),
    url(r'^media/getAllUserMedia/(?P<userId>\d+)$', views.getAllUserMedia),
    url(r'^media/getAllUsers$', views.getAllUsers),
    url(r'^media/getAllArtists$', views.getAllArtists),
    url(r'^media/getSpecificUser/(?P<user_id>\d+)$', views.getSpecificUser),
    url(r'^media/getSpecificArtist/(?P<artist_id>\d+)$', views.getSpecificArtist),
    url(r'^media/getSpecificUserByEmail/(?P<user_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.getSpecificUserByEmail),
    url(r'^media/getSpecificUserByUsername/(?P<user_name>[-\w]+)/$', views.getSpecificUserByUsername),
    url(r'^media/getAllEvents$', views.getAllEvents),
    url(r'^media/getSpecificEvent/(?P<eventId>\d+)$', views.getSpecificEvent),
    url(r'^media/getAllDevices$', views.getAllDevices),
    url(r'^media/getSpecificDevice/(?P<device_id>\d+)$', views.getSpecificDevice),


    # Unused Calls
    url(r'^media/getAllUserVideos/(?P<userId>\d+)$', views.getAllUserVideos),
    url(r'^media/getAllImagesUserEvent/(?P<userId>\d+)/(?P<eventId>\d+)$', views.getAllImagesUserEvent),
    url(r'^media/getAllVideosUserEvent/(?P<userId>\d+)/(?P<eventId>\d+)$', views.getAllVideosUserEvent),
    
    # Api function calls 
    url(r'^api/', include(user_resource.urls)),
    url(r'^api/', include(user_event_resource.urls)),
    url(r'^api/', include(artist_resource.urls)),
    url(r'^api/', include(artist_event_resource.urls)),
    url(r'^api/', include(device_resource.urls)),
    url(r'^api/', include(media_resource.urls)),
    url(r'^api/', include(event_resource.urls)),
    url(r'^api/', include(comment_resource.urls)),
    url(r'^api/', include(like_resource.urls)),

    # Views for portal
    url(r'^login$', rendering.login),
    url(r'^browsing$', rendering.browsing),
    url(r'^SoundOff$', rendering.soundOff),
    url(r'^userPage/(?P<device_number>\d+)$', rendering.userPage),
    url(r'^usersEventPage/(?P<eventId>\d+)/(?P<userId>\d+)$', rendering.usersEventPage),
    url(r'^artistPage/(?P<artist_id>\d+)$', rendering.artistPage),
    url(r'^adminLogin$', rendering.adminLogin),
    url(r'^adminPage$', rendering.adminPage),
    url(r'^viewEventMedia/(?P<event_id>\d+)$', rendering.viewEventMedia),
    url(r'^setCurrentEvent/(?P<event_id>\d+)$', currentEvent.setCurrentEvent),
    # Admin Portal Routes
    url(r'^curatorPortal$', rendering.curatorPortal),
    url(r'^userTestingPortal$', rendering.userTestingPortal),
    url(r'^devicePortal$', rendering.devicePortal),
    url(r'^softwarePortal$', rendering.softwarePortal),
    
    # Adding/Deleting information to the database
    url(r'^registerUser$', adding.registerUser),
    url(r'^createUser$', adding.createUser),
    url(r'^createEvent$', adding.createEvent),
    url(r'^createMedia$', adding.createMedia),
    url(r'^createDevice$', adding.createDevice),
    url(r'^deleteUser/(?P<user_id>\d+)$', adding.deleteUser),
    url(r'^deleteEvent/(?P<event_id>\d+)$', adding.deleteEvent),
    url(r'^deleteDevice/(?P<device_id>\d+)$', adding.deleteDevice),
    # CSV work for metrics
    url(r'^exportCsv$', views.fromDatabase),
    # S3 Calls
    url(r'^testS3Download$', adding.testS3Download), 
    url(r'^uploadMediaToS3$', adding.uploadMediaToS3), 

    # Testing Calls
    url(r'^fixingErrors$', fixingErrors.partitionVideos), 
]
