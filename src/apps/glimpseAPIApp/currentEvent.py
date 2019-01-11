from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import bcrypt, sys, os, base64, datetime, hashlib, hmac, pytz
import boto3, csv, json
import requests

# global currentEventId

# # Routing functions
def setCurrentEvent(request, event_id):
    request.session["currentEventId"] = event_id
    currentEventId = event_id
    return redirect('/adminPage')

# def getCurrentEventId():
#     return currentEventId

# currentEventId = getCurrentEventId()