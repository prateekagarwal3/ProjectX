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

StrokesArray = [10]
times = len(StrokesArray);
	#iterations = 15
Narray = [260]
M = 1600
Eps = 0.0000000001
errorBound = 1.1

for numEm in xrange(times):

	N = Narray[numEm]
	Strokes = StrokesArray[numEm]	

	

	if numEm == 0:
		termDoc = np.load("termDocTraining26x10.npy")
		termDoc = termDoc
		termDoc = 255 - termDoc
		termDoc = termDoc/255
	else: 
		termDoc = np.load("w_zL"+str(numEm-1)+".npy");

		for k in xrange(N):
			sm=0
			ma = np.amax(termDoc[k])
			odr = np.argsort(termDoc[k])
			for i in xrange(M-1,-1,-1):
				sm+=termDoc[k][odr[i]];
				if(sm>=errorBound):
					#cnt = cnt + 1
					termDoc[k][odr[i]]=0;

		for k in xrange(N):
			ma = np.amax(termDoc[k])
			for j in xrange(M):
				termDoc[k][j]= termDoc[k][j]/ma

		print termDoc

	##print termDoc
	##termDoc contains an array of M pixels for N samples , each element defining the pixel intensity

	print termDoc.shape;

	
	LikelihoodList = []

	Pz_d_w = np.zeros((N,Strokes,M),dtype = np.float64)  	##Probability(zk|di,wj) Probability of k-th stroke given i-th sample and j-th pixel is black
	Pw_z  = np.zeros((Strokes,M),dtype = np.float64)	 	##Probability(wj|zk)  Probability of j-th pixel being black given k-th stroke
	Pz_d = np.zeros((N,Strokes),dtype = np.float64)			##Probability(zk|di) Probability of k-th stroke being present in i-th sample
	nD = np.zeros(N,dtype=np.float64)
	rM = np.int32(math.sqrt(M));

	imgStrokes = np.zeros( (rM,rM),dtype = np.float64 )

					
	for m in xrange(M):					
		for k in xrange(Strokes):
			Pw_z[k][m] = random.random()


	for i in xrange(N):
		for k in xrange(Strokes) :
			Pz_d[i][k] = random.random();
		nD[i]=np.sum(termDoc[i])
						    				##nD[i] = sum of (Intesity of ) the white pixels in i-th document

	Norm1 =  np.sum(Pw_z,axis=1);       ##Norm1 contains for each stroke k (sum(j = 1 to M ) P(wj|zk))  
	Norm2 = np.sum(Pz_d,axis=1);		##Norm2 contains for each document i (sum k = 1 to Strokes P(zk|di))	
	for i in xrange(Strokes):
		for j in xrange(0,M):
			Pw_z[i][j]/=Norm1[i]
			

	Pn = float(1)/N									##Normalized beacuse they should be 1

	for i in xrange(N):
		for j in xrange(Strokes):
			Pz_d[i][j]/=Norm2[i]
	#print np.sum(Pz_d,axis=0)



	platform = cl.get_platforms()[1];
	device = platform.get_devices()[0]
	cntxt=cl.Context([device])
	# cntxt = cl.create_some_context()
		




	temp = np.ones((M,),dtype=np.float64);
	d_tD = cl.Buffer(cntxt,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=termDoc);
	d_out =cl.Buffer(cntxt,cl.mem_flags.WRITE_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=temp);
	d_nD = cl.Buffer(cntxt,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=nD)
	d_out2 = cl.Buffer(cntxt,cl.mem_flags.WRITE_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=Pz_d);

	print "End of Initialization"


	#####  Starting EM Algorithm  #####

	BegTime = datetime.datetime.now();

	em = 0

	prg = """
				
					#pragma OPENCL EXTENSION cl_khr_fp64 : enable
				
				
				__kernel void EStep(__global double *Pw_z,__global double *Pz_d,__global double* Pz_d_w, int i, int k )
				{
					
					int  j = get_global_id(0);
					int l ;
					int Strokes = %d;
					int N = %d;
					int M = %d;
					
					double den = 0.0000000001;
					for (l=0;l<Strokes;l++)
					{
						int idx1 =  l*M + j;
						int idx2 = i*Strokes + l; 
						den+=Pw_z[idx1]*Pz_d[idx2];
					}
					int idx1,idx2;
					idx1 = k*M+j;
					idx2 = i*Strokes + k;
					
					Pz_d_w[j]=(Pw_z[idx1]*Pz_d[idx2])/den;
				}
				
				
				__kernel void MStep1(__global double *Pz_d_w,__global double * out,global double * termDoc, int k,double den)
				{
					int j = get_global_id(0);
					int Strokes = %d;
					int N = %d;
					int M = %d;
					int i ;
					double num = 0.000000001;
					int idx1,idx2;
					for(i=0;i<N;i++)
					{	
						idx1=i*M+j;
						idx2=i*M*Strokes+k*M+j;
						num+=termDoc[idx1]*Pz_d_w[idx2];
					}
					out[j]=num/den;
				}
						
				__kernel void MStep2(__global double* nD,__global double* Pz_d_w, __global double* termDoc,__global double* out )
				{
					int i = get_global_id(0);
					int Strokes = %d;
					int N = %d;
					int M = %d;
					double num = 0.000000001;

					int j , k;
					for(k=0;k<Strokes;k++)
					{
						num = 0.000000001;
						for(j=0;j<M;j++)
						{
							num += termDoc[i*M+j] * Pz_d_w[i*M*Strokes+k*M+j];
						}
						out[i*Strokes+k]=num/nD[i];

					}




				}
					
						
		
		"""%(Strokes,N,M,Strokes,N,M,Strokes,N,M);
				
	bld = cl.Program(cntxt,prg).build();
	Q = cl.CommandQueue(cntxt);

		
		


	while(1) :

		em = em +1 
		StartTime = datetime.datetime.now();


		##Checking for convergence
		print ""
		if(em>2):
			percchange = (LikelihoodList[-1]-LikelihoodList[-2])/abs(LikelihoodList[-1])
			print "Percentage Change = "+str(percchange) 
			if(percchange<2e-06):
				break;

		
		
		
		
		
		
		
		#####  E-Step  #####
		
		d_Pw_z=cl.Buffer(cntxt,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=Pw_z)
		d_Pz_d=cl.Buffer(cntxt,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=Pz_d)
		
		
		for i in xrange(N):
			for k in xrange(Strokes):
				'''for j in xrange(M):
					den = Eps
					for l in xrange(Strokes):
						den+= Pw_z[l][j]*Pz_d[i][l]
					Pz_d_w[i][k][j]=(Pw_z[k][j]*Pz_d[i][k])/den'''
				launch = bld.EStep(Q,(M,),(1,),d_Pw_z,d_Pz_d,d_out,np.int32(i),np.int32(k));
				launch.wait();
				cl.enqueue_read_buffer(Q,d_out,Pz_d_w[i][k]).wait()
				
				
				
		S=(datetime.datetime.now())
		Ss=S-StartTime
		print "End of E Step " + str(em)+" in time ",
		print str(Ss.seconds/60)+" Minutes "+str(Ss.seconds%60)+" Seconds"


		#####  M-Step - I #####
		
		d_in=cl.Buffer(cntxt,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=Pz_d_w);
		
		
		for k in xrange(Strokes):
			den = Eps
			for m in xrange(M):
					for i in xrange(N):
						den+=termDoc[i][m]*Pz_d_w[i][k][m]
			'''for j in xrange(M):
			#	den = Eps
				num = Eps
				for i in xrange(N):
					num += termDoc[i][j]*Pz_d_w[i][k][j]
				Pw_z[k][j]=num/den'''
			launch = bld.MStep1(Q,(M,),(1,),d_in,d_out,d_tD,np.int32(k),np.float64(den));
			launch.wait();
			cl.enqueue_read_buffer(Q,d_out,Pw_z[k]).wait()

		#####  M-Step - II #####
		'''for i in xrange(N):
			for k in xrange(Strokes):
				num=Eps
				for j in xrange(M):
					num += termDoc[i][j] * Pz_d_w[i][k][j]
				Pz_d[i][k] = num/(nD[i])'''
		launch = bld.MStep2(Q,(N,),(1,),d_nD,d_in,d_tD,d_out2);
		launch.wait();
		cl.enqueue_read_buffer(Q,d_out2,Pz_d).wait()

		EndTime = datetime.datetime.now()
		
		E=EndTime-S

		print "End of M Step " + str(em)+" in time ",
		print str(E.seconds/60)+" Minutes "+str(E.seconds%60)+" Seconds"



		##Calculating Likelihood


		A=0
		B=0
		
		Likelihood=0
		for i in xrange(N):
			A=0;
			for j in xrange(M):
				B=0;
				for k in xrange(Strokes):
					B+=(Pw_z[k][j]*Pz_d[i][k])
				B=math.log(B)
				A+=termDoc[i][j]*B/nD[i]
			Likelihood+=nD[i]*(math.log(Pn)+A)		


		LikelihoodList.append(Likelihood)

		LikelihoodEndTime = datetime.datetime.now();
		
		LikelihoodTime = LikelihoodEndTime-EndTime			

		minutes=LikelihoodTime.seconds/60
		seconds=LikelihoodTime.seconds%60



	##Plotting Likelihood

		plt.scatter(xrange(len(LikelihoodList)),LikelihoodList)
		#plt.show()
		#plt.savefig("Plots/Likelihood"+str(numEm)+".png")

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












	ma = np.amax(Pw_z)			##Normalize using the maximum 
	np.save("w_zL"+str(numEm),Pw_z);
	np.save("z_dL"+str(numEm),Pz_d)
	                                   	
	for k in xrange(Strokes):
		for x in xrange(rM):
			for y in xrange(rM):
				imgStrokes[x][y] =255 -  Pw_z[k][x*rM+y]*255/ma
		imgStrokes  =  np.uint8(imgStrokes)
		img  =  Image.fromarray(imgStrokes)
		#img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
		#img.show();
		img.save("Strokes/StrokeImage" +str(numEm)+"L"+str(k) + ".tif")	
