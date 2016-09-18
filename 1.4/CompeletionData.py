import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import itertools

Pw_z=np.load("w_z.npy")
Pz_d=np.load("z_d.npy")

#np.set_printoptions(threshold=np.inf)


Strokes=10
P = np.zeros((Strokes,40,40),dtype=np.float64)



ma = np.amax(Pw_z)
Pw_z=Pw_z.transpose()
#Pw_z=Pw_z*255/ma

for k in range(Strokes):
	for i in xrange(40):
		for j in xrange(40):
			P[k][i][j]=Pw_z[k][i*40+j]




print np.amax(Pw_z,axis=0)

R = np.array(xrange(40))
R1 = np.tile(R,40)
R2 = np.repeat(R,40)

# for i in xrange(R1.size):
# 	for j in xrange(R2.size):
# 		print R2[i], R2[j]

for i in xrange(Strokes):
	plt.ylim((0,ma))
	plt.xlim((0,1600))
	#ax=Axes3D(fig)
	plt.scatter(xrange(1600),Pw_z[i])
	plt.savefig("Plots/Stroke "+str(i)+" Plot")
	#plt.show()
	plt.clf()
	




