from sysSetting import systemSetting
import scipy.io as sio
import numpy as np
import random
import math
from build_complex import complex_builder
from homology import ComputeBettiNumber
class incellhole():
    # 将半径设置为最大值
    def setmaxradii(self,ap_num,maximum_radii):
        total_ap=ap_num+systemSetting.BORDER_AP_NUM
        print(total_ap)
        max_radii=np.zeros((total_ap,1))
        for i in range(ap_num):
            max_radii[i][0]=maximum_radii
        for i in range(ap_num,total_ap):
            max_radii[i][0]=systemSetting.BORDER_AP_RADII
        return max_radii
        
    # 输入点坐标和对应半径，构造Rips复形
    def get_complex(self,ap_pos,ap_num,ap_radii):
        node_list=[]
        cp_builder=complex_builder()
        cp_builder.complex_generator(ap_pos,ap_num,ap_radii,node_list)
        tri=cp_builder.find_all_tri(ap_num,node_list)
        edg=cp_builder.find_all_edg(ap_num,node_list)
        matrix_first=cp_builder.border_functor_first(edg,ap_num+20)
        matrix_second=cp_builder.border_functor_second(edg,tri)
        matrix_zero=np.zeros((1,45))
        first_betti_number=ComputeBettiNumber.bettiNumber(matrix_zero.astype('float'),matrix_first.astype('float'))
        second_betti_number=ComputeBettiNumber.bettiNumber(matrix_first.astype('float'),matrix_second.astype('float'))
        return first_betti_number,second_betti_number,node_list

    # 获取初始化复形的前两位贝蒂数
    def get_init_bettis(self,ap_pos,ap_num,ap_radii):
        first_betti_init,second_betti_init,node_list=self.get_complex(ap_pos,ap_num,ap_radii)
        init_bettis=[first_betti_init,second_betti_init]
        return init_bettis

    # 检查调整过某一AP半径后，贝蒂数是否发生改变
    def examine_betti_numbers(self,pre_betti,ap_pos,ap_num,ap_radii):
        first_betti_number,second_betti_number,node_list=self.get_complex(ap_pos,ap_num,ap_radii)
        if first_betti_number!=1 or second_betti_number>pre_betti:
            # print(first_betti_number,second_betti_number)
            return False
        # print(second_betti_init,second_betti_number)
        pre_betti=second_betti_number
        return True

    def opt_radii(self,pre_betti,ap_radii,ap_pos,ap_num):
        t=systemSetting.T0
        for i in range(100):
            t=t*0.95
            if t<=5:
                break
            print("温度变化:",t)
            for j in range(200):
                ap_selected=np.random.randint(0,25,1)
                sign=random.choice([-1,1])
                if sign==-1:
                    ap_radii[ap_selected[0]][0]-=0.1
                    # print(ap_selected,ap_radii[ap_selected[0]][0],"radii-0.1")
                    if not self.examine_betti_numbers(pre_betti,ap_pos,ap_num,ap_radii):
                        # print("我不改了")
                        ap_radii[ap_selected[0]][0]+=0.1
                        # print(ap_selected,ap_radii[ap_selected[0]][0])
                    # else:
                    #     print("接受这个改动！")
                # else:
                #     if ap_radii[ap_selected[0]][0]<2.5:
                #         p=math.pow(ap_radii[ap_selected[0]][0]+0.1,2)-math.pow(ap_radii[ap_selected[0]][0],2)
                #         if np.random.uniform(0,1)<math.exp(p/t*-1):
                #             # print("当前p：",p)
                #             # print("接受概率：",math.exp((p*60)/t*-1))
                #             ap_radii[ap_selected[0]][0]+=0.1
    def store_results(self,store_path):
        store_path=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
        try:
            sio.savemat(store_path,{'ap_radii':ap_radii})
            print("结果已写入")
        except:
            print("写入失败")


