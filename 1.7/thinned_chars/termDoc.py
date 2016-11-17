import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import sys


Strokes = 20
N = 26 
M = 1600
Eps = 0.0000000001

termDocument = np.zeros((N,M))
docNum = 0

for dirTrav in xrange(1,27) : # 1 - 26 Alphabets

	charPath = str(dirTrav)
	#print "Path : " + charPath
	if os.path.exists(charPath) == False:
		print "Directory Not Found"
		continue

	try : 
		imgPath = charPath + ".jpg"
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

np.save("termDoc26*1",termDocument)
ter2 = np.load("termDoc26*1.npy")
if (ter2 == termDocument).all():
	print "Success"
#print N