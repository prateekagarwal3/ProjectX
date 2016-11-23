import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import itertools

Pw_z=np.load("w_z.npy")
Pz_d=np.load("z_d.npy")
termdoc = np.load("termDoc.npy")
termdoc = termdoc/255.0

print termdoc.shape
#np.set_printoptions(threshold=np.inf)


Strokes=10
N = 50
P = np.zeros((Strokes,40,40),dtype=np.float64)



ma = np.amax(Pw_z)
# Pw_z=Pw_z.transpose()
# Pz_d = Pz_d.transpose();
#Pw_z=Pw_z*255/ma

# for k in range(Strokes):
# 	for i in xrange(40):
# 		for j in xrange(40):
# 			P[k][i][j]=Pw_z[k][i*40+j]




print np.amax(Pw_z,axis=0)

# R = np.array(xrange(40))
# R1 = np.tile(R,40)
# R2 = np.repeat(R,40)

# for i in xrange(R1.size):
# 	for j in xrange(R2.size):
# 		print R2[i], R2[j]



# for i in xrange(Strokes):
	
	
# 	plt.xlabel("Position of Pixel");
# 	plt.ylabel("Probability of it being black")
# 	#ax=Axes3D(fig)
# 	plt.figure(figsize=(20,10))
# 	plt.ylim((0,ma))
# 	plt.xlim((0,1600))
# 	plt.scatter(xrange(1600),Pw_z[i])
# 	plt.savefig("Plots/Stroke "+str(i)+" Plot")
# 	#plt.show()
# 	plt.clf()

	

# Avg = np.mean(Pz_d,axis=0)
# Mm  = np.amax(Avg)

# plt.ylim((0,Mm+0.1))
# plt.xlim((0,10))
# plt.scatter(xrange(10),Avg)
# plt.savefig("Plots/StrokeProbability Plot")
# plt.clf




Sum = np.zeros((N,1600),dtype=np.float64)
nD = np.zeros((N),dtype=np.float64)


for i in xrange(N):
	nD[i]=np.sum(termdoc[i])
	for j in xrange(1600):
		for k in xrange(Strokes):
			Sum[i][j]+=Pw_z[k][j]*Pz_d[i][k]
		#print Sum[i][j]/termdoc[i][j]
	termdoc[i]=termdoc[i]/nD[i]
	print np.sum(Pz_d[i])
		

Diff = abs(termdoc-Sum)
print  np.sum(Diff)
