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

selChar = [16,21,24,29,33,34,39,40,43,44]
M = 1600
rM = np.int32( math.sqrt(M));
charMap = np.load("charMap.npy")
P= np.load("termDocStroke25nr0.8.npy");
P = 255-P
P=P/255
charNum = charMap.shape[0]
Strokes = charMap.shape[1]
zers = "0000"

Samples = 10
existingsamples =0
imgPixels = np.zeros((M),dtype = np.float64)

def calcSim(A,B):
	return A*B

correct_all=0.0
for dirpath in xrange(4,34):
	charPath = "F" + zers[:3-len(str(dirpath))] + str(dirpath)

	correct = 0.0
	for i in xrange(10):
		try:
			path = "Testing Data/"+str(charPath)+"/"+"000" + str(selChar[i])+".tif";
			print path
			img = Image.open(path);
			imgArray = np.array(img);
			for k in xrange(rM):
				for l in xrange(rM):
					imgPixels[k*rM+l] = imgArray[k][l];
			imgPixels = 255 - (imgPixels)
			imgPixels =  imgPixels/255
			existingsamples = existingsamples + 1
			
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
					dist = math.fabs(C[k]-charMap[j][k])**2 + dist
				if(mn>dist):
					pos = j
					mn = dist
		except(IOError,OSError) as err:
			continue
		#print pos,dist
		if pos == dirpath-4 :
			correct = correct + 1
	correct_all = correct_all + correct
	print correct*100/Samples

print "Overall accuracy : "+str(correct_all*100/existingsamples)