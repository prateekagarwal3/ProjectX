import PIL
import math
import numpy as np
from PIL import Image


for numEm in xrange(4):

	P = np.load('w_zL'+str(numEm)+'.npy');

	Strokes = P.shape[0]
	N = 300;
	M = 1600;

	for k in xrange(Strokes):
		ma=np.sum(P[k])
		print ma
		
	ma = np.max(P);

	#P = ma - P
	Pn = float(1)/M;
	cnt = 0 
	for k in xrange(Strokes):
		sm=0
		ma = np.amax(P[k])
		odr = np.argsort(P[k])
		for i in xrange(M-1,-1,-1):
			sm+=P[k][odr[i]];
			#print sm
			if(sm>=0.85):
				cnt = cnt + 1
				P[k][odr[i]]=0;


	imgStrokes = np.zeros( (40,40),dtype = np.float64 )

	ma = np.amax(P)
	#P = ma - P

	print cnt
	# for k in xrange(Strokes):
	# 	ma=np.amax(P[k])
	# 	P[k]=ma-P[k]
	for k in xrange(Strokes):
		ma = np.amax(P[k])
		for x in xrange(40):
			for y in xrange(40):
				imgStrokes[x][y] =255 - P[k][x*40+y]*255/ma
		imgStrokes  =  np.uint8(imgStrokes)
		img  =  Image.fromarray(imgStrokes)
		#img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
		#img.show();
		img.save("NRStroke/StrokeImage" + str(numEm)+str(k)+ ".tif")