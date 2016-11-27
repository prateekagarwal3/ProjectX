import PIL
import os
from PIL import Image

hsize = 40
basewidth = 40
error = open("errors.txt",'w')

N=["00013","00018","00026","00029","00053","00057","00101","00109","00141","00165"]

for i in xrange(11,37):
	for j in xrange(len(N)):
		nwpath = "Sample0"+str(i)+"/img0"+str(i)+"-"+N[j]+".png";
		print(nwpath)
		try:
			img = Image.open(nwpath)
		except (IOError,OSError) as err:
			error.write("FileName Error : " + nwpath + "\n")
			print ''
			continue

		wpercent = (basewidth/float(img.size[0]))
		img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
		path = "Sample0"+str(i)+"/"+str(j)+".tif";
		print(path)
		img.save(path)
		width, height = img.size
		print width,height