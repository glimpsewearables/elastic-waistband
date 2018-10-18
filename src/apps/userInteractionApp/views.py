from django.shortcuts import render, HttpResponse
import bcrypt, sys, os, base64, datetime, hashlib, hmac 
import boto3, csv
from django.db import models
from .models import User, Device, Event, Media
client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
v1_raw_bucket = resource.Bucket('pi-1')
v1_edited_bucket = resource.Bucket('pi-2')
v2_raw_bucket = resource.Bucket('pi-4')
v2_edited_bucket = resource.Bucket('pi-5') 


# All of the endpoints for pushing information from the api call
# functions divider
# functions divider
# functions divider
def index():
    response = "from the userInteractionApp we are on the index"
    return HttpResponse(response)
def userPage(request, user_id):
    response = "from the userInteractionApp we are on the userPage"
    this_user = User.objects.get(id=user_id)
    return HttpResponse(this_user)
def createUser():
    print("creating a new user")
def updateUser():
    print("updating user")

# All of functions for creating users and managing user information

# functions divider
# functions divider
# functions divider

# def createUser(request):
#     if request.method=="POST":
#         errors = User.objects.basic_validator(request.POST)
#         if len(errors):
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/registerLoginPage', errors)
#         else:
#             imgCount = 0
#             vidCount = 0
#             device_number = request.POST['deviceNumber']
#             bucket_select = "user" + device_number
#             bucket_images = bucket_select + "/images"
#             bucket_videos = bucket_select + "/videos"
#             throw_images = bucket_images + "/"
#             throw_videos = bucket_videos + "/"
#             this_users_images = test_bucket.objects.filter(Prefix=bucket_images)
#             this_users_videos = test_bucket.objects.filter(Prefix=bucket_videos)
#             newEmail = request.POST['usersEmail']
#             print(newEmail.lower())
#             User.objects.create(full_name=request.POST['usersName'], email_address=newEmail.lower(), phone_number=request.POST['usersPhone'], number_pics = imgCount, number_vids = vidCount, device_key_name=request.POST['deviceNumber'])
#             last_user = User.objects.last()
#             request.session['user_id'] = last_user.id
#             Device.objects.create(device_owner = User.objects.get(device_key_name = device_number), device_key_name = "SerialNumber", number_pics = imgCount, number_vids = vidCount)
#             user_with_id = User.objects.get(id=request.session['user_id'])
#             return redirect('/userPage')
#     return redirect('/')
# def login(request):
#     if request.method == "POST":
#         errors = User.objects.login_validator(request.POST)
#         if len(errors):
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/registerLoginPage', errors)
#         checkEmail = request.POST['emailsLogin']
#         passEmail = checkEmail.lower()
#         if User.objects.filter(email_address=passEmail):
#             user = User.objects.get(email_address=passEmail)
#             if user.device_key_name == request.POST['deviceNumber']:
#                 request.session['user_id'] = user.id
#                 return redirect('/userPage')
#     return redirect('/')
# All of functions for creating events and managing event information

# functions divider
# functions divider
# functions divider

# def createEvent(request):
#     if isLoggedIn() == "false":
#         return redirect("")
#     if request.method == "POST":
#         errors = Event.objects.basic_validator(request.POST)
#         print(errors)
#         if len(errors):
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/godMode', errors)
#         else:
#             Event.objects.create(name=request.POST['eventName'], venue_name=request.POST['venueName'], address=request.POST['address'], start_date=request.POST['startDate'], end_date=request.POST['endDate'])
#     return redirect("/godMode")
