from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json
import requests

currentEventId = None

# def initCurrentEventId(request):
    # global currentEventId
    # if currentEventId is None:
    #     currentEventId = 13
    # else:
    #     currentEventId = getCurrentEventId



# # Routing functions
def setCurrentEvent(request, event_id):
    global currentEventId
    request.session["currentEventId"] = event_id
    currentEventId = event_id
    return redirect('/adminPage')

def getCurrentEventId(request):
    global currentEventId
    if not request.session["currentEventId"]:
        request.session["currentEventId"] = 0
    return currentEventId

# currentEventId = getCurrentEventId()