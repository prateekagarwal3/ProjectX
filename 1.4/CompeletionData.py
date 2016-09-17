import numpy as np
import matplotlib.pyplot as plt

Pw_z=np.load("w_z.npy")
Pz_d=np.load("z_d.npy")

#np.set_printoptions(threshold=np.inf)


Strokes=10


ma = np.amax(Pw_z)
Pw_z=Pw_z.transpose()
#Pw_z=Pw_z*255/ma



print np.amax(Pw_z,axis=0)



for i in xrange(Strokes):
	plt.ylim((0,ma))
	plt.xlim((0,1600))
	plt.scatter(xrange(1600),Pw_z[i])
	plt.savefig("Plots/Stroke "+str(i)+" Plot")
	plt.clf()




