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

from sklearn.neighbors import NearestNeighbors

neigh = NearestNeighbors(n_neighbors=1,algorithm='brute')

M = 1600
rM = np.int32( math.sqrt(M));
charMap = np.load("charMap.npy")
P= np.load("termDocStroke10.npy");
P = 1-P/255
Strokes = charMap.shape[1]
neigh.fit(charMap)


N = 10

imgPixels = np.zeros((M),dtype = np.float64)

for i in xrange(N):
	C=np.zeros((Strokes))
	path = "Testing Data/Sample011/"+str(i)+".tif";
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
	print(neigh.kneighbors(C))
		




