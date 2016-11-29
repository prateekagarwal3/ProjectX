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
P= np.load("termDocStroke18nr11.npy");
P = 255-P
P=P/255
charNum = charMap.shape[0]
Strokes = charMap.shape[1]

xnorbuf = 0.4

N = 10

imgPixels = np.zeros((M),dtype = np.float64)

def calcSim(A,B):
	if abs(A-B) > xnorbuf :
		return 1
	return 0

'''def calcSim(A,B):
	if A>0.6 or B>0.6:
		return 1
	return A*B'''

correct_all=0.0
for dirpath in xrange(11,37):
	correct = 0.0
	for i in xrange(N):
		path = "Testing Data/Sample0"+str(dirpath)+"/"+str(i)+".tif";
		#print path
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
		if pos == dirpath-11 :
			correct = correct + 1
	correct_all = correct_all + correct
	print correct*100/N

print "Overall accuracy : "+str(correct_all*100/(charNum*N))		
	
			


'''for i in xrange(N):
	C=np.zeros((Strokes))
	path = "test.tif";
	print path
	img = Image.open(path);
	imgArray = np.array(img);
	for k in xrange(rM):
		for l in xrange(rM):
			imgPixels[k*rM+l] = imgArray[k][l];
	imgPixels = 255 - (imgPixels)
	imgPixels =  imgPixels/255
	for k in xrange(Strokes):
		C[k]=np.sum(np.abs(imgPixels-P[k]))
	C.reshape(1,-1)
	print(neigh.kneighbors(C))'''
		




