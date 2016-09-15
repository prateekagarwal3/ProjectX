import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import sys

Eps = 0.0000000001
termDoc = np.load("termDoc.npy")
termDoc = termDoc/255.0

hsize = 100
basewidth = 100

Strokes = 15
iterations = 15
N = 75
M = 1600

Pz_d_w = np.zeros((Strokes,N,M),dtype = np.float64)
Pw_z  = np.zeros((M,Strokes),dtype = np.float64)
Pz_d = np.zeros((Strokes,N),dtype = np.float64)

for k in xrange(Strokes) : #Initialization
	for i in xrange(N) :
		for m in range(M):
			Pz_d_w[k][i][m] = random.random()
				
for m in xrange(0,1600):
	for k in xrange(Strokes) :
		Pw_z[m][k] = random.random()

for k in xrange(Strokes) :
	for i in xrange(N) :
		Pz_d[k][i] = random.random()

print "End of Initialization"


#####  Starting EM Algorithm  #####

for em in xrange(iterations) :
	
	#####  E-Step  #####
	print em
	for i in xrange(N):
		for j in xrange(M):
			den = Eps
			for l in xrange(Strokes):
				den = den + Pw_z[j][l] * Pz_d[l][i]
			for k in xrange(Strokes):
				Pz_d_w[k][i][j] = Pw_z[j][k] * Pz_d[k][i]	
				Pz_d_w[k][i][j] /= den

	print "End of E Step " + str(em)

	#####  M-Step - I #####
	
	for k in xrange(Strokes):
		den = Eps
		for m in xrange(M):
			for i in xrange(N):
				den += termDoc[i][m] * Pz_d_w[k][i][m]
		for j in xrange(M):
			num = Eps
			for i in xrange(N):
				num += termDoc[i][j] * Pz_d_w[k][i][j]

			Pw_z[j][k] = num/den

	print "End of M Step - I " + str(em)

	#####  M-Step - II #####

	for k in xrange(Strokes):
		for i in xrange(N):
			num=Eps
			for j in xrange(M):
				num += termDoc[i][j] * Pz_d_w[k][i][j]
			Pz_d[k][i] = num/M

	print "End of M Step - II " + str(em)


imgStrokes = np.zeros( (40,40),dtype = np.float64 )

ma = np.amax(Pw_z)
for k in xrange(Strokes):
	for x in xrange(40):
		for y in xrange(40):
			imgStrokes[x][y] = Pw_z[x*40+y][k] * 255/ma
	imgStrokes  =  np.uint8(imgStrokes)
	img  =  Image.fromarray(imgStrokes)
	img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
	img.show();
	img.save("/StrokeImagev.2" + str(k) + ".tif")	
