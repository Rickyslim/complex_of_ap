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
appos=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos.mat'
pos=sio.loadmat(appos)
apradii=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
radii=sio.loadmat(apradii)
ap_pos=pos['APpos']
ap_radii=radii['ap_radii']
node_x=ap_pos[:,0]
node_y=ap_pos[:,1]
node_coor=np.vstack([node_x,node_y])
incell=incellhole()
# ap_radii=incell.setmaxradii(np.size(node_coor,1)-systemSetting.BORDER_AP_NUM,2.5)
init_bettis=incell.get_init_bettis(ap_pos,ap_radii)
print(len(systemSetting.node_list[0].simp['simp2'][0]['neighb']))
#将构建复形的结果node_list存入SystemSetting当中

incell.opt_radii(init_bettis[1],ap_radii,ap_pos)
incell.store_results(ap_radii)


