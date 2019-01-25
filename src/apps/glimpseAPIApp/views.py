from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json, inspect, urllib
import requests
from django.db import models
from .models import User, UserEvent, Artist, ArtistEvent, Device, Event, Media, MediaComment
client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
v1_raw_bucket = resource.Bucket('pi-1')
v1_edited_bucket = resource.Bucket('pi-2')
v2_raw_bucket = resource.Bucket('users-raw-content')
v2_edited_bucket = resource.Bucket('users-edited-content') 

# Initializing the database 
# Only to be used once at the very beginning of launching the website to transfer all of the 
# existing files that are stored in the s3 database but not yet tracked in the sql database specific
# to the api that we are using
# Once the api is able to continually update the sql database every time an image is uploaded 
# this function will never have to be run again
def fromDatabase(request):
    allMedia = Media.objects.all() 
    myFields = ['media_id', 'user_id', 'device_id', 'event_id', 'link', 'date', 'date_time', 'views', 'starred', 'media_type', 'raw_or_edited', 'downloaded', 'ranking', 'created_at', 'updated_at', 'gif_link']  
    response = HttpResponse(content_type='text/csv')
    today = datetime.date.today()
    response['Content-Disposition'] = 'attachment; filename="glimpseMetrics.csv"'
    writer = csv.writer(response)
    writer.writerow(myFields)
    for data_point in allMedia:
        adding_context = [
            data_point.id,
            str(data_point.user_id),
            str(data_point.device_id),
            str(data_point.event_id),
            data_point.link,
            data_point.date,
            data_point.date_time,
            data_point.views,
            data_point.starred,
            data_point.media_type,
            data_point.raw_or_edited,
            data_point.downloaded,
            data_point.ranking,
            str(data_point.created_at),
            str(data_point.updated_at),
            data_point.gif_link
        ]
        writer.writerow(adding_context)
    return response

# The link to certain urls has been changing, this is where you can update the links
def checkUrls(request):
    allMedia =  Media.objects.all()
    startingLink = 'https://s3-us-west-2.'
    for media in allMedia:
        oldLink = media.link
        oldId = media.id
        if oldLink.startswith('https://s3.'):
            newLink = startingLink + oldLink[11:]
            old = Media.objects.filter(id = oldId)
            old.link = newLink
            old.save()
            print(newLink + " is the new link")
        else:
            print("good link")
    return redirect("/")

def removeDuplicates(request):
    allMedia =  Media.objects.all()
    for media in allMedia:
        if allMedia.filter(link = media.link):
            print("duplicate")
        else:
            print("not a duplicate")
    return redirect("/")

def logout(request):
    request.session["userType"] = None
    request.session["deviceNumber"] = None
    return redirect("/")
# All of the endpoints for retrieving information from the api call
def mediaHome(request):
    response = "here is the home page from the media application portion of the api"
    return HttpResponse(response)


# Links being used
def getAllUserMedia(request, userId): # grabs ALL images connected to the specific user that are being stored in the raw bucket
    context = {}
    raw_media = Media.objects.filter(user_id = userId, raw_or_edited = "raw")
    edited_media = Media.objects.filter(user_id= userId, raw_or_edited = "edited")
    featured_media = Media.objects.filter(user_id= userId, raw_or_edited = "featured")
    curated_media = Media.objects.filter(user_id= userId, raw_or_edited = "curated")
    json_raw_media = jsonifyMediaData(raw_media)
    json_edited_media = jsonifyMediaData(edited_media)
    json_curated_media = jsonifyMediaData(curated_media)
    json_featured_media = jsonifyMediaData(featured_media)
    context["raw_media"] = json_raw_media
    context["edited_media"] = json_edited_media
    context["featured_media"] = json_featured_media
    context["curated_media"] = json_curated_media
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getAllDeviceMedia(request, deviceId): # grabs ALL images connected to the specific user that are being stored in the raw bucket
    context = {}
    raw_media = Media.objects.filter(device_id = deviceId, raw_or_edited = "raw")
    edited_media = Media.objects.filter(device_id = deviceId, raw_or_edited = "edited")
    featured_media = Media.objects.filter(device_id = deviceId, raw_or_edited = "featured")
    curated_media = Media.objects.filter(device_id = deviceId, raw_or_edited = "curated")
    json_raw_media = jsonifyMediaData(raw_media)
    json_edited_media = jsonifyMediaData(edited_media)
    json_curated_media = jsonifyMediaData(curated_media)
    json_featured_media = jsonifyMediaData(featured_media)
    context["raw_media"] = json_raw_media
    context["edited_media"] = json_edited_media
    context["featured_media"] = json_featured_media
    context["curated_media"] = json_curated_media
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getAllEvents(request): # grabs ALL events from mysql database
    all_events = Event.objects.all()
    newContext = json.dumps(jsonifyEventData(all_events))
    return HttpResponse(newContext, content_type="application/json")

def getSpecificEvent(request, eventId): # grabs a specific event from the mySQL database
    context = {}
    newContext = {}
    if Event.objects.filter(event_id = eventId):
        response = "Getting a single specific event with a event id of"
        this_event = Event.objects.get(event_id = eventId)
        this_event_content = Media.objects.filter(event_id = eventId)
        context["this_event"] = jsonifyEventData(this_event)
        context["this_event_content"] = jsonifyMediaData(this_event_content)
        newContext = json.dumps(context)
    else:
        newContext["error"] = "You entered a event that does not exist"
    return HttpResponse(newContext, content_type="application/json")

def getAllDevices(request): # grabs a specific user from the mySQL database
    all_devices = Device.objects.all()
    context = jsonifyDeviceData(all_devices)
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificDevice(request, device_id): # grabs all Devices from the mySQL database
    context = {}
    if Device.objects.filter(id = device_id):
        this_device = Device.objects.filter(id=device_id)
        context = jsonifyDeviceData(this_device)
    else:
        context["error"] = "You entered a device that does not exist"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getAllUsers(request): # grabs a specific user from the mySQL database
    all_users = User.objects.all()
    context = jsonifyUserData(all_users)
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getAllArtists(request): # grabs a specific user from the mySQL database
    all_artists = Artist.objects.all()
    context = jsonifyArtistData(all_artists)
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificUser(request, user_id): # grabs all users from the mySQL database
    context = {}
    if User.objects.filter(id = user_id):
        this_user = User.objects.filter(id=user_id)
        all_media = Media.objects.filter(user_id = user_id).order_by('-date', "-date_time")
        thisUsersEvents = UserEvent.objects.filter(user_id = user_id)
        json_media = jsonifyMediaData(all_media)
        json_events = jsonifyUserEventData(thisUsersEvents, user_id)
        context["user"] = jsonifyUserData(this_user)
        context["user_events"] = json_events
        context["media"] = json_media
    else:
        context["error"] = "You entered a user that does not exist"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificArtist(request, artist_id): # grabs all users from the mySQL database
    context = {}
    if Artist.objects.filter(id = artist_id):
        this_artist = Artist.objects.filter(id=artist_id)
        thisArtistEvents = ArtistEvent.objects.filter(artist_id = artist_id)
        # for event in thisArtistEvents:
        #     thisMedia = Media.objects.filter(event_id = event.event_id)
        #     thisEvent = Event.objects.filter(event_id = event.event_id)
        # json_feat = jsonifyMediaData(featured_content)
        json_events = jsonifyArtistEventData(thisArtistEvents)
        context["artist"] = jsonifyArtistData(this_artist)
        context["artist_events"] = json_events
        # context["all_events_media"] = json_all_events_media
    else:
        context["error"] = "You entered a user that does not exist"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificUserByEmail(request, user_email):
    context = {}
    if User.objects.filter(email = user_email):
        this_user = User.objects.filter(email = user_email)
        context = jsonifyUserData(this_user)
    else:
        context["error"] = "You entered a user that does not exist"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificUserByUsername(request, user_name):
    context = {}
    if User.objects.filter(user_name = user_name):
        this_user = User.objects.filter(user_name = user_name)
        context = jsonifyUserData(this_user)
    else:
        context["error"] = "You entered an invalid username"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")


# Unused Links
def getAllImages(request): # grabs ALL images that are being stored in the raw bucket
    context = {}
    all_images = Media.objects.filter(media_type = "image")
    json_images = jsonifyMediaData(all_images)
    newContext = json.dumps(json_images)
    return HttpResponse(newContext, content_type="application/json")

def getAllVideos(request): # grabs ALL videos that are being stored in the raw bucket
    context = {}
    all_videos = Media.objects.filter(media_type = "video")
    json_videos = jsonifyMediaData(all_videos)
    newContext = json.dumps(json_videos)
    return HttpResponse(newContext, content_type="application/json")

def getAllUserVideos(request, userId): # grabs ALL videos connected to the specific user that are being stored in the raw bucket
    context = {}
    if User.objects.filter(id = userId):
        response = "Getting all videos specific to a user..."
        videos_raw = Media.objects.filter(user_id = userId, media_type = "video", raw_or_edited = "raw")
        videos_edited = Media.objects.filter(user_id = userId, media_type = "video", raw_or_edited = "edited")
        json_raw_videos = jsonifyMediaData(videos_raw)
        json_edited_videos = jsonifyMediaData(videos_edited)
        context["raw_videos"] = json_raw_videos
        context["edited_videos"] = json_edited_videos
    else:
        context["error"] = "You entered a user that does not exist"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getAllImagesUserEvent(request, userId, eventId): # grabs all images for a specific user at a specific event
    context = {}
    if Event.objects.filter(id = eventId) and Device.objects.filter(id = userId):
        response = "Getting all images for a single user at a specific event with a event id of" + eventId
        user_event_images = Media.objects.filter(event_id = eventId, user_id = userId, media_type="image")
        json_user_event_images = jsonifyMediaData(user_event_images)
        context["user_event_images"] = json_user_event_images
    else:
        context["error"] = "You entered a user or event that does not exist"
    return HttpResponse(json.dumps(context), content_type="application/json")

def getAllVideosUserEvent(request, userId, eventId): # grabs all videos for a specific user at a specific event
    context = {}
    if Event.objects.filter(id = eventId):
        user_event_videos = Media.objects.filter(event_id = eventId, user_id = userId, media_type="video")
        json_user_event_videos = jsonifyMediaData(user_event_videos)
        context["user_event_videos"] = json_user_event_videos
    else:
        context["error"] = "You entered a user or event that does not exist"
    return HttpResponse(json.dumps(context), content_type="application/json")

# Converting the object based data into json data that can be parsed and returned by the api
def jsonifyMediaData(data):
    context = {}
    all_edited_media = []
    all_raw_media = []
    all_curated_media = []
    all_featured_media = []
    for data_point in data:
        arrayToGoIn = data_point.raw_or_edited
        adding_context = {
            "views" : data_point.views,
            "starred" : data_point.starred,
            "link" : data_point.link,
            "user_id" : str(data_point.user_id),
            "device_id" : str(data_point.device_id),
            "event_id" : str(data_point.event_id),
            "media_type" : data_point.media_type,
            "raw_or_edited" : data_point.raw_or_edited,
            "downloaded" : data_point.downloaded,
            "ranking" : data_point.ranking,
            "created_at" : str(data_point.created_at),
            "updated_at" : str(data_point.updated_at),
            "gif_link" : data_point.gif_link,
            "date": data_point.date,
            "date_time": data_point.date_time
        }
        if data_point.raw_or_edited == "raw":
            all_raw_media.append(adding_context)
        elif data_point.raw_or_edited == "edited":
            all_edited_media.append(adding_context)
        elif data_point.raw_or_edited == "featured":
            all_featured_media.append(adding_context)
        elif data_point.raw_or_edited == "curated":
            all_curated_media.append(adding_context)
    context.update({
        "raw_media" : all_raw_media,
        "featured_media" : all_featured_media,
        "curated_media" : all_curated_media,
        "edited_media" : all_edited_media
    })
    return context

def jsonifyEventData(data):
    context = {}
    if len(data) == 1:
        adding_context = {
            "id" : data[0].id,
            "event_id" : data[0].event_id,
            "name" : data[0].name,
            "header_image": data[0].header_image,
            "address" : data[0].address,
            "start_date" : str(data[0].start_date),
            "end_date" : str(data[0].end_date),
            "header_image": str(data[0].header_image),
            "long" : str(data[0].long),
            "lat" : str(data[0].lat),
            "created_at" : str(data[0].created_at),
            "updated_at" : str(data[0].updated_at)
        }
        return adding_context
    else:
        all_events = []
        for data_point in data:
            adding_context = {
                "id" : data_point.id,
                "event_id" : data_point.event_id,
                "name" : data_point.name,
                "header_image": data_point.header_image,
                "address" : data_point.address,
                "start_date" : str(data_point.start_date),
                "end_date" : str(data_point.end_date),
                "header_image": str(data_point.header_image),
                "long" : str(data_point.long),
                "lat" : str(data_point.lat),
                "created_at" : str(data_point.created_at),
                "updated_at" : str(data_point.updated_at)
            }
            all_events.append(adding_context)
        context.update({"all_events" : all_events})
        return context

def jsonifyDeviceData(data):
    context = {}
    all_events = []
    for data_point in data:
        adding_context = {
            "serial_number" : data_point.serial_number,
            "device_number" : data_point.device_number,
            "user_id" : data_point.user_id,
            "created_at" : str(data_point.created_at),
            "updated_at" : str(data_point.updated_at)
        }
        all_events.append(adding_context)
    context.update({"devices" : all_events})
    return context

def jsonifyUserEventData(data, user_id):
    context = {}
    all_events = []
    all_events_media = []
    for data_point in data:
        all_events.append(jsonifyEventData(Event.objects.filter(event_id = data_point.event_id)))
        all_events_media.append(jsonifyMediaData(Media.objects.filter(event_id = data_point.event_id, user_id = user_id, media_type = "video").order_by('-date', "-date_time")))
    context["events"] = all_events
    context["events_media"] = all_events_media
    return context

def jsonifyArtistEventData(data):
    context = {}
    all_events = []
    all_events_media = []
    for data_point in data:
        all_events.append(jsonifyEventData(Event.objects.filter(event_id = data_point.event_id)))
        all_events_media.append(jsonifyMediaData(Media.objects.filter(event_id = data_point.event_id)))
    context["events"] = all_events
    context["events_media"] = all_events_media
    return context

def jsonifyUserData(data):
    context = {}
    if len(data) == 1:
        context = {
            "user_id" : data[0].id,
            "user_name" : data[0].user_name,
            "first_name" : data[0].first_name,
            "last_name" : data[0].last_name,
            "profile_pic_link" : data[0].profile_pic_link,
            "email" : data[0].email,
            "phone" : data[0].phone,
            "password" : data[0].password,
            "created_at" : str(data[0].created_at),
            "updated_at" : str(data[0].updated_at)
        }
    else:
        all_users = []
        for data_point in data:
            adding_context = {
                "user_id" : data_point.id,
                "user_name" : data_point.user_name,
                "first_name" : data_point.first_name,
                "last_name" : data_point.last_name,
                "profile_pic_link" : data_point.profile_pic_link,
                "email" : data_point.email,
                "phone" : data_point.phone,
                "password" : data_point.password,
                "created_at" : str(data_point.created_at),
                "updated_at" : str(data_point.updated_at)
            }
            all_users.append(adding_context)
        context.update({"users" : all_users})
    return context

def jsonifyArtistData(data):
    context = {}
    if len(data) == 1:
        context = {
            "artist_id" : data[0].id,
            "user_name" : data[0].user_name,
            "first_name" : data[0].first_name,
            "last_name" : data[0].last_name,
            "profile_pic_link" : data[0].profile_pic_link,
            "header_pic_link": data[0].header_pic_link,
            "email" : data[0].email,
            "phone" : data[0].phone,
            "password" : data[0].password,
            "created_at" : str(data[0].created_at),
            "updated_at" : str(data[0].updated_at)
        }
    else:
        all_artists = []
        for data_point in data:
            adding_context = {
                "artist_id" : data_point.id,
                "user_name" : data_point.user_name,
                "first_name" : data_point.first_name,
                "last_name" : data_point.last_name,
                "profile_pic_link" : data_point.profile_pic_link,
                "header_pic_link": data_point.header_pic_link,
                "email" : data_point.email,
                "phone" : data_point.phone,
                "password" : data_point.password,
                "created_at" : str(data_point.created_at),
                "updated_at" : str(data_point.updated_at)
            }
            all_artists.append(adding_context)
        context.update({"artists" : all_artists})
    return context
