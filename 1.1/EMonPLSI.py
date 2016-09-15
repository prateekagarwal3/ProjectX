import PIL
import os
import math
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random
import sys


Strokes = 5
N = 100
Eps = 0.0000000001
Pz_d_w = np.zeros((Strokes,N,75,75),dtype = np.float64)
Pw_z  = np.zeros((75,75,Strokes),dtype = np.float64)
Pz_d = np.zeros((Strokes,N),dtype = np.float64)

for k in xrange(Strokes) : #Initialization
	for i in xrange(N) :
		for x in xrange(75) : 
			for y in xrange(75) : 
				Pz_d_w[k][i][x][y] = random.random()
				
for x in xrange(75) :
	for y in xrange(75) : 
		for k in xrange(Strokes) :
			Pw_z[x][y][k] = random.random()

for k in xrange(Strokes) :
	for i in xrange(N) :
		Pz_d[k][i] = random.random()

print "End of Initialization"

zers = "0000"
for dirTrav in xrange(4,6) : # 4 - 33 Directories
	charPath = "F" + zers[:3-len(str(dirTrav))] + str(dirTrav)
	#print "Path : " + charPath
	if os.path.exists(charPath) == False:
		print "Directory Not Found"
		continue

	dirLength = len([f for f in os.listdir(charPath) if os.path.isfile(os.path.join(charPath, f))])
	#print "File : " + str(dirLength)
	try : 
		for fileTrav in xrange(1,dirLength + 1): #Each Image of a Character		
			imgPath = charPath + "/000" + str(fileTrav) + ".tif"

			try:
				img = Image.open(imgPath)
			except (IOError,OSError) as err:
				print "Image Not Found"
				continue
			imgPixels = np.array(img) #255 is White & 0 is Black
			for em in xrange(10) :
			#####  E-Step  #####

				for k in xrange(Strokes) :
					for i in xrange(N) :
						for x in xrange(75) :
							for y in xrange(75) :
								den = Eps
								for l in xrange(Strokes) :
									den = den + Pw_z[x][y][l] * Pz_d[l][i]
									Pz_d_w[k][i][x][y] = ( Pw_z[x][y][k] * Pz_d[k][i] ) / den 

				print "End of E-Step : Dir No : " + charPath + " " + "Image No : " + str(fileTrav)

				#####  M-Step - I #####
				for k in xrange(Strokes) :
					den = Eps
					for x in xrange(75) :
						for y in xrange(75):
							for i in xrange(N):
								den = den + ( float(imgPixels[x][y]) / 255.0 ) * Pz_d_w[k][i][x][y]
					for x in xrange(75) :
						for y in xrange(75) :
							for i in xrange(N) :
								Pw_z[x][y][k] = ( Pw_z[x][y][k] + ( float(imgPixels[x][y]) / 255.0 ) * Pz_d_w[k][i][x][y] ) / den

				print "End of M-Step - I : Dir No : " + charPath + " " + "Image No : " + str(fileTrav)

				#####  M-Step - II #####

				for k in xrange(Strokes) :
					for i in xrange(N) :
						for x in xrange(75) :
							for y in xrange(75) :
								Pz_d[k][i] = ( Pz_d[k][i] + (float(imgPixels[x][y]) / 255.0) * Pz_d_w[k][i][x][y] ) / ( 75 * 75 )

				print "End of M-Step - II : Dir No : " + charPath + " " + "Image No : " + str(fileTrav)
	except(IOError,OSError) as err:
		print "error"
		continue

print "EM Done" 
#####  Printing of Image  #####
print "Now Printing Strokes :)"

# for j in xrange(0,Strokes):
# 	new_mat = Pw_z *Pz_d *255
# 	#print "Probability of " + str(j) + "  =  "  + str(Pz_d[j])		
# 	newimg  =  new_mat[j]
# 	newimg  =  np.uint8(newimg)
# 	img  =  Image.fromarray(newimg)
# 	img.save(path + "/Simage" + str(j) + ".tif")	