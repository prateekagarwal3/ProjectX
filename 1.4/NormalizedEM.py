import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import sys
import datetime

Eps = 0.0000000001
termDoc = np.load("termDoc.npy")
##termDoc contains an array of M pixels for N samples , each element defining the pixel intensity


<<<<<<< HEAD
Strokes = 15
=======
Strokes = 20
>>>>>>> 08b8805a5b2318782202313f7296eb703677ab18
iterations = 40
N = 2517
M = 1600

Pz_d_w = np.zeros((Strokes,N,M),dtype = np.float64)  	##Probability(zk|di,wj) Probability of k-th stroke given i-th sample and j-th pixel is black
Pw_z  = np.zeros((M,Strokes),dtype = np.float64)	 	##Probability(wj|zk)  Probability of j-th pixel being black given k-th stroke
Pz_d = np.zeros((Strokes,N),dtype = np.float64)			##Probability(zk|di) Probability of k-th stroke being present in i-th sample
nD = np.zeros(N,dtype=np.float64)

				
for m in xrange(0,1600):					
	for k in xrange(Strokes) :
		Pw_z[m][k] = random.random()

for k in xrange(Strokes) :
	for i in xrange(N) :
		Pz_d[k][i] = random.random();
		nD[i] = np.sum(termDoc[i])      ##nD[i] = sum of (Intesity of ) the white pixels in i-th document


Norm1 =  np.sum(Pw_z,axis=0);       ##Norm1 contains for each stroke k (sum(j = 1 to M ) P(wj|zk))  
Norm2 = np.sum(Pz_d,axis=0);		##Norm2 contains for each document i (sum k = 1 to Strokes P(zk|di))	
for i in xrange(Strokes):
	for j in xrange(0,1600):
		Pw_z[j][i]/=Norm1[i]
		

									##Normalized beacuse they should be 1

for i in xrange(N):
	for j in xrange(Strokes):
		Pz_d[j][i]/=Norm2[i]
#print np.sum(Pz_d,axis=0)






print "End of Initialization"


#####  Starting EM Algorithm  #####

BegTime = datetime.datetime.now();

for em in xrange(iterations) :

	StartTime = datetime.datetime.now();
	
	#####  E-Step  #####
	
	for i in xrange(N):
		for j in xrange(M):
			den = Eps
			for l in xrange(Strokes):
				den = den + Pw_z[j][l] * Pz_d[l][i]
			for k in xrange(Strokes):
				Pz_d_w[k][i][j] = Pw_z[j][k] * Pz_d[k][i]	
				Pz_d_w[k][i][j] /= den

<<<<<<< HEAD
	S=(datetime.datetime.now())
	Ss=S-StartTime
	print "End of E Step " + str(em)+" in time "
	print str(Ss.seconds/60)+" Minutes "+str(Ss.seconds%60)+" Seconds"
=======
	print "End of E Step of Iteration No : " + str(em)
>>>>>>> 08b8805a5b2318782202313f7296eb703677ab18

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

		#print "End of M Step - I " + str(em)

	#####  M-Step - II #####
	#for k in xrange(Strokes):
		for i in xrange(N):
			  							
			num=Eps
			for j in xrange(M):
				num += termDoc[i][j] * Pz_d_w[k][i][j]
			Pz_d[k][i] = num/(nD[i])

<<<<<<< HEAD
	EndTime = datetime.datetime.now()
	
	E=EndTime-S

	print "End of M Step " + str(em)+" in time "
	print str(E.seconds/60)+" Minutes "+str(E.seconds%60)+" Seconds"
=======
	print "End of M Step of Iteration No : " + str(em)
>>>>>>> 08b8805a5b2318782202313f7296eb703677ab18


	

	ElapsedTime = EndTime - StartTime

	minutes = ElapsedTime.seconds/60;
	seconds = ElapsedTime.seconds%60;

	print "Took "+str(minutes)+" Minutes "+str(seconds)+" seconds to complete "+str(em)+" iteration"

FinTime = datetime.datetime.now();

TotalElapsedTime = FinTime - BegTime;

print ""
print "Total Time"
print "Minutes: "+str(TotalElapsedTime.seconds/60)
print "Seconds: "+str(TotalElapsedTime.seconds%60)


imgStrokes = np.zeros( (40,40),dtype = np.float64 )

ma = np.amax(Pw_z)			##Normalize using the maximum 
np.save("w_z",Pw_z);
np.save("z_d",Pz_d)
                                   	
for k in xrange(Strokes):
	for x in xrange(40):
		for y in xrange(40):
			imgStrokes[x][y] = Pw_z[x*40+y][k]*255/ma
	imgStrokes  =  np.uint8(imgStrokes)
	img  =  Image.fromarray(imgStrokes)
	#img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
	#img.show();
	img.save("Stroke/StrokeImage" + str(k) + ".tif")	
