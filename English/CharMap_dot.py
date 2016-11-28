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


N = 26
Samples = 10


P= np.load("termDocStroke15nr11.npy");

print P.shape
Strokes,M  = P.shape
rM = math.sqrt(M)

P = 255 - P
P = P/255
'''for k in xrange(Strokes):
		sm=0
		ma = np.amax(P[k])
		odr = np.argsort(P[k])
		for i in xrange(M-1,-1,-1):
			sm+=P[k][odr[i]];
			#print sm
			if(sm>=ErrorBound):
				cnt = cnt + 1
				P[k][odr[i]]=0;
for k in xrange(Strokes):
	ma = np.amax(P[k])
	P[k]=P[k]/ma'''



def calcSim(A,B):
	return A*B

imgPixels = np.load("termDocTraining26x10.npy")
print imgPixels.shape
imgPixels = 255-imgPixels
imgPixels=imgPixels/255;
charMap = np.zeros((N,Strokes),dtype = np.float64)

for i in xrange(N):
	for j in xrange(Samples):
		'''path = "Samples/"+str(i+1)+"/"+str(j)+".tif";
		img = Image.open(path);
		imgArray = np.array(img);
		for k in xrange(rM):
			for l in xrange(rM):
				imgPixels[k*40+l] = imgArray[k][l];
		imgPixels = 1 - (imgPixels/255)'''
		sm = np.sum(imgPixels[i*Samples+j])
		for k in xrange(Strokes):
			AbsoluteSum=0
			for l in xrange(M):
				AbsoluteSum  += calcSim(imgPixels[i*Samples+j][l],P[k][l])
			print AbsoluteSum,sm
			
			charMap[i][k]+=AbsoluteSum/sm
	charMap[i]=charMap[i]/Samples
	#plt.scatter(xrange(Strokes),charMap[i])
	#plt.savefig(str(i)+" character")
	#plt.clf()



np.save("charMap",charMap)
	
			






