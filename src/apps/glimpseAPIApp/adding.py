from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json
import requests
from django.db import models
from .models import User, Device, Event, Media, MediaComment

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
        if request.session["userType"] != "admin":
            return redirect("/")
        else:
            createNewUser(request, request.POST["usersName"], request.POST["firstName"], request.POST["lastName"], request.POST["usersEmail"], request.POST["password"], request.POST["usersPhone"] )
    return redirect("/adminPage")

def createEvent(request):
    if request.POST:
        if request.session["userType"] != "admin":
            return redirect("/")
        else:
            createNewEvent(request, request.POST["eventName"], request.POST["address"], request.POST["startDate"], request.POST["endDate"], request.POST["imageHeader"])
    return redirect("/adminPage")

def createMedia(request):
    if request.POST:
        if request.session["userType"] != "admin":
            return redirect("/")
        else:
            createNewMedia(request, request.POST["url_link"], request.POST["device_id"], request.POST["event_id"])
            return redirect("/adminPage")

def createDevice(request):
    if request.POST:
        if request.session["userType"] != "admin":
            return redirect("/")
        else:
            createNewDevice(request, request.POST["device_number"], request.POST["user_id"], request.POST["serial_number"])
    return redirect("/adminPage")

def deleteUser(request, user_id):
    if request.session["userType"] != "admin":
        return redirect("/")
    else:
        User.objects.get(id = user_id).delete()
        return redirect("/adminPage")

def deleteEvent(request, event_id):
    if request.session["userType"] != "admin":
        return redirect("/")
    else:
        Event.objects.get(id = event_id).delete()
        return redirect("/adminPage")

def deleteDevice(request, device_id):
    if request.session["userType"] != "admin":
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

def createNewEvent(request, name, address, start_date, end_date, image_header):
    if request.session["userType"] != "admin":
        return redirect("/")
    else:
        now = datetime.date.today()
        Event.objects.create(
            name = name,
            address = address,
            start_date = start_date,
            end_date = end_date,
            long = 0.00,
            lat = 0.00,
            created_at = now,
            updated_at = now,
            image_header = image_header
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
