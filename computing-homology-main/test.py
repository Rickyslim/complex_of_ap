import matlab.engine
import scipy.io as sio
import numpy as np
from numpy import mat
import random
# matrix_first_mat=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/matrix_first.mat'
# first=sio.loadmat(matrix_first_mat)
# matrix_second_mat=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/matrix_second.mat'
# second=sio.loadmat(matrix_second_mat)
# a=first["matrix_first"]
# b=second["matrix_second"]
# c=np.zeros((1,45))
# print(type(c))
# eng=matlab.engine.start_matlab()
ap_pos=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos.mat'
a=sio.loadmat(ap_pos)
ap_radii=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
b=sio.loadmat(ap_radii)
appos=a['APpos']
apradii=b['ap_radii']
mat_appos=matlab.double(appos.tolist())
mat_apradii=matlab.double(apradii.tolist())

a=np.array([0, 7, 5, 31, 32, 41])
b=np.array([1,9])
c=np.intersect1d(a,b)

t=np.array([[1,2,3],[1,2,3],[3,5,8]])
t=np.unique(t,axis=0)
print(t[0,0])






#matrix_first,matrix_second=eng.complex_generator()
