from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^users$', views.index),
    url(r'^users/userPage/(?P<user_id>\d+)$', views.userPage),
]  