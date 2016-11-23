import PIL
import os
from PIL import Image

hsize = 100
basewidth = 100
zers = "0000"
error = open("errors.txt",'w')
for j in xrange(0,10):
	stri = "stro"+str(j)+".jpg"
	print stri+" ",
	img = Image.open(stri)
	wpercent = (basewidth/float(img.size[0]))
	img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
	img.save(stri)
	width, height =img.size
	print width,height
