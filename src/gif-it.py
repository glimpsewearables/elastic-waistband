import os
from os import listdir
from moviepy.editor import *

files = os.listdir("videos/")
files.sort()
#print(files)
for idx, file in enumerate(files):
	clip = VideoFileClip("videos/" + file) 
	start = 5.0
	end = 7.0
	if (clip.duration < 5):
		start = 0.0
		end = clip.duration
	clip = (clip.subclip((0,start),(0,end)).resize(0.3))
	clip.write_gif("gifs/ezgif.com-crop (%d).gif" % (idx + 50))