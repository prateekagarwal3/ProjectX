import PIL
import os
from PIL import Image

hsize = 40
basewidth = 40
error = open("errors.txt",'w')

for i in xrange(1,27):
	path = str(i) + ".jpg"
	try:
		img = Image.open(path)
	except (IOError,OSError) as err:
		error.write("FileName Error : " + path + "\n")
		print ''
		continue

	wpercent = (basewidth/float(img.size[0]))
	img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
	img.save(path)
	width, height = img.size
	print width,height