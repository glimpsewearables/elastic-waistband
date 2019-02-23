from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz, requests, datetime, json
from django.db import models

from .models import Event, Media

base_url = "https://api.glimpsewearables.com/api/media/"
first_num = 727
last_num = 910

def fixErrors():
    head =  {"Content-type":"application/json"}
    for i in range(first_num, last_num):
        new_url = base_url + str(i) + "/"
        payload = {'event_id' : 9}
        new_payload = json.dumps(payload)
        r = requests.patch(new_url, new_payload, headers = head)
        print r
def fixEvents():
    allMedia = Media.objects.all()
    allEvents = Event.objects.all()
    for media in allMedia:
        if media.date == "2019-02-17" or media.date == "2019-02-18":
            print "Boogie T"
# fixErrors()
fixEvents()