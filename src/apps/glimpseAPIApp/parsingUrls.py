import boto3, csv, json
import requests, datetime
from django.db import models
from .models import User, Device, Event, Media, MediaComment

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
v1_raw_bucket = resource.Bucket('pi-1')
v1_edited_bucket = resource.Bucket('pi-2')
v2_raw_bucket = resource.Bucket('users-raw-content')
v2_edited_bucket = resource.Bucket('users-edited-content') 

def fromDatabase():
    myFile = open('export.csv', 'w') 
    allMedia = Media.objects.all()
    with myFile:  
        myFields = ['views', 'starred', 'link', 'user_id', 'device_id', 'event_id', 'media_type', 'raw_or_edited', 'downloaded', 'ranking', 'date', 'date_time', 'created_at', 'updated_at', 'gif_link']
        for data_point in allMedia:
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
            writer.writerow(adding_context)

fromDatabase()
    


def fromS3():
    raw_content = v2_raw_bucket.objects.filter()
    edited_content = v2_edited_bucket.objects.filter()
    for media in raw_content:
        splitLink = media.key.split("_")
        userId = ""
        media_type = ""
        date = ""
        dateTimeOf = ""
        for part in splitLink:
            if part.startswith("user"):
                newPart = part.split("user")
                userId = newPart[1]
            elif part == "image" or part == "video":
                media_type = part
            elif part.startswith("201"):
                date = part
            elif part.endswith(".jpg") or part.endswith(".jpeg"):
                endingPart = part.split(".jpg")
                dateTimeOf = endingPart[0]
            elif part.endswith(".mp4"):
                endingPart = part.split(".mp4")
                dateTimeOf = endingPart[0]
        
        print " the user id is " + userId + ". With a media_type of " + media_type + ". Date is " + date + ", time of " + dateTimeOf

# fromS3()

# def checkDateTime():
#     now = datetime.datetime.now().time()
#     today = datetime.date.today()
#     print now
# checkDateTime()