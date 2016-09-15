import PIL
import os
import math
from PIL import Image
import numpy as np

zers = "0000"

for i in xrange(0,235):#directory
	length = len(os.listdir(os.getcwd()))
	blackcount = 0
	path = "F" + zers[:3-len(str(i))] + str(i)
	if os.path.exists(path) == False:
		continue
	length = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
	print length
	coords = [[[0 for k in xrange(40)] for j in xrange(40)] for i in xrange(length)]
	pdf = [[0.0 for k in xrange(40)] for j in xrange(40)]
	try:
		for j in xrange(1,length+1):#Each Image of Character		
			stri = path+"/000"+str(j)+".tif"
			#print j;
			try:
				img = Image.open(stri)
			except (IOError,OSError) as err:
				continue
			imagepixels = np.array(img)#imagepixels contains the 2d array of image pixels(0/255)

			for k in xrange(0,40): #Counting number of black pixels in the entire directory
				for l in xrange(0,40):
					if imagepixels[k][l] == 255:
						coords[j-1][k][l] = 1
						blackcount = blackcount + 1

		# for k in xrange(0,40):   #Counting number of black pixels in the entire directory for a particular point
		# 	for l in xrange(0,40):
		# 		for j in xrange(0,length):
		# 			pdf[k][l] += float(coords[j][k][l])/length

		# for j in xrange(1,length+1): #Writing to pdf file		
		# 	pdffile = open(path + "/" + "PDF-" + path + ".txt", "wb")
		# 	pdffile.write(str(pdf))
		

		#np.save(path+"/PdfPickle",pdf);
		countvar = float(blackcount)/length
		print countvar
		np.save(path+"/BlackCount",countvar)



	except(IOError,OSError) as err:
		continue