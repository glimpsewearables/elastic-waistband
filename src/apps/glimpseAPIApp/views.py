from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json, wget, inspect, urllib, tinys3
import requests
from django.db import models
from .models import User, Device, Event, Media, MediaComment
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
    # return redirect('/adminPage')

# def downloadCsv(request):



def updateDatabase(request):
    request.session["currentEventId"] = 1
    thisUsersContentRaw = v2_raw_bucket.objects.filter()
    thisUsersContentEdited = v2_edited_bucket.objects.filter()
    if (User.objects.filter(id = 1)):
        print("Initial User exists")
    else:
        User.objects.create(
            user_name = "glimpseTesting",
            first_name = "glimpse",
            last_name = "project",
            email = "drose@glimpsewearables.com",
            phone = "5094818244",
            password = "password",
            created_at = datetime.time,
            updated_at = datetime.time
        )
    if(Device.objects.filter(id = 2)):
        print("Inital Device exists")
    else:
        for i in range (1, 10):
            Device.objects.create(
                device_number = i,
                serial_number = str(i) + "a" + str(i) + "b" + str(i) + "c",
                user_id = i
            )
    if(Event.objects.filter(id = 1)):
        print("Inital Event in database exists")
    else:
        Event.objects.create(
            name = "Glimpse Testing",
            event_id = 1,
            lat = 47.6062,
            long = 122.3321,
            address = "4637 21st Ave NE",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/seattle.jpg"
        )
        Event.objects.create(
            name = "Bumbershoot Festival",
            event_id = 2,
            lat = 47.6062,
            long = 122.3321,
            address = "Seattle City Center",
            start_date = "2018-08-31",
            end_date = "2018-09-03",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/bumbershoot-festival.jpg"
        )
        Event.objects.create(
            name = "Louis The Child",
            event_id = 3,
            lat = 47.6062,
            long = 122.3321,
            address = "Seattle City Center",
            start_date = "2018-12-01",
            end_date = "2018-12-01",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/louisTheChildHeaderImage.jpg"
        )
    # This function is the most important for updating the database, checking to see if all of the images
    # that are in the s3 database are accounted for in the sql database
    for data in thisUsersContentRaw:
        urlHeader = "https://s3-us-west-2.amazonaws.com/users-raw-content/"
        linkCheck = urlHeader + data.key
        if Media.objects.filter(link = linkCheck):
            print(data.key + "data.key already exists")
        elif not data.key.endswith(".jpg") and not data.key.endswith(".mp4"):
            print("data key is not a proper link")
        else:
            splitLink = data.key.split("_")
            userId = 0
            media_type = "neither"
            dateOf = "not given"
            dateTimeOf = "not given"
            event_id = 1
            for part in splitLink:
                if part.startswith("user"):
                    newPart = part.split("user")
                    userId = newPart[1]
                elif part == "image" or part == "video":
                    media_type = part
                elif part.startswith("201"):
                    dateOf = part
                elif part.endswith(".jpg") or part.endswith(".jpeg"):
                    endingPart = part.split(".jpg")
                    dateTimeOf = endingPart[0]
                elif part.endswith(".mp4"):
                    endingPart = part.split(".mp4")
                    dateTimeOf = endingPart[0]
            if dateOf == "2018-12-01":
                event_id = 3
            elif dateOf =="2018-08-31" or dateOf == "2018-09-01" or dateOf =="2018-09-02":
                event_id = 2
        # If else statement that helps decide whether or not this media type is a image or video
            Media.objects.create(
                user_id = int(userId),
                device_id = int(userId),
                event_id = event_id,
                media_type = media_type,
                link = "https://s3-us-west-2.amazonaws.com/users-raw-content/" + data.key,
                raw_or_edited = "raw",
                downloaded = 0,
                ranking = 1,
                created_at = datetime.datetime.now(),
                updated_at = datetime.datetime.now(),
                gif_link = "",
                views = 0,
                starred = 0,
                date = dateOf,
                date_time = dateTimeOf
            )
    # This function is the most important for updating the database, checking to see if all of the images
    # that are in the s3 database are accounted for in the sql database
    for data in thisUsersContentEdited:
        urlHeader = "https://s3-us-west-2.amazonaws.com/users-edited-content/"
        linkCheck = urlHeader + data.key
        if Media.objects.filter(link = linkCheck):
            print(data.key + "data.key already exists")
        elif not data.key.endswith(".jpg") and not data.key.endswith(".mp4"):
            print("data key is not a proper link")
        else:
            splitLink = data.key.split("_")
            if "user" in splitLink:
                userId = ""
                media_type = ""
                dateOf = ""
                dateTimeOf = ""
                event_id = 1
                for part in splitLink:
                    if part.startswith("user"):
                        newPart = part.split("user")
                        userId = newPart[1]
                    elif part == "image" or part == "video":
                        media_type = part
                    elif part.startswith("201"):
                        dateOf = part
                    elif part.endswith(".jpg") or part.endswith(".jpeg"):
                        endingPart = part.split(".jpg")
                        dateTimeOf = endingPart[0]
                    elif part.endswith(".mp4"):
                        endingPart = part.split(".mp4")
                        dateTimeOf = endingPart[0]
                # If else statement that helps decide whether or not this media type is a image or video
                if dateOf == "2018-12-01":
                    event_id = 3
                elif dateOf =="2018-08-31" or dateOf == "2018-09-01" or dateOf =="2018-09-02":
                    event_id = 2
                Media.objects.create(
                    user_id = int(userId),
                    device_id = int(userId),
                    event_id = event_id,
                    media_type = media_type,
                    link = "https://s3-us-west-2.amazonaws.com/users-edited-content/" + data.key,
                    raw_or_edited = "edited",
                    downloaded = 0,
                    ranking = 1,
                    created_at = datetime.datetime.now(),
                    updated_at = datetime.datetime.now(),
                    gif_link = "",
                    views = 0,
                    starred = 0,
                    date = dateOf,
                    date_time = dateTimeOf
                )
    return HttpResponse(thisUsersContentRaw)

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
            print newLink + " is the new link"
        else:
            print "good link"
    return redirect("/")

def removeDuplicates(request):
    allMedia =  Media.objects.all()
    for media in allMedia:
        if allMedia.filter(link = media.link):
            print "duplicate"
        else:
            print "not a duplicate"
    return redirect("/")

def logout(request):
    request.session["userType"] = None
    request.session["deviceNumber"] = None
    return redirect("/")
# All of the endpoints for retrieving information from the api call
def mediaHome(request):
    response = "here is the home page from the media application portion of the api"
    return HttpResponse(response)

def getAllImages(request): # grabs ALL images that are being stored in the raw bucket
    context = {}
    all_images = Media.objects.filter(media_type = "image")
    json_images = jsonifyMediaData(all_images)
    newContext = json.dumps(json_images)
    return HttpResponse(newContext, content_type="application/json")
    # return json(json_images)

def getAllVideos(request): # grabs ALL videos that are being stored in the raw bucket
    context = {}
    all_videos = Media.objects.filter(media_type = "video")
    json_videos = jsonifyMediaData(all_videos)
    newContext = json.dumps(json_videos)
    return HttpResponse(newContext, content_type="application/json")

def getAllUserMedia(request, userId): # grabs ALL images connected to the specific user that are being stored in the raw bucket
    context = {}
    if User.objects.filter(id = userId):
        response = "Getting all media specific to user " + userId + "..!! "
        raw_media = Media.objects.filter(user_id = userId, raw_or_edited = "raw")
        edited_media = Media.objects.filter(user_id= userId, raw_or_edited = "edited")
        json_raw_media = jsonifyMediaData(raw_media)
        json_edited_media = jsonifyMediaData(edited_media)
        context["raw_media"] = json_raw_media
        context["edited_media"] = json_edited_media
    else:
        context["error"] = "You entered a user that does not exist"
    newContext = json.dumps(context)
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
    if Event.objects.filter(id = eventId) and Device.objects.filter(id = userId):
        response = "Getting all videos for a single user at a specific event with a event id of" + eventId
        user_event_videos = Media.objects.filter(event_id = eventId, user_id = userId, media_type="video")
        json_user_event_videos = jsonifyMediaData(user_event_videos)
        context["user_event_videos"] = json_user_event_videos
    else:
        context["error"] = "You entered a user or event that does not exist"
    return HttpResponse(json.dumps(context), content_type="application/json")

# all of the endpoint functions for retrieving event information
def getAllEvents(request): # grabs ALL events from mysql database
    response = "Getting all events that have been created"
    context = {}
    all_events = Event.objects.all()
    all_images = Media.objects.filter(media_type = "image")
    all_videos = Media.objects.filter(media_type = "video")
    context["all_events"] = jsonifyEventData(all_events)
    context["all_images"] = jsonifyMediaData(all_images)
    context["all_videos"] = jsonifyMediaData(all_videos)
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificEvent(request, eventId): # grabs a specific event from the mySQL database
    context = {}
    newContext = {}
    if Event.objects.filter(id = eventId):
        response = "Getting a single specific event with a event id of"
        this_event = Event.objects.get(id = eventId)
        this_event_content = Media.objects.filter(event_id = eventId)
        context["this_event"] = jsonifyEventData(this_event)
        context["this_event_content"] = jsonifyMediaData(this_event_content)
        newContext = json.dumps(context)
    else:
        newContext["error"] = "You entered a event that does not exist"
    return HttpResponse(newContext, content_type="application/json")

# all of the endpoint functions for retrieving device information
def getAllDevices(request): # grabs a specific user from the mySQL database
    all_devices = Device.objects.all()
    context = jsonifyDeviceData(all_devices)
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificDevice(request, device_id): # grabs all users from the mySQL database
    context = {}
    if Device.objects.filter(id = device_id):
        this_device = User.objects.filter(id=device_id)
        context = jsonifyUserData(this_device)
    else:
        context["error"] = "You entered a device that does not exist"
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

# all of the endpoint functions for retrieving user information
def getAllUsers(request): # grabs a specific user from the mySQL database
    all_users = User.objects.all()
    context = jsonifyUserData(all_users)
    newContext = json.dumps(context)
    return HttpResponse(newContext, content_type="application/json")

def getSpecificUser(request, user_id): # grabs all users from the mySQL database
    context = {}
    if User.objects.filter(id = user_id):
        this_user = User.objects.filter(id=user_id)
        context = jsonifyUserData(this_user)
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

# Converting the object based data into json data that can be parsed and returned by the api
def jsonifyMediaData(data):
    context = {}
    all_media = []
    for data_point in data:
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
        all_media.append(adding_context)
    context.update({"media" : all_media})
    return context

def jsonifyEventData(data_point):
    adding_context = {
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
    return adding_context

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

def jsonifyUserData(data):
    context = {}
    all_users = []
    for data_point in data:
        adding_context = {
            "user_name" : data_point.user_name,
            "first_name" : data_point.first_name,
            "last_name" : data_point.last_name,
            "email" : data_point.email,
            "phone" : data_point.phone,
            "password" : data_point.password,
            "created_at" : str(data_point.created_at),
            "updated_at" : str(data_point.updated_at)
        }
        all_users.append(adding_context)
    context.update({"users" : all_users})
    return context
