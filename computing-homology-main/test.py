import matlab.engine
import scipy.io as sio
import numpy as np
from numpy import mat
import random
import math
from build_complex import complex_builder
from incell_hole import incellhole
from sysSetting import systemSetting
from locate_hole import hole_locator
from cluster import cluster_generator
# matrix_first_mat=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/matrix_first.mat'
# first=sio.loadmat(matrix_first_mat)
# matrix_second_mat=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/matrix_second.mat'
# second=sio.loadmat(matrix_second_mat)
# a=first["matrix_first"]
# b=second["matrix_second"]
# c=np.zeros((1,45))
# print(type(c))
# eng=matlab.engine.start_matlab()
appos=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos_tag.mat'
a=sio.loadmat(appos)
apradii=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
b=sio.loadmat(apradii)
cluster=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/cluster.mat'
c=sio.loadmat(cluster)
ap_pos=a['APpos']
ap_radii=b['ap_radii']
ap_cluster=c['cluster']
systemSetting.cluster=ap_cluster

# ----------------------------------------------
hl=hole_locator()
cg=cluster_generator()
# a=np.array([0, 7, 5, 31, 32, 41])
# b=np.array([1,9])
# c=np.intersect1d(a,b)

# t=np.array([[1,2,3],[1,2,3],[3,5,8]])
# t=np.unique(t,axis=0)
# print(t[0,0])

node_x=ap_pos[:,0]
node_y=ap_pos[:,1]
node_coor=np.vstack([node_x,node_y])
incell=incellhole()
# ap_radii=incell.setmaxradii(np.size(node_coor,1)-systemSetting.BORDER_AP_NUM,2.5)

#将构建复形的结果node_list存入SystemSetting当中
# print(systemSetting.node_list[0].simp['simp2'])
# pos,radii=incell.delete_dispensable_node(init_bettis[1],ap_radii,ap_pos)

# store_path=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii_bp.mat'
# store_path2=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos_bp.mat'
# incell.store_results(pos,'APpos',store_path2)
# incell.store_results(radii,'ap_radii',store_path)
cluster_pos_tmp=np.zeros((45,3))
cluster_radii_tmp=np.zeros((45,1))
for i in range(3):
    cluster=systemSetting.cluster[0][i][0]
    cluster_radii=cg.get_cluster_radii(cluster,ap_radii)
    cluster_pos=cg.get_cluster_ap_pos(cluster,ap_pos)
    # print(cluster_pos,'\n')
    # fence_index=cg.get_cluster_inner_node(cluster_radii)
    cluster_radii=incell.setmaxradii(cluster,2.5,26)
    contour_ap,contour_border=cg.get_cluster_contour(i+1)

    # print(incell.check_contour_border(contour_border,cluster_pos,cluster_radii))
    init_bettis=incell.get_init_bettis(cluster_pos,cluster_radii)
    # print(init_bettis)
    incell.opt_radii(init_bettis[1],cluster_radii,cluster_pos,contour_border)
    cg.merge_to_one(cluster,cluster_pos,cluster_radii,cluster_pos_tmp,cluster_radii_tmp)
store_path=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii_bp.mat'
store_path2=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos_bp.mat'
incell.store_results(cluster_pos_tmp,'APpos',store_path2)
incell.store_results(cluster_radii_tmp,'ap_radii',store_path)