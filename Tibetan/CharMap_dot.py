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


N = 30
Samples = 10


P= np.load("termDocStroke20nr11.npy");

print P.shape
Strokes,M  = P.shape
rM = math.sqrt(M)

P = 255 - P
P = P/255

def calcSim(A,B):
	return A*B

imgPixels = np.load("termDocTraining30x10.npy")
print imgPixels.shape
imgPixels = 255-imgPixels
imgPixels=imgPixels/255;
charMap = np.zeros((N,Strokes),dtype = np.float64)

for i in xrange(N):
	for j in xrange(Samples):
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