import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import sys



#Strokes = 20
N = 0

M = 1600
Eps = 0.0000000001


zers = "0000"
termDocument = np.zeros((260,M))
docNum = 0

for dirTrav in xrange(11,37) : # 4 - 33 Directories
	
	#print "Path : " + charPath
	

	#print "File : " + str(dirLength)
	try : 
		for fileTrav in xrange(10): #Each Image of a Character		
			imgPath = "Sample0"+str(dirTrav)+"/"+str(fileTrav)+".tif";
			N = N + 1
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

np.save("termDocTest26x10",termDocument)
ter2 = np.load("termDocTest26x10.npy")
if (ter2 == termDocument).all():
	print "Success"
print N