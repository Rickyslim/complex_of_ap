import scipy.io as sio
import numpy as np
import random
import math
from build_complex import complex_builder
from homology import ComputeBettiNumber
from incell_hole import incellhole
# ————————————————————测试数据——————————————————————
theta=np.linspace(0,2*math.pi,360)
ap_num=25
# extend_ap=int(math.pow(math.ceil(math.sqrt(ap_num)),2))
# ap_radii=np.random.uniform(1.5,2.5,extend_ap+20)
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
ap_radii=incell.setmaxradii(ap_num,2.5)
init_bettis=incell.get_init_bettis(ap_pos,ap_num,ap_radii)
incell.opt_radii(init_bettis[1],ap_radii,ap_pos,ap_num)
incell.store_results("bish")


# ————————————————————————————————————————————————
# def setmaxradii(ap_pos,maximum_radii):
#     max_radii=np.zeros((np.size(ap_pos,0),1))
#     for i in range(np.size(ap_pos,0)-20):
#         max_radii[i][0]=maximum_radii
#     for i in range(25,45):
#         max_radii[i][0]=1.6
#     return max_radii

# def get_complex(ap_pos,ap_num,ap_radii):
#     node_list=[]
#     cp_builder=complex_builder()
#     cp_builder.complex_generator(ap_pos,ap_num,ap_radii,node_list)
#     tri=cp_builder.find_all_tri(ap_num,node_list)
#     edg=cp_builder.find_all_edg(ap_num,node_list)
#     matrix_first=cp_builder.border_functor_first(edg,ap_num+20)
#     matrix_second=cp_builder.border_functor_second(edg,tri)
#     matrix_zero=np.zeros((1,45))
#     first_betti_number=ComputeBettiNumber.bettiNumber(matrix_zero.astype('float'),matrix_first.astype('float'))
#     second_betti_number=ComputeBettiNumber.bettiNumber(matrix_first.astype('float'),matrix_second.astype('float'))
#     return first_betti_number,second_betti_number,node_list

# def examine_betti_numbers(pre_betti,ap_pos,ap_num,ap_radii):
#     first_betti_number,second_betti_number,node_list=get_complex(ap_pos,ap_num,ap_radii)
#     if first_betti_number!=1 or second_betti_number>pre_betti:
#         # print(first_betti_number,second_betti_number)
#         return False
    
#     # print(second_betti_init,second_betti_number)
#     pre_betti=second_betti_number
#     return True
# # ————————————————初始化————————————————
# # ap_radii=setmaxradii(ap_pos,3.0)
# first_betti_init,second_betti_init,node_list=get_complex(ap_pos,ap_num,ap_radii)
# init_bettis=[first_betti_init,second_betti_init]
# max_radii=setmaxradii(ap_pos,2.5)

# # ap_radii[4][0]=1.5
# # ap_radii[1][0]=1.5
# # ap_radii[9][0]=1.5

# # c,d,e=get_complex(ap_pos,ap_num,ap_radii)
# # print(c,d)
# def opt_radii(ap_radii,ap_pos,ap_num):
#     t=100
#     for i in range(100):
#         t=t*0.95
#         if t<=5:
#             break
#         print("温度变化:",t)
#         for j in range(200):
#             ap_selected=np.random.randint(0,25,1)
#             sign=random.choice([-1,1])
#             if sign==-1:
#                 ap_radii[ap_selected[0]][0]-=0.1
#                 print(ap_selected,ap_radii[ap_selected[0]][0],"radii-0.1")
#                 if not examine_betti_numbers(init_bettis[1],ap_pos,ap_num,ap_radii):
#                     print("我不改了")
#                     ap_radii[ap_selected[0]][0]+=0.1
#                     print(ap_selected,ap_radii[ap_selected[0]][0])
#                 # else:
#                 #     print("接受这个改动！")
#             # else:
#             #     if ap_radii[ap_selected[0]][0]<2.5:
#             #         p=math.pow(ap_radii[ap_selected[0]][0]+0.1,2)-math.pow(ap_radii[ap_selected[0]][0],2)
#             #         if np.random.uniform(0,1)<math.exp(p/t*-1):
#             #             # print("当前p：",p)
#             #             # print("接受概率：",math.exp((p*60)/t*-1))
#             #             ap_radii[ap_selected[0]][0]+=0.1
            
#     store_path=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
#     try:
#         sio.savemat(store_path,{'ap_radii':ap_radii})
#         print("结果已写入")
#     except:
#         print("写入失败")
# opt_radii(max_radii,ap_pos,ap_num)    