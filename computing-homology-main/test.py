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
pos=sio.loadmat(u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos.mat')
radii=sio.loadmat(u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat')
aplist=sio.loadmat(u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/hole_border_ap_list.mat')
ap_pos=pos['APpos']
ap_radii=radii['ap_radii']
ap_list=aplist['hole_border_ap_list']
node_x=ap_pos[:,0]
node_y=ap_pos[:,1]
node_coor=np.vstack([node_x,node_y])
incell=incellhole()
#将所有AP发射半径设置为最大值
# ap_radii=incell.setmaxradii(np.size(node_coor,1)-systemSetting.BORDER_AP_NUM,2.5)
#获取初始网络拓扑的前两阶贝蒂数
init_bettis=incell.get_init_bettis(ap_pos,ap_radii)
print(init_bettis)
print(ap_list)
print(ap_pos[:,2])