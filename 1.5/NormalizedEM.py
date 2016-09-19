import PIL
import os
import math
from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import datetime

Eps = 0.0000000001
termDoc = np.load("termDoc250.npy")
termDoc = termDoc/255.0
##termDoc contains an array of M pixels for N samples , each element defining the pixel intensity

print termDoc.shape;

Strokes = 8
#iterations = 15
N = 250
M = 1600
LikelihoodList = []

Pz_d_w = np.zeros((N,Strokes,M),dtype = np.float64)  	##Probability(zk|di,wj) Probability of k-th stroke given i-th sample and j-th pixel is black
Pw_z  = np.zeros((Strokes,M),dtype = np.float64)	 	##Probability(wj|zk)  Probability of j-th pixel being black given k-th stroke
Pz_d = np.zeros((N,Strokes),dtype = np.float64)			##Probability(zk|di) Probability of k-th stroke being present in i-th sample
nD = np.zeros(N,dtype=np.float64)


				
for m in xrange(0,1600):					
	for k in xrange(Strokes) :
		Pw_z[k][m] = random.random()


for i in xrange(N):
	for k in xrange(Strokes) :
		Pz_d[i][k] = random.random();
	nD[i]=np.sum(termDoc[i])
					    				##nD[i] = sum of (Intesity of ) the white pixels in i-th document


Norm1 =  np.sum(Pw_z,axis=1);       ##Norm1 contains for each stroke k (sum(j = 1 to M ) P(wj|zk))  
Norm2 = np.sum(Pz_d,axis=1);		##Norm2 contains for each document i (sum k = 1 to Strokes P(zk|di))	
for i in xrange(Strokes):
	for j in xrange(0,1600):
		Pw_z[i][j]/=Norm1[i]
		

Pn = float(1)/N									##Normalized beacuse they should be 1

for i in xrange(N):
	for j in xrange(Strokes):
		Pz_d[i][j]/=Norm2[i]
#print np.sum(Pz_d,axis=0)






print "End of Initialization"


#####  Starting EM Algorithm  #####

BegTime = datetime.datetime.now();

em = 0


while(1) :

	em = em +1 
	StartTime = datetime.datetime.now();


	##Checking for convergence
	print ""
	if(em>2):
		percchange = (LikelihoodList[-1]-LikelihoodList[-2])/abs(LikelihoodList[-2])
		print "Percentage Change = "+str(percchange) 
		if(percchange<0.000001):
			break;



	
	#####  E-Step  #####
	
	for i in xrange(N):
		for k in xrange(Strokes):
			for j in xrange(M):
				den = Eps
				for l in xrange(Strokes):
					den+= Pw_z[l][j]*Pz_d[i][l]
				Pz_d_w[i][k][j]=(Pw_z[k][j]*Pz_d[i][k])/den
	

	S=(datetime.datetime.now())
	Ss=S-StartTime
	print "End of E Step " + str(em)+" in time ",
	print str(Ss.seconds/60)+" Minutes "+str(Ss.seconds%60)+" Seconds"


	#####  M-Step - I #####
	
	for k in xrange(Strokes):
		den = Eps
		for m in xrange(M):
				for i in xrange(N):
					den+=termDoc[i][m]*Pz_d_w[i][k][m]
		for j in xrange(M):
		#	den = Eps
			num = Eps
			
			for i in xrange(N):
				num += termDoc[i][j]*Pz_d_w[i][k][j]
			Pw_z[k][j]=num/den

		#print "End of M Step - I " + str(em)

	#####  M-Step - II #####
	for i in xrange(N):
		for k in xrange(Strokes):
			num=Eps
			for j in xrange(M):
				num += termDoc[i][j] * Pz_d_w[i][k][j]
			Pz_d[i][k] = num/(nD[i])

	EndTime = datetime.datetime.now()
	
	E=EndTime-S

	print "End of M Step " + str(em)+" in time ",
	print str(E.seconds/60)+" Minutes "+str(E.seconds%60)+" Seconds"



	##Calculating Likelihood


	A=0
	B=0
	
	Likelihood=0
	for i in xrange(N):
		prevA=A
		A=0
		Likelihood+= nD[i]*(math.log(Pn)+prevA)
		for j in xrange(M):
			prevB = B
			B=0
			A+=termDoc[i][j]/nD[i]*prevB
			for k in xrange(Strokes):
				B+=Pw_z[k][j]*Pz_d[i][k]
			B=math.log(B)	
	

	LikelihoodList.append(Likelihood)

	LikelihoodEndTime = datetime.datetime.now();
	
	LikelihoodTime = LikelihoodEndTime-EndTime			

	minutes=LikelihoodTime.seconds/60
	seconds=LikelihoodTime.seconds%60



##Plotting Likelihood

	plt.scatter(xrange(len(LikelihoodList)),LikelihoodList)
	#plt.show()
	plt.savefig("Plots/Likelihood.png")

	print "Likelihood = "+str(Likelihood) + " " ,
	print "Completed in "+str(minutes)+" Minutes "+str(seconds)+" Seconds"




	ElapsedTime = LikelihoodEndTime - StartTime

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
			imgStrokes[x][y] = Pw_z[k][x*40+y]*255/ma
	imgStrokes  =  np.uint8(imgStrokes)
	img  =  Image.fromarray(imgStrokes)
	#img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
	#img.show();
	img.save("Stroke/StrokeImage" + str(k) + ".tif")	
