import numpy as np
import scipy.io as sio
import random
from node import Node
import math
class complex_builder():
    def __init__(self):
        pass
    
    def dist(self,coord1,coord2):
        distance=math.sqrt(math.pow((coord1[0]-coord2[0]),2)+math.pow((coord1[1]-coord2[1]),2))
        return distance

    def complex_generator(self,ap_pos,ap_radii,node_list):  
    # ——————————————————转换ap_pos数据格式为矩阵————————————
        node_x=ap_pos[:,0]
        node_y=ap_pos[:,1]
        node_coor=np.vstack([node_x,node_y])


    # ————————————————————构建一阶复形——————————————————————

        for i in range(np.size(node_coor,1)):
            node=Node()
            node_list.append(node)
            for j in range(np.size(node_coor,1)):
                distance=self.dist(node_coor[:,i],node_coor[:,j])
                if distance<=ap_radii[i]+ap_radii[j]:
                    node_list[i].neighbor.append(j)
                    #找到node(i)的所有邻居节点
        for i in range(np.size(node_coor,1)):
            neighbor_temp1=np.setdiff1d(node_list[i].neighbor,i)
            new_simp={'vert':[i],'neighb':neighbor_temp1}
            node_list[i].simp['simp1']=new_simp
            no_neighb=np.size(neighbor_temp1)
            list_temp=[]#用于向其中添加simp2字典
            list_temp2=[]#用于向其中添加simp3字典
            if no_neighb>0:
                for j in range(no_neighb):
                    new_node=neighbor_temp1[j]
                    vert_set_temp=np.sort(np.array([i,new_node]))
                    neighbor_temp2=np.setdiff1d(node_list[new_node].neighbor,new_node)
                    neighb_set_temp=np.intersect1d(neighbor_temp1,neighbor_temp2)
                    simp_temp={'vert':vert_set_temp,'neighb':neighb_set_temp}
                    list_temp.append(simp_temp)
                node_list[i].simp['simp2']=list_temp
            else:
                node_list[i].simp['simp2']=[]
    # ————————————————构建二阶复形————————————————
            if(node_list[i].simp['simp2']!=[]):
                no_edge=len(node_list[i].simp['simp2'])
                for j in range(no_edge):
                    vert_set=node_list[i].simp['simp2'][j]['vert']
                    neighb_set=node_list[i].simp['simp2'][j]['neighb']
                    if len(neighb_set)!=0:
                        no_neighb=len(neighb_set)
                        for k in range(no_neighb):
                            new_node=neighb_set[k]
                            # 为了避免重复构建，规定三角形三点的序号按照从小到大的顺序排列。
                            if new_node<np.max(np.setdiff1d(vert_set,i)):
                                continue
                            else:
                                vert_set_temp=np.union1d(vert_set,new_node)
                                neighb_set_temp=np.intersect1d(neighb_set,np.setdiff1d(node_list[new_node].neighbor,new_node))
                                simp_temp={'vert':vert_set_temp,'neighb':neighb_set_temp}
                                # 这里的vert字段包含构成二阶复形的三个点
                                list_temp2.append(simp_temp)
                node_list[i].simp['simp3']=list_temp2
                                    
    def find_all_tri(self,node_list):
        tri=np.array([0,0,0])
        for i in range(len(node_list)):
            if len(node_list[i].simp)<3:
                continue
            for j in range(len(node_list[i].simp['simp3'])):
                tri=np.vstack((tri,node_list[i].simp['simp3'][j]['vert']))
        tri=np.unique(tri,axis=0)
        tri=np.delete(tri,0,axis=0)
        return tri

    def find_all_edg(self,node_list):
        edg=np.array([0,0])
        for i in range(len(node_list)):
            for j in range(len(node_list[i].simp['simp2'])):
                # print(node_list[i].simp['simp2'][j]['vert'])
                edg=np.vstack((edg,node_list[i].simp['simp2'][j]['vert']))
        edg=np.unique(edg,axis=0)
        edg=np.delete(edg,0,axis=0)
        return edg

    def border_functor_first(self,edg,ap_num):
        matrix_first=np.zeros((ap_num,np.size(edg,0)))
        for i in range(np.size(edg,0)):
            for j in range(ap_num):
                if j==edg[i,0]:
                    matrix_first[j,i]=-1
                if j==edg[i,1]:
                    matrix_first[j,i]=1
        return matrix_first

    def border_functor_second(self,edg,tri):
        matrix_second=np.zeros((np.size(edg,0),np.size(tri,0)))
        for i in range(np.size(tri,0)):
            for j in range(np.size(edg,0)):
                if edg[j,0]==tri[i,0] and edg[j,1]==tri[i,1]:
                    matrix_second[j,i]=1
                if edg[j,0]==tri[i,0] and edg[j,1]==tri[i,2]:
                    matrix_second[j,i]=-1
                if edg[j,0]==tri[i,1] and edg[j,1]==tri[i,2]:
                    matrix_second[j,i]=1
        return matrix_second