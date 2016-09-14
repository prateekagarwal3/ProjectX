import PIL
import os
import math
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
zers  =  "0000"
for i in xrange(0,235):#directory
	eps  =  0.00000000001
	path  =  "F"  +  zers[:3-len(str(i))]  +  str(i)
	print path
	if os.path.exists(path)  ==  False:
		print "Exp"
		continue
	length  =  len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
	try :
		pdf  =  np.load(path  +  "/PdfPickle.npy") 
		pdf=1-pdf
		N = 75
		n = np.zeros(2,dtype = np.float64)
		#n[0] = np.load(path + "/BlackCount.npy")
		#n[1] = N-n
		k  =  input()
		

		Pz_d = np.zeros(k,dtype = np.float64);
		Pw_z = np.zeros((k,75,75),dtype = np.float64);
		Pz_d_w = np.zeros((k,75,75),dtype = np.float64);
		summation = 0
		for j in xrange(0,k): 					##Intialization
			Pz_d[j] = 0.5
			for a in xrange(0,75):
				for b in xrange(0,75):
					Pw_z[j][a][b] = 0.5
					summation = summation + pdf[a][b]
		
		#print Pw_z[0][4][32]
		#sys.exit()


		for c in xrange(100):
			print c                            ##E-Step 
			for j in xrange(0,k):
				for a in xrange(0,N):
					for b in xrange(0,N):
						f = eps
						for l in xrange(0,k):
							f = f + Pw_z[l][a][b]*Pz_d[l]



						Pz_d_w[j][a][b] = (Pw_z[j][a][b]*Pz_d[j])
						Pz_d_w[j][a][b] = Pz_d_w[j][a][b]/f
						print "f in E-step " + str(f)			
						
													##E-Step ENDS
			print "PROBLEM: " + str(Pz_d_w[0][4][32])


													##M-Step	
			for j in xrange(0,k):
				f = 0.0
				for l in xrange(0,N):
					for m in xrange(0,N):
						f = f + pdf[l][m]*(Pz_d_w[j][l][m])
						#print "f in M-step " + str(j) + " " + str(l) + " " + str(m) + " " + str(Pz_d_w[j][l][m])
						if(math.isnan(f)):
							sys.exit()	
				for a in xrange(0,N):
					for b in xrange(0,N):
						Pw_z[j][a][b] = (Pz_d_w[j][a][b])*pdf[a][b]/f

				#print Pz_d_w[0][4][32],pdf[4][32]
				#sys.exit();
									
				z = 0.0
				for a in xrange(0,N):
					for b in xrange(0,N): 	
						z = z + pdf[a][b]*Pz_d_w[j][a][b]

						#print "z,pdf,Pz_d_w in M-step  " + str(z) + " " + str(pdf[a][b]) + " " + str(Pw_z[j][a][b])
				#sys.exit()

				Pz_d[j] = z/5625


		for j in xrange(0,k):
			new_mat = Pw_z
			print "Probability of " + str(j) + "  =  "  + str(Pz_d[j])		
			ma=np.amax(new_mat[j])
			newimg  =  new_mat[j]*255/ma
			newimg  =  np.uint8(newimg)
			print newimg
			img  =  Image.fromarray(newimg);
			img.save(path + "/Simage" + str(j) + ".tif");

		sys.exit()



	except(IOError,OSError) as err:
		print "error"
		continue