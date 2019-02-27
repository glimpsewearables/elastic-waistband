from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json
import requests
from django.db import models
from .models import User, UserEvent, Artist, ArtistEvent, Device, Event, Media, MediaComment
client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
v1_raw_bucket = resource.Bucket('pi-1')
v1_edited_bucket = resource.Bucket('pi-2')
v2_raw_bucket = resource.Bucket('users-raw-content')
v2_edited_bucket = resource.Bucket('users-edited-content') 


# This is the page with all of the functions for viewing and rendering pages 
def index(request): # this is the standard endpoint that will not return anything
    return render(request, "portal.html", status=200)

def login(request):
    if request.method=="POST":
        device_number = request.POST['deviceNumber']
        request.session["deviceNumber"] = device_number
        request.session["userType"] = "user"
    return redirect("/userPage/" + device_number)

def browsing(request):
    context = {}
    all_events = Event.objects.all()
    all_artists = Artist.objects.all()
    
    context["events"] = all_events
    context["artists"] = all_artists
    return render(request, "browsing.html", context)

def userPage(request, device_number):
    this_device_content = Media.objects.filter(user_id = device_number, media_type = "video").order_by('created_at')
    all_events = Event.objects.all().order_by('id').reverse()
    most_recent = this_device_content.order_by('-date', "-date_time")[:9]
    featured = this_device_content.filter(featured = 1)
    this_users_event_content = {}
    this_users_event_content["all_artists"] = Artist.objects.all()
    this_users_event_content["all_events"] = all_events
    this_users_event_content["my_events"] = []
    this_users_event_content["device_number"] = device_number
    this_users_event_content["most_recent"] = most_recent
    this_users_event_content["featured"] = featured
    this_users_event_content["total_vids"] = len(this_device_content)
    this_users_event_content["last_video"] = this_device_content[:1]
    for event in all_events:
        this_id = event.event_id
        if this_device_content.filter(event_id = event.event_id):
            allTheseVideos = this_device_content.filter(event_id = this_id)
            # partedVideos = partitionVideos(request, this_id, device_number)
            # print partedVideos
            # this_users_event_content["event" + str(this_id)] = {
            #     "videos" : partedVideos,
            #     "eventInfo" : event,
            #     "numVids" : len(allTheseVideos)
            # }
            # Working code
            this_users_event_content["event" + str(this_id)] = {
                "videos" : this_device_content.filter(event_id = this_id),
                "eventInfo" : event,
                "numVids" : len(allTheseVideos)
            }
            this_users_event_content["my_events"].append(event.event_id)
        else: 
            this_users_event_content["event" + str(this_id)] = {
                "eventInfo" : event,
            }
    return render(request, "userPage.html", context=this_users_event_content)

def usersEventPage(request, eventId, userId):
    context = {}
    all_events = Event.objects.all()
    this_user = User.objects.get(id = userId)
    this_event = Event.objects.get(id = eventId)
    this_event_content = Media.objects.filter(device_id = userId, event_id = eventId).order_by('-date', "-date_time")
    context["media"] = this_event_content.order_by('-date', "-date_time")
    context["this_event"] = this_event
    context["all_events"] = all_events
    context["this_user"] = this_user
    return render(request, "userEventPage.html", context)

# Break up all of the videos into segments of nine in order to deal with rendering issues for massive ammounts of videos in html
def partitionVideos(request, event_id, device_id):
    allVideos = Media.objects.filter(device_id = device_id, event_id = event_id, media_type = "video")
    all_videos = []
    groupedVideos = {}
    for video in allVideos:
        all_videos.append(video.link)
    for i in range(0, (len(all_videos) / 9) + 1):
        groupedVideos["videos" + str(i)] = []
    section = 0
    for i in range(0, len(all_videos)):
        groupedVideos["videos" + str(section)].append(all_videos[i])
        if i % 9 == 0 and i != 0:
            section += 1
    return groupedVideos

def checkLogin():
    if request.session["deviceNumber"]:
        return True
    else:
        return False

def adminLogin(request):
    if request.method=="POST":
        adminName = request.POST['adminName']
        adminPassword = request.POST['adminPassword']
        if adminName == "Master Boss" and adminPassword == "MasterMaster":
            request.session["userType"] = "masterAdmin"
            return redirect('/adminPage')
        elif adminName == "Software Team" and adminPassword == "SoftwarePassword": 
            request.session["userType"] = "softwareAdmin"
            return redirect('/softwarePortal')
        elif adminName == "Curator Team" and adminPassword == "CuratorPassword":
            request.session["userType"] = "curatorAdmin"
            return redirect('/curatorPortal')
        elif adminName == "User Testing Team" and adminPassword == "UserTestingPassword":
            request.session["userType"] = "userTestingAdmin"
            return redirect('/userTestingPortal')
        elif adminName == "Device Team" and adminPassword == "DevicePassword":
            request.session["userType"] = "deviceAdmin"
            return redirect('/devicePortal')
        else:
            return redirect('/')

def curatorPortal(request):
    # if request.session["userType"] == "curatorAdmin" or request.session["userType"] == "masterAdmin":
    all_images = Media.objects.filter(media_type = "image")
    all_videos = Media.objects.filter(media_type = "video").order_by('-date', "-date_time")
    userType = request.session["userType"]
    context = {
        "user_type" : userType,
        "image_number" : len(all_images), 
        "all_videos" : all_videos,
        "video_number" : len(all_videos),
        "all_users" : User.objects.all(),
        "all_events" : Event.objects.all(),
        "event_number" :len(Event.objects.all()),
        "all_devices" : Device.objects.all(),
        "device_number" : len(Device.objects.all()),
    }
    return render(request, "portalPages/curatorPortal.html", context)
    # else:
    #     return redirect("/")

def softwarePortal(request):
    # if request.session["userType"] == "softwareAdmin" or request.session["userType"] == "masterAdmin":
    all_images = Media.objects.filter(media_type = "image")
    all_videos = Media.objects.filter(media_type = "video").order_by('-date', "-date_time")
    userType = request.session["userType"]
    context = {
        "user_type" : userType,
        "image_number" : len(all_images), 
        "all_videos" : all_videos,
        "video_number" : len(all_videos),
        "all_users" : User.objects.all(),
        "all_events" : Event.objects.all(),
        "event_number" :len(Event.objects.all()),
        "all_devices" : Device.objects.all(),
        "device_number" : len(Device.objects.all()),
    }
    return render(request, "portalPages/softwarePortal.html", context)
    # else:
    #     return redirect("/")

def userTestingPortal(request):
    # if request.session["userType"] == "userTestingAdmin" or request.session["userType"] == "masterAdmin":
    all_images = Media.objects.filter(media_type = "image")
    all_videos = Media.objects.filter(media_type = "video").order_by('-date', "-date_time")
    all_user_events = UserEvent.objects.all()
    userType = request.session["userType"]
    context = {
        "all_user_events": all_user_events,
        "user_type" : userType,
        "image_number" : len(all_images), 
        "all_videos" : all_videos,
        "video_number" : len(all_videos),
        "all_users" : User.objects.all(),
        "all_events" : Event.objects.all(),
        "event_number" :len(Event.objects.all()),
        "all_devices" : Device.objects.all(),
        "device_number" : len(Device.objects.all()),
    }
    return render(request, "portalPages/userTestingPortal.html", context)
    # else:
    #     return redirect("/")

def devicePortal(request):
    # if request.session["userType"] == "deviceAdmin" or request.session["userType"] == "masterAdmin":
    all_images = Media.objects.filter(media_type = "image")
    all_videos = Media.objects.filter(media_type = "video").order_by('-date', "-date_time")
    userType = request.session["userType"]
    context = {
        "user_type" : userType,
        "image_number" : len(all_images), 
        "all_videos" : all_videos,
        "video_number" : len(all_videos),
        "all_users" : User.objects.all(),
        "all_events" : Event.objects.all(),
        "event_number" :len(Event.objects.all()),
        "all_devices" : Device.objects.all(),
        "device_number" : len(Device.objects.all()),
    }
    return render(request, "portalPages/devicePortal.html", context)
    # else:
    #     return redirect("/")


def adminPage(request):
    # if request.session["userType"] != "admin":
    #     return redirect("/")
    # else:
    all_images = Media.objects.filter(media_type = "image")
    all_videos = Media.objects.filter(media_type = "video").order_by('-date', "-date_time")
    last_video = all_videos.first()
    context = {
        "image_number" : len(all_images), 
        "all_videos" : all_videos,
        "video_number" : len(all_videos),
        "all_users" : User.objects.all(),
        "all_events" : Event.objects.all(),
        "event_number" :len(Event.objects.all()),
        "all_devices" : Device.objects.all(),
        "device_number" : len(Device.objects.all()),
        "last_video" : last_video
    }
    return render(request, "adminPage.html", context)

def viewEventMedia(request, event_id):
    # if request.session["userType"] != "admin":
    #     return redirect("/")
    # else:
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
    context = {}
    this_event = Event.objects.get(id = event_id)
    this_event_images = Media.objects.filter(event_id = event_id, media_type = "image").order_by('-date', "-date_time")
    this_event_videos = Media.objects.filter(event_id = event_id, media_type = "video").order_by('-date', "-date_time")
    context["this_event"] = this_event
    context["this_event_images"] = this_event_images
    context["this_event_videos"] = this_event_videos
    context["desktop"] =  desktop
    return render(request, "viewMedia.html", context)

def artistPage(request, artist_id):
    thisArtist = Artist.objects.get(id = artist_id)
    thisArtistEvents = ArtistEvent.objects.filter(artist_id = artist_id)
    allEventsWithMedia = []
    for artistEvent in thisArtistEvents:
        thisEventMedia = Media.objects.filter(event_id = artistEvent.event_id)
        thisEvent = {
            "event": Event.objects.get(event_id = artistEvent.event_id),
            "eventMedia": thisEventMedia
        }
        allEventsWithMedia.append(thisEvent)
    context = {}
    context["artist"] = thisArtist
    context["thisArtistsEvents"] = thisArtistEvents
    context["eventsWithMedia"] = allEventsWithMedia
    return render(request, "artistPage.html", context)
