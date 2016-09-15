import PIL
import os
from PIL import Image

hsize = 32
basewidth = 32
zers = "0000"
error = open("errors.txt",'w')
for i in xrange(4,34):
	path = "F"+zers[:3-len(str(i))]+str(i)
	try:
		for j in xrange(1,len(os.listdir(path))+1):
			stri = path+"/000"+str(j)+".tif"
			print stri+" ",
			try:
				img = Image.open(stri)
			except (IOError,OSError) as err:
				error.write("FileName Error : " +str(i)+" "+str(j)+"\n")
				print ''
				continue
			wpercent = (basewidth/float(img.size[0]))
			img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
			img.save(stri)
			width, height =img.size
			print width,height
	except (IOError,OSError) as err:
		print error
		print ''
		continue
