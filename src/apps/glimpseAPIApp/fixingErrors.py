from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz, requests, datetime, json
from django.db import models

from .models import Event, Media

base_url = "https://api.glimpsewearables.com/api/media/"

def fixErrors():
    head =  {"Content-type":"application/json"}
    for i in range(first_num, last_num):
        new_url = base_url + str(i) + "/"
        payload = {'event_id' : 9}
        new_payload = json.dumps(payload)
        r = requests.patch(new_url, new_payload, headers = head)
        print(r)
def fixEvents():
    allMedia = Media.objects.all()
    allEvents = Event.objects.all()
    for media in allMedia:
        if media.date == "2019-02-17" or media.date == "2019-02-18":
            print("Boogie T")
# fixErrors()
# fixEvents()

def partitionVideos(request):
        context = {}
        context["event"] = Event.objects.get(id = 3)
        devicesAttending = getDevices(request, 3)
        context["devices_attending"] = devicesAttending
        allSections = {}
        for device in devicesAttending:
                thisMedia = Media.objects.filter(event_id = 3, media_type = "video", device_id = device)
                totalMedia = len(thisMedia)
                sectionNumber = 0
                sectionTracker = totalMedia
                sections = {}
                print(totalMedia)
                while sectionTracker >= 0:
                        sections["section" + str(sectionNumber)] = []
                        sectionTracker -= 20
                        sectionNumber += 1
                allSections["device" + str(device)] = sections
                section = 0
                vidTracker = 0
                for video in thisMedia:
                        thisSection = "section" + str(section)
                        allSections["device" + str(device)]["section" + str(section)].append(video)
                        if vidTracker - 20 == 0:
                                vidTracker = 0
                                section+=1
                        vidTracker+=1
        context["allSections"] = allSections
        # eventTwoMedia = Media.objects.filter(event_id = 3, media_type = "video")
        # sections = {}
        # numMedia = len(eventTwoMedia)
        # sectionNumber = 0
        # sectionTracker = numMedia
        # while sectionTracker >= 0:
        #         sections["section" + str(sectionNumber)] = []
        #         sectionTracker -= 30
        #         sectionNumber += 1
        # context["sections"] = sections
        # for section in sections:
        #         context[section] = []
        # section = 0
        # vidTracker = 0
        # for video in eventTwoMedia:
        #         thisSection = "section" + str(section)
        #         sections.get(thisSection).append(video)
        #         context["section" + str(section)].append(video)
        #         if vidTracker - 30 == 0:
        #                 vidTracker = 0
        #                 section+=1
        #         vidTracker+=1
        return render(request, "testing.html", context)

def getDevices(request, event_id):
        thisEventMedia = Media.objects.filter(event_id = event_id, media_type = "video")
        devicesAttending = []
        for media in thisEventMedia:
                if media.device_id not in devicesAttending:
                        devicesAttending.append(media.device_id)
        return devicesAttending
