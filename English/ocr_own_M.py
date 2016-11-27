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
P= np.load("termDocStroke10.npy");
P = 255-P
P=P/255
charNum = charMap.shape[0]
Strokes = charMap.shape[1]



N = 10

imgPixels = np.zeros((M),dtype = np.float64)

def calcSim(A,B):
	if A>=0.75 and B>=0.75 :
		return 0
	else:
		return (A-B)**2

for i in xrange(N):
	path = "Testing Data/Sample014/"+str(i)+".tif";
	print path
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

	print pos,dist
		
	
			


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
		




