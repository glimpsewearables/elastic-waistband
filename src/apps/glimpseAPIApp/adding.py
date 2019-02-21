from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json
import urllib
import botocore
import requests
from django.db import models
from .models import User, UserEvent, Artist, ArtistEvent, Device, Event, Media, MediaComment

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
v1_raw_bucket = resource.Bucket('pi-1')
v1_edited_bucket = resource.Bucket('pi-2')
v2_raw_bucket = resource.Bucket('users-raw-content')
v2_edited_bucket = resource.Bucket('users-edited-content') 

# All s3 commands
def testS3Download(request):
    firstFile = Media.objects.first()
    urlLink = firstFile.link
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
    fileSplit = firstFile.link.split("https://s3-us-west-2.amazonaws.com/users-raw-content/")
    KEY = str(fileSplit[1])
    fileType = KEY[-4:]
    downloadTool = urllib.URLopener()
    filePath = desktop + "/" + KEY
    downloadTool.retrieve(urlLink, filePath)
    return HttpResponse(KEY)

def uploadMediaToS3(request):
    video = request.POST["uploadedVideo"]
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
    client.upload_file(desktop+"/"+video, "users-edited-content", video)
    user_id = request.POST["user_id"]
    event_id = request.POST["event_id"]
    device_id = request.POST["device_id"]
    thisEvent = Event.objects.get(id = event_id)
    Media.objects.create(
        user_id = user_id,
        event_id = event_id,
        device_id = device_id,
        featured = 1,
        media_type = "video",
        link = "https://s3-us-west-2.amazonaws.com/users-edited-content/" + video,
        raw_or_edited = "curated",
        ranking = 5,
        curator_rating = 5,
        user_rating = 3,
        date = thisEvent.start_date,
        date_time = "12:00"
    )
    return redirect("/adminPage")

# Initializing the database 
# Update database goes into s3 and checks to see if any links are in the s3 bucket but not in the sqlite database
# Only to be used once at the very beginning of launching the website to transfer all of the 
# existing files that are stored in the s3 database but not yet tracked in the sql database specific
# to the api that we are using
# Once the api is able to continually update the sql database every time an image is uploaded 
# this function will never have to be run again
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
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "ElasticWaistband",
            first_name = "Clayton",
            last_name = "Novotney",
            email = "clayton-novotney@hotmail.com",
            phone = "5094818244",
            password = "password",
            profile_pic_link = "https://s3-us-west-2.amazonaws.com/users-edited-content/profile_pics/user2_image_profile_ClaytonNovotney.jpg",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "TonyStark",
            first_name = "Dylan",
            last_name = "Rose",
            email = "drose@gmail.com",
            phone = "8473630989",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "CaptainMagma",
            first_name = "Keegan",
            last_name = "Jordan",
            email = "keeganbbjordan@gmail.com",
            phone = "2068522550",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "StarLord",
            first_name = "Achyuth",
            last_name = "Naidu",
            email = "ac@hotmail.com",
            phone = "2066175455",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "MissAppear",
            first_name = "Alexis",
            last_name = "Macaskill",
            email = "alexis9@uw.edu",
            phone = "3142625437",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "TheQuickster",
            first_name = "Kelson",
            last_name = "Flint",
            email = "Kelson.flint@gmail.com",
            phone = "2062062062",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "MermaidMan",
            first_name = "Michael",
            last_name = "Fernandez",
            email = "michael10@uw.edu",
            phone = "2064340881",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "HarryTheHusky",
            first_name = "Kyle",
            last_name = "Kusche",
            email = "kylerkusche@gmail.com",
            phone = "3609915429",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        User.objects.create(
            user_name = "PatrickStar",
            first_name = "Ronak",
            last_name = "Patel",
            email = "ronak0624@gmail.com",
            phone = "6505216699",
            password = "password",
            profile_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
    if (Artist.objects.filter(id = 1)):
        print("Initial Artist exists")
    else:
        Artist.objects.create(
            user_name = "GlimpseTesting",
            first_name = "Glimpse",
            last_name = "Wearables",
            email = "drose@glimpsewearables.com",
            phone = "5095095095",
            password = "password",
            profile_pic_link = "https://s3-us-west-2.amazonaws.com/users-edited-content/profile_pics/user1_image_profile_GlimpseCam.jpg",
            header_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        ArtistEvent.objects.create(
            artist_id = 1,
            event_id = 1
        )
        Artist.objects.create(
            user_name = "LouisTheChild",
            first_name = "Louis",
            last_name = "TheChild",
            email = "louisTheChild@gmail.com",
            phone = "5095095095",
            password = "password",
            profile_pic_link = "",
            header_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        ArtistEvent.objects.create(
            artist_id = 2,
            event_id = 3
        )
        Artist.objects.create(
            user_name = "AlanWalker",
            first_name = "Alan",
            last_name = "Walker",
            email = "alanWalker@gmail.com",
            phone = "5095095095",
            password = "password",
            profile_pic_link = "",
            header_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        ArtistEvent.objects.create(
            artist_id = 3,
            event_id = 4
        )
        Artist.objects.create(
            user_name = "TwoFriends",
            first_name = "Two",
            last_name = "Friends",
            email = "TwoFriends@gmail.com",
            phone = "5095095095",
            password = "password",
            profile_pic_link = "",
            header_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        ArtistEvent.objects.create(
            artist_id = 4,
            event_id = 5
        )
        Artist.objects.create(
            user_name = "HippieSabotage",
            first_name = "Hippie",
            last_name = "Sabotage",
            email = "HippieSabotage@gmail.com",
            phone = "5095095095",
            password = "password",
            profile_pic_link = "",
            header_pic_link = "",
            created_at = datetime.time,
            updated_at = datetime.time
        )
        ArtistEvent.objects.create(
            artist_id = 5,
            event_id = 6
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
            start_date = "2018-06-20",
            end_date = "2018-07-20",
            start_time = "12:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event1_header_Seattle.jpg"
        )
        Event.objects.create(
            name = "Bumbershoot Festival",
            event_id = 2,
            lat = 47.6062,
            long = 122.3321,
            address = "Seattle City Center",
            start_date = "2018-08-31",
            end_date = "2018-09-03",
            start_time = "12:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event2_header_BumbershootFestival.jpg"
        )
        Event.objects.create(
            name = "Louis The Child",
            event_id = 3,
            lat = 47.594971,
            long = -122.331520,
            address = "WaMu Theatre, 800 Occidental Ave S, Seattle, WA 98134",
            start_date = "2018-12-01",
            end_date = "2018-12-01",
            start_time = "19:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event3_header_LouisTheChild.jpg"
        )
        Event.objects.create(
            name = "Alan Walker",
            event_id = 4,
            lat = 47.587894,
            long = -122.333717,
            address = "ShowBox Sodo, 1700 1st Ave S, Seattle, WA 98134",
            start_date = "2019-02-02",
            end_date = "2019-02-02",
            start_time = "19:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event4_header_AlanWalker.jpg"
        )
        Event.objects.create(
            name = "Two Friends",
            event_id = 5,
            lat = 47.613959,
            long = -122.319574,
            address = "Neumos, 925 East Pike Street, Seattle, WA 98122",
            start_date = "2019-02-07",
            end_date = "2019-02-07",
            start_time = "20:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event5_header_TwoFriends.jpg"
        )
        Event.objects.create(
            name = "Hippie Sabotage",
            event_id = 6,
            lat = 47.6133,
            long = -122.3313,
            address = "Paramount Theatre, 911 Pine St, Seattle, WA 98101",
            start_date = "2019-02-09",
            end_date = "2019-02-09",
            start_time = "20:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event6_header_HippieSabotage.jpg"
        )
        Event.objects.create(
            name = "LollaPalooza",
            event_id = 7,
            lat = 41.8742,
            long = 87.6208,
            address = "Grant Park, Chicago",
            start_date = "2018-08-02",
            end_date = "2018-08-05",
            start_time = "12:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event7_header_LollaPalooza.png"
        )
        Event.objects.create(
            name = "Sound Off",
            event_id = 8,
            lat = 41.8742,
            long = 87.6208,
            address = "Seattle, WA",
            start_date = "2019-02-16",
            end_date = "2019-02-17",
            start_time = "12:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event7_header_LollaPalooza.png"
        )
        Event.objects.create(
            name = "Boogie T",
            event_id = 9,
            lat = 41.8742,
            long = 87.6208,
            address = "Seattle, WA",
            start_date = "2019-02-17",
            end_date = "2019-02-18",
            start_time = "12:00:00",
            header_image = "https://s3-us-west-2.amazonaws.com/users-edited-content/headerImages/event7_header_LollaPalooza.png"
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
            allEvents = Event.objects.all()
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

            event_id = checkEvent(dateOf)
            # if dateOf == "2018-12-01":
            #     event_id = 3
            # elif dateOf =="2018-08-31" or dateOf == "2018-09-01" or dateOf =="2018-09-02":
            #     event_id = 2
            # elif dateOf == "2019-02-02":
            #     event_id = 4
            # elif dateOf == "2019-02-07":
            #     event_id = 5
            # elif dateOf == "2019-02-09":
            #     event_id = 6
            # elif dateOf == "2018-08-02" or dateOf == "2018-08-03" or dateOf =="2018-08-04" or dateOf == "2018-08-05":
            #     event_id = 7
            # elif dateOf == "2019-02-16" or dateOf == "2019-02-17":
            #     event_id = 8
            # elif dateOf == "2019-02-18":
            #     event_id = 9
        # If else statement that helps decide whether or not this media type is a image or video
            if (not UserEvent.objects.filter(user_id = userId, event_id = event_id)) and event_id != 1 and event_id != 0:
                UserEvent.objects.create(
                    user_id = userId,
                    event_id = event_id,
                    device_used_id = userId
                )
            Media.objects.create(
                user_id = int(userId),
                device_id = int(userId),
                event_id = event_id,
                media_type = media_type,
                featured = 0,
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
        elif "headerImages" in data.key:
            print("This is a header Image")
        elif "profile_pics" in data.key: 
            print("This is a Profile Picture")
        else:
            splitLink = data.key.split("_")
            if "user" in splitLink:
                userId = ""
                media_type = ""
                dateOf = ""
                dateTimeOf = ""
                event_id = 1
                raw_or_edited = "edited"
                for part in splitLink:
                    if part.startswith("user"):
                        newPart = part.split("user")
                        userId = newPart[1]
                    elif part == "image" or part == "video":
                        media_type = part
                    elif part == "profile" or part == "header":
                        raw_or_edited = part
                    elif part.startswith("201"):
                        dateOf = part
                    elif part.endswith(".jpg") or part.endswith(".jpeg"):
                        endingPart = part.split(".jpg")
                        dateTimeOf = endingPart[0]
                    elif part.endswith(".mp4"):
                        endingPart = part.split(".mp4")
                        dateTimeOf = endingPart[0]
                # If else statement that helps decide whether or not this media type is a image or video
                event_id = checkEvent(dateOf)
                # if dateOf =="2018-08-31" or dateOf == "2018-09-01" or dateOf =="2018-09-02":
                #     event_id = 2
                # elif dateOf == "2018-12-01":
                #     event_id = 3
                # elif dateOf =="2019-02-02":
                #     event_id = 4
                # elif dateOf =="2019-02-07":
                #     event_id = 5
                # elif dateOf =="2019-02-09":
                #     event_id = 6
                # elif dateOf == "2018-08-02" or dateOf == "2018-08-03" or dateOf =="2018-08-04" or dateOf == "2018-08-05":
                #     event_id = 7
                # elif dateOf == "2019-02-16" or dateOf == "2019-02-17":
                #     event_id = 8
                # elif dateOf == "2019-02-18":
                #     event_id = 9
                Media.objects.create(
                    user_id = int(userId),
                    device_id = int(userId),
                    event_id = event_id,
                    media_type = media_type,
                    featured = 0,
                    link = "https://s3-us-west-2.amazonaws.com/users-edited-content/" + data.key,
                    raw_or_edited = raw_or_edited,
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

def checkEvent(this_date):
    this_event_id = 1
    all_events = Event.objects.all()
    for event in all_events:
        if str(event.start_date) == str(this_date) or str(event.end_date) == str(this_date):
            return event.event_id
    return this_event_id

# All internal commands
def registerUser(request):
    if request.POST:
        createNewUser(request, request.POST["usersName"], request.POST["firstName"], request.POST["lastName"], request.POST["usersEmail"], request.POST["password"], request.POST["usersPhone"])
        request.session["userType"] = "user"
        request.session["deviceNumber"] = request.POST["deviceNumber"]
        return redirect("/userPage/" + str(request.POST["deviceNumber"]))
    else: 
        return redirect("/")

def createUser(request):
    if request.POST:
        if request.session["userType"] != "masterAdmin" and request.session["userType"] != "userTestingAdmin" and request.session["userType"] != "curatorAdmin":
            return redirect("/")
        else:
            createNewUser(request, request.POST["usersName"], request.POST["firstName"], request.POST["lastName"], request.POST["usersEmail"], request.POST["password"], request.POST["usersPhone"] )
    return redirect("/adminPage")

def createEvent(request):
    if request.POST:
        if request.session["userType"] != "masterAdmin" and request.session["userType"] != "userTestingAdmin" and request.session["userType"] != "curatorAdmin":
            return redirect("/")
        else:
            now = datetime.date.today()
            Event.objects.create(
                event_id = request.POST["eventId"],
                name = request.POST["eventName"],
                address = request.POST["address"],
                start_date = request.POST["startDate"],
                end_date = request.POST["endDate"],
                long = 0.00,
                lat = 0.00,
                created_at = now,
                updated_at = now,
                header_image = request.POST["imageHeader"]
            )
    return redirect("/curatorPortal")

def createMedia(request):
    if request.POST:
        if request.session["userType"] != "masterAdmin" and request.session["userType"] != "curatorAdmin" and request.session["userType"] != "userTestingAdmin":
            return redirect("/")
        else:
            createNewMedia(request, request.POST["url_link"], request.POST["device_id"], request.POST["event_id"])
            return redirect("/adminPage")

def createDevice(request):
    if request.POST:
        if request.session["userType"] != "masterAdmin" and request.session["userType"] != "deviceAdmin":
            return redirect("/")
        else:
            createNewDevice(request, request.POST["device_number"], request.POST["user_id"], request.POST["serial_number"])
    return redirect("/adminPage")

def deleteUser(request, user_id):
    if request.session["userType"] != "masterAdmin" and request.session["userType"] != "userTestingAdmin":
        return redirect("/")
    else:
        User.objects.get(id = user_id).delete()
        return redirect("/adminPage")

def deleteEvent(request, event_id):
    if request.session["userType"] != "masterAdmin" and request.session["userType"] != "userTestingAdmin":
        return redirect("/")
    else:
        Event.objects.get(id = event_id).delete()
        return redirect("/adminPage")

def deleteDevice(request, device_id):
    if request.session["userType"] != "masterAdmin" and request.session["userType"] != "deviceAdmin":
        return redirect("/")
    else:
        Device.objects.get(id = device_id).delete()
        return redirect("/adminPage")

#  Creation functions
def createNewDevice(deviceNum, userId, serialNumber):
    now = datetime.date.today()
    Device.objects.create(
        user_id = userId,
        device_number = deviceNum,
        serial_number = serialNumber,
        created_at = now,
        updated_at = now
    )

def createNewUser(request, user_name, first_name, last_name, email, password, phone):
    User.objects.create(
        user_name = user_name,
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone = phone,
        password = password,
        created_at = datetime.date.today(),
        updated_at = datetime.date.today()
    )

def createNewMedia(request, url_link, device_id, event_id):
    if request.session["userType"] != "admin":
        return redirect("/")
    else:
        now = datetime.datetime.now(pytz.timezone('US/Pacific'))
        Media.objects.create(
            user_id = device_id,
            device_id = device_id,
            event_id = event_id,
            media_type = "video",
            link = url_link,
            raw_or_edited = "raw",
            downloaded = 0,
            ranking = 1,
            created_at = now,
            updated_at = now,
            gif_link = "",
            views = 0,
            starred = 0,
            date = datetime.date.today(),
            date_time = datetime.datetime.now().time()
        )
