import PIL
import os
from PIL import Image

hsize = 40
basewidth = 40
error = open("errors.txt",'w')

N=["01013","00961","00965","00949","00913","00057","00885","00837","00829","00745"]

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