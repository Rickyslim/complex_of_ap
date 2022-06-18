import scipy.io as sio
import numpy as np
import random
import math
from build_complex import complex_builder
from homology import ComputeBettiNumber
from incell_hole import incellhole
from sysSetting import systemSetting
# ————————————————————测试数据——————————————————————

theta=np.linspace(0,2*math.pi,360)
pos=sio.loadmat(u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/pos_test.mat')
radii=sio.loadmat(u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/radii_test.mat')
aplist=sio.loadmat(u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/hole_border_ap_list.mat')
ap_pos=pos['APpos']
ap_radii=radii['ap_radii']
ap_list=aplist['hole_border_ap_list']
node_x=ap_pos[:,0]
node_y=ap_pos[:,1]
node_coor=np.vstack([node_x,node_y])
incell=incellhole()
#将所有AP发射半径设置为最大值
# ap_radii=incell.setmaxradii(ap_pos,2.5,np.size(node_coor,1)-systemSetting.BORDER_AP_NUM)
#获取初始网络拓扑的前两阶贝蒂数
init_bettis=incell.get_init_bettis(ap_pos,ap_radii)
print("初始空洞数: "+str(init_bettis))
# print(len(systemSetting.node_list[0].simp['simp2'][0]['neighb']))
#删除网络拓扑中的冗余节点（在全覆盖的情况下简化复型结构）
# ap_pos,ap_radii=incell.delete_dispensable_node(init_bettis[1],ap_radii,ap_pos)
#簇内的覆盖优化（1、全覆盖；2、功率尽可能小）
# incell.opt_radii(init_bettis[1],ap_radii,ap_pos,ap_list)
#(自选)在存在空洞的情况况下简化复型结构
ap_pos,ap_radii=incell.simplify_init_complex_without_modifying_holes(init_bettis[1],ap_radii,ap_pos,ap_list)




store_path=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
store_path2=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos.mat'
incell.store_results(ap_radii,'ap_radii',store_path)
incell.store_results(ap_pos,'APpos',store_path2)

