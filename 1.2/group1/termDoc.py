import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import sys


Strokes = 6
N = 0
Eps = 0.0000000001


zers = "0000"
termDocument = np.zeros((75,1600))
docNum = 0

for dirTrav in xrange(4,9) : # 4 - 33 Directories
	charPath = "F" + zers[:3-len(str(dirTrav))] + str(dirTrav)
	#print "Path : " + charPath
	if os.path.exists(charPath) == False:
		print "Directory Not Found"
		continue

	dirLength = len([f for f in os.listdir(charPath) if os.path.isfile(os.path.join(charPath, f))])
	#print "File : " + str(dirLength)
	try : 
		for fileTrav in xrange(1,16): #Each Image of a Character		
			imgPath = charPath + "/000" + str(fileTrav) + ".tif"

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

np.save("termDoc",termDocument)
ter2 = np.load("termDoc.npy")
if (ter2 == termDocument).all():
	print "Success"