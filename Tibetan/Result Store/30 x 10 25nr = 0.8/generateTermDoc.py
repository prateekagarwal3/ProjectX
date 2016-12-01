import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import sys



Strokes = 25

M = 1600
Eps = 0.0000000001


zers = "0000"
termDocument = np.zeros((Strokes,M))
docNum = 0

for dirTrav in xrange(1) : # 4 - 33 Directories
	

	
	#print "File : " + str(dirLength)
	try : 
		for fileTrav in xrange(Strokes): #Each Image of a Character		
			imgPath ="StrokeImage0"+str(fileTrav)+".tif";
			print imgPath
			#N = N + 1
			try:
				img = Image.open(imgPath)
			except (IOError,OSError) as err:
				print "Image Not Found"
				continue
			imgPixels = np.array(img) #255 is White & 0 is Black
			tempImgPixels = [0 for x in range(1600)]
			for x in xrange(0,40):
				for y in xrange(0,40):
					tempImgPixels[x*40+y] = imgPixels[x][y]
			termDocument[docNum] = tempImgPixels
			print termDocument[docNum]
			docNum = docNum + 1

	except(IOError,OSError) as err:
		print "error"
		continue

#Stored Term Document matrix in pickle

np.save("termDocStroke20nr11",termDocument)
ter2 = np.load("termDocStroke20nr11.npy")
if (ter2 == termDocument).all():
	print "Success"
#print N