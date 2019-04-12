import os
import boto3, csv, json
import urllib2
import botocore
from os import listdir
from moviepy.editor import *

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
v1_raw_bucket = resource.Bucket('pi-1')
v1_edited_bucket = resource.Bucket('pi-2')
v2_raw_bucket = resource.Bucket('users-raw-content')
v2_edited_bucket = resource.Bucket('users-edited-content')

# s3_connection = boto.connect_s3()
# bucket = s3_connection.get_bucket('users-edited-content')

def gifMultipleVideos():
	desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
	gifFilePath = desktop + "/gifingVideos"
	alreadyGifedPath = gifFilePath + "/alreadyGifed"
	toGifPath = gifFilePath + "/toGif"
	files = os.listdir(toGifPath)
	files.sort()
	print(files)
	for idx, file in enumerate(files):
		clip = VideoFileClip(toGifPath + "/" + file) 
		start = 5.0
		end = 7.0
		if (clip.duration < 5):
			start = 0.0
			end = clip.duration
		clip = (clip.subclip((0,start),(0,end)).resize(0.3))
		clip.write_gif(alreadyGifedPath + "/mediaId_ (%d).gif" % (idx + 50))

def gifSingleVideo(fileName):
	desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
	gifFilePath = desktop + "/gifingVideos"
	alreadyGifedPath = gifFilePath + "/alreadyGifed"
	toGifPath = gifFilePath + "/toGif"
	clip = VideoFileClip(toGifPath + "/" + fileName) 
	start = 5.0
	end = 7.0
	if (clip.duration < 5):
		start = 0.0
		end = clip.duration
	clip = (clip.subclip((0,start),(0,end)).resize(0.3))
	newFileName = fileName.split(".")
	firstBit = newFileName[0]
	secondBit = newFileName[1]
	clip.write_gif(alreadyGifedPath + "/" + firstBit + ".gif")
	lastGif = alreadyGifedPath + "/" + firstBit + ".gif" 
	v2_edited_bucket.upload_file(lastGif, "newGifs/"+ firstBit + ".gif")
	print("gif sent")
	# key = boto.s3.key.Key(bucket, file)
	# with open('some_file.zip') as f:
	# 	key.send_file(f)


def getAllLinksFromS3():
	allKeyNames = []
	for i in iterate_bucket_items(bucket='users-raw-content'):
		if i["Key"].endswith(".mp4"):
			allKeyNames.append(i["Key"])
	return allKeyNames

def iterate_bucket_items(bucket):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket)
    for page in page_iterator:
        if page['KeyCount'] > 0:
            for item in page['Contents']:
                yield item

def downloadFromS3():
	desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
	gifFilePath = desktop + "/gifingVideos"
	alreadyGifedPath = gifFilePath + "/alreadyGifed"
	toGifPath = gifFilePath + "/toGif"
	allKeys = getAllLinksFromS3()
	baseUrl = "https://s3-us-west-2.amazonaws.com/users-raw-content/"
	# for i in range(0, len(allLinks)):
	for i in range(0, 10):
		print(allKeys[i])
		urllib.request.urlretrieve(baseUrl + allKeys[i], toGifPath + "/" + allKeys[i])
		gifSingleVideo(allKeys[i])


downloadFromS3()

def previousWork():
	files = os.listdir("videos/")
	files.sort()
	for idx, file in enumerate(files):
		clip = VideoFileClip("videos/" + file) 
		start = 5.0
		end = 7.0
		if (clip.duration < 5):
			start = 0.0
			end = clip.duration
		clip = (clip.subclip((0,start),(0,end)).resize(0.3))
		clip.write_gif("gifs/ezgif.com-crop (%d).gif" % (idx + 50))