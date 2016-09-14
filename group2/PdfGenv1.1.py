import PIL
import os
import math
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

zers = "0000"

for i in xrange(0,235):#directory
	blackcount = 0
	path = "F" + zers[:3-len(str(i))] + str(i)
	print path
	if os.path.exists(path) == False:
		print "Exp"
		continue
	length = len(os.listdir(os.getcwd()))
	coords = [[[0 for k in xrange(40)] for j in xrange(40)] for i in xrange(length)]
	pdf = [[0.0 for k in xrange(40)] for j in xrange(40)]
	#npdf = np.zeros((40,40))
	#print "HELLO"
	try:
		#print "yo"
		
		pdf=np.load(path+"/PdfPickle.npy");
		npdf=pdf*255;
		npdf=np.uint8(npdf);
		print npdf

		# for k in xrange(0,40):
		# 	for l in xrange(0,40):
		# 		npdf[k*40+l] = pdf[k][l]


		# ind = np.arange(0,npdf.size)
		# plt.plot(npdf,'ro')
		# plt.savefig(path+"/image.png")

		img = Image.fromarray(npdf);
		img.save(path+"/probimage.tif");
		#img.show()

	except (IOError,OSError) as err:
		print "Exception"
		continue