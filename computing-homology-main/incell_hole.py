from sysSetting import systemSetting
import scipy.io as sio
import numpy as np
import random
import math
from build_complex import complex_builder
from homology import ComputeBettiNumber
class incellhole():
    # 将半径设置为最大值
    def setmaxradii(self,ap_num,maximum_radii,fence_tag):
        # total_ap=ap_num+systemSetting.BORDER_AP_NUM
        max_radii=np.zeros((ap_num,1))
        for i in range(fence_tag):
            max_radii[i][0]=maximum_radii
        for i in range(fence_tag,ap_num):
            max_radii[i][0]=systemSetting.BORDER_AP_RADII
        return max_radii
        
    # 输入点坐标和对应半径，构造Rips复形
    def get_complex(self,ap_pos,ap_radii):
        node_list=[]
        cp_builder=complex_builder()
        cp_builder.complex_generator(ap_pos,ap_radii,node_list)
        tri=cp_builder.find_all_tri(node_list)
        edg=cp_builder.find_all_edg(node_list)
        matrix_first=cp_builder.border_functor_first(edg,len(node_list))
        matrix_second=cp_builder.border_functor_second(edg,tri)
        matrix_zero=np.zeros((1,len(node_list)))
        first_betti_number=ComputeBettiNumber.bettiNumber(matrix_zero.astype('float'),matrix_first.astype('float'))
        second_betti_number=ComputeBettiNumber.bettiNumber(matrix_first.astype('float'),matrix_second.astype('float'))
        return first_betti_number,second_betti_number,node_list

    # 获取初始化复形的前两位贝蒂数
    def get_init_bettis(self,ap_pos,ap_radii):
        first_betti_init,second_betti_init,node_list=self.get_complex(ap_pos,ap_radii)
        init_bettis=[first_betti_init,second_betti_init]
        # systemSetting.node_list=node_list
        self.set_border_ap_tag(node_list)
        return init_bettis

    def set_border_ap_tag(self,node_list):
        for i in range(len(node_list)-systemSetting.BORDER_AP_NUM):
            node_list[i].flag=1

    # 检查调整过某一AP半径后，贝蒂数是否发生改变
    def examine_betti_numbers(self,pre_betti,ap_pos,ap_radii):
        first_betti_number,second_betti_number,node_list=self.get_complex(ap_pos,ap_radii)
        if first_betti_number!=1 or second_betti_number!=pre_betti:
            # print(first_betti_number,second_betti_number)
            return False
        # print(second_betti_init,second_betti_number)
        # pre_betti=second_betti_number
        return True

    def examine_betti_numbers_for_simplify(self,pre_betti,ap_pos,ap_radii):
        first_betti_number,second_betti_number,node_list=self.get_complex(ap_pos,ap_radii)
        if first_betti_number!=1 or second_betti_number>pre_betti:
            # print(first_betti_number,second_betti_number)
            return False
        # print(second_betti_init,second_betti_number)
        # pre_betti=second_betti_number
        return True
        

    def opt_radii(self,pre_betti,ap_radii,ap_pos,fence_index):
        t=systemSetting.T0
        for i in range(100):
            t=t*0.95
            if t<=5:
                break
            print("温度变化:",t)
            for j in range(100):
                ap_selected=np.random.randint(0,fence_index,1)
                # sign=random.choice([-1,1])
                # if sign==-1:
                if ap_radii[ap_selected[0]][0]>1.6:
                    ap_radii[ap_selected[0]][0]-=0.1
                # print(ap_selected,ap_radii[ap_selected[0]][0],"radii-0.1")
                if not self.examine_betti_numbers(pre_betti,ap_pos,ap_radii):
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
    def delete_dispensable_node(self,pre_betti,ap_radii,ap_pos):
        for i in range(np.size(ap_pos,0)):
            if i>25:
                break
            ap_pos_tmp=ap_pos[i]
            ap_radii_tmp=ap_radii[i]
            ap_pos=np.delete(ap_pos,i,axis=0)
            ap_radii=np.delete(ap_radii,i,axis=0)
            if not self.examine_betti_numbers_for_simplify(pre_betti,ap_pos,ap_radii):
                ap_pos=np.insert(ap_pos,i,values=ap_pos_tmp,axis=0)
                ap_radii=np.insert(ap_radii,i,values=ap_radii_tmp,axis=0)
            else:
                print('deleted',i)
        return ap_pos,ap_radii
    def store_results(self,var,var_name,store_path):
        try:
            sio.savemat(store_path,{var_name:var})
            print("结果已写入")
        except:
            print("写入失败")



