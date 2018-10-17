API for services in GlimpseWearables
## Reading to do
https://stackoverflow.com/questions/8634473/sending-json-request-with-python

The current urls will return the content as described in a json file
#API functionality with put/post/get/delete/patch requests

## Using "get" as the HTTP Response will allow you to simply return the json files as seen below
### GET "api/user/" => returns all of the users in the database
### GET "api/user/{{user_id_of_desired_user}}/" => returns the user with that device id from the database
### GET "api/media/" => returns all of the media in the database
### GET "api/media/{{media_id_of_desired_media}}/" => returns the media with that media id from the database
### GET "api/device/" => returns all of the devices in the database
### GET "api/device/{{device_id_of_desired_device}}/" => returns the device with that device id from the database
### GET "api/event/" => returns all of the events in the database
### GET "api/event/{{event_id_of_desired_event}}/" => returns the event with that event id from the database

## Using "post" as the HTTP Response will allow you to create a new piece of data in the database as long as you follow the proper json syntax for the data
####
##### Make sure you include the "/" at the end of each post/patch/put url, otherwise the django framework will see this as routing and won't post any information
###### Use POST request to create a new object being stored in the database
###### Use PUT request to update an already existing object in the database
### POST/PUT "api/user/" => 
{
    "email": "{{Desired email of user}}",
    "first_name": "{{Desired first name of user}}",
    "last_name": "{{Desired last name of user}}",
    "password": "{{Desired password of user}}",
    "phone": "{{Desired phone number of user}}"
}
### POST/PUT "api/event/" => 
{
    "name": "{{Desired name of event}}",
    "address": "{{Desired address of event}}",
    "end_date": "{{Desired end_date of event}}",
    "start_date": "{{Desired start_date of event}}",
    "lat": "{{Desired latitude of event}}",
    "long": "{{Desired longitude of event}}"
}
### POST/PUT "api/media/" => 
{
    "link": "{{name of the media that is stored in the s3 data}",
    "media_type": "{{image or video}}",
    "ranking": "{{Desired ranking of the media}}",
    "raw_or_edited" : {{Whether or not the image has been edited or not}}",
    "downloaded" : "{{0 means not downloaded, 1 means downloaded}}",
}
### POST/PUT "api/device/" => 
{
    "device_number" : "{{device number of device}}",
    "serial_number" : "{{serial number of the device}}"
}

#All of the following routes return a specific type of data from the database
## **""** => 
returns nothing, a loading page telling you to enter a proper url as an endpoint
## **"media"** => 
returns nothing, a loading page telling you to enter a proper url as an endpoint
## **"media/getAllImages"** => 
grabs ALL images that are being stored in the raw bucket
## **"media/getAllVideos"** => 
grabs ALL videos that are being stored in the raw bucket
## **"media/getAllUserImages/{{user_id_of_who_you_want_to_grab}}"** => 
grabs ALL images that are being stored in the raw bucket as well as the edited bucket
## **"media/getAllUserVideos/{{user_id_of_who_you_want_to_grab}}"** => 
grabs ALL videos that are being stored in the raw bucket as well as the edited bucket
## **"media/getAllEvents"** => 
grabs ALL events from mysql database
## **"media/getSpecificEvent/{{event_id_of_which_event_you_want_to_grab}}"** => 
grabs a specific event from the mySQL database with all of the details about the event as well as all of the content that is associated with that event
## **"media/getAllImagesUserEvent/{{user_id_of_who_you_want_to_grab}}/{{event_id_of_which_event_you_want_to_grab}}"** => 
grabs all images for a specific user at a specific event
## **"media/getAllVideosUserEvent/{{user_id_of_who_you_want_to_grab}}/{{event_id_of_which_event_you_want_to_grab}}"** => 
grabs all videos for a specific user at a specific event
## **"media/updateDatabase"** => 
Initializing/updating the database. Only to be used once at the very beginning of launching the website to transfer all of the existing files that are stored in the s3 database but not yet tracked in the sql database specific to the api that we are using. Once the api is able to continually update the sql database every time an image is uploaded this function will never have to be run again