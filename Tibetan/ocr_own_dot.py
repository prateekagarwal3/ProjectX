import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import datetime
import pyopencl as cl
import pyopencl.array as cl_array


M = 1600
rM = np.int32( math.sqrt(M));
charMap = np.load("charMap.npy")
P= np.load("termDocStroke20nr11.npy");
P = 255-P
P=P/255
charNum = charMap.shape[0]
Strokes = charMap.shape[1]
zers = "0000"

Samples = 10
existingsamples = 0
imgPixels = np.zeros((M),dtype = np.float64)

def calcSim(A,B):
	return A*B

correct_all=0.0
for dirpath in xrange(4,34):
	charPath = "F" + zers[:3-len(str(dirpath))] + str(dirpath)

	correct = 0.0
	for i in xrange(29,39):
		path = "Testing Data/"+str(charPath)+"/"+"000" + str(i)+".tif";
		print path
		try :	
			img = Image.open(path);
			imgArray = np.array(img);
			for k in xrange(rM):
				for l in xrange(rM):
					imgPixels[k*rM+l] = imgArray[k][l];
			imgPixels = 255 - (imgPixels)
			imgPixels =  imgPixels/255
			
			mn = 1000000000000000
			pos = -1
			for j in xrange(charNum):
				dist = 0
				C = np.zeros((Strokes),dtype = np.float64)
				sm = np.sum(imgPixels)
				for k in xrange(Strokes):
					for l in xrange(M):
						C[k]+=calcSim(imgPixels[l],P[k][l])
					C[k]= C[k]/sm
				for k in xrange(Strokes):
					dist = (C[k]-charMap[j][k])**2 + dist
				if(mn>dist):
					pos = j
					mn = dist

			#print pos,dist
			existingsamples = existingsamples + 1
			if pos == dirpath - 4 :
				correct = correct + 1
		except(IOError,OSError):
			print "Image Not Found"

	correct_all = correct_all + correct
	print correct*100/Samples

print "Overall accuracy : "+str(correct_all*100/existingsamples)