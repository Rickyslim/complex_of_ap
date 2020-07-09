import numpy as np
import math
import scipy.io as sio
import random
from node import Node
from homology import ComputeBettiNumber

# ————————————————————模型初始化——————————————————————
theta=np.linspace(0,2*math.pi,360)
ap_num=25
node_list=[]
# extend_ap=int(math.pow(math.ceil(math.sqrt(ap_num)),2))
# ap_radii=np.random.uniform(1.5,2.5,extend_ap+20)
appos=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_pos.mat'
pos=sio.loadmat(appos)
apradii=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/ap_radii.mat'
radii=sio.loadmat(apradii)
ap_pos=pos['APpos']
ap_radii=radii['ap_radii']
# ————————————————————————————————————————————————
'''
def ap_pos_generator(ap_num,ap_radii):
    extend_ap=int(math.pow(math.ceil(math.sqrt(ap_num)),2))
    extra_ap=extend_ap-ap_num
    ap_pos=np.zeros((ap_num,2))
    for i in range(ap_num,extend_ap+20):
        ap_radii[i]=1.6
    for j in range(1,extend_ap):
        ap_pos[j-1,0]=(j-1)%(math.sqrt(extend_ap))*(15/math.sqrt(extend_ap))+1
        ap_pos[j-1,1]=math.floor((j-1)/math.sqrt(extend_ap))*(15/math.sqrt(extend_ap))+1     
    delete_ap=np.random.randint(0,extend_ap-1,extend_ap-ap_num)
    for i in range(1,np.size(delete_ap)):
        ap_pos=np.delete(ap_pos,i,axis=0)
        ap_radii=np.delete(ap_radii,i,axis=0)
    
#————————————————创建边界——————————————————————————
    topx=np.array([np.linspace(0,15,6)])
    topy=np.array([[15,15,15,15,15,15]])
    top=np.hstack((topx.T,topy.T))
    lefty=np.array([np.linspace(0,12,5)])
    leftx=np.array([[0,0,0,0,0]])
    left=np.hstack((leftx.T,lefty.T))
    righty=np.array([np.linspace(0,12,5)])
    rightx=np.array([[15,15,15,15,15]])
    right=np.hstack((rightx.T,righty.T))
    bottomx=np.array([np.linspace(3,12,4)])
    bottomy=np.array([[0,0,0,0]])
    bottom=np.hstack((bottomx.T,bottomy.T))
    ap_pos=np.vstack([ap_pos,top])
    ap_pos=np.vstack([ap_pos,left])
    ap_pos=np.vstack([ap_pos,right])
    ap_pos=np.vstack([ap_pos,bottom])
    
# ——————————————————调整AP位置——————————————————
    for i in range(1,ap_num):
        ap_pos[i-1,0]=ap_pos[i-1,0]+np.random.random()-0.5
        ap_pos[i-1,1]=ap_pos[i-1,1]+np.random.random()-0.5
    return ap_pos    
'''
def dist(coord1,coord2):
    distance=math.sqrt(math.pow((coord1[0]-coord2[0]),2)+math.pow((coord1[1]-coord2[1]),2))
    return distance

def complex_generator(ap_pos,ap_num,ap_radii):  
# ——————————————————转换ap_pos数据格式为矩阵————————————
    node_x=ap_pos[:,0]
    node_y=ap_pos[:,1]
    node_coor=np.vstack([node_x,node_y])


# ————————————————————构建一阶复形——————————————————————

    for i in range(np.size(node_coor,1)):
        node=Node()
        node_list.append(node)
        if i>len(node_coor)-ap_num:
            node_list[i].flag=1
        for j in range(np.size(node_coor,1)):
            distance=dist(node_coor[:,i],node_coor[:,j])
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
                                
def find_all_tri(node_list):
    tri=np.array([0,0,0])
    for i in range(len(node_list)):
        if len(node_list[i].simp)<3:
            continue
        for j in range(len(node_list[i].simp['simp3'])):
            tri=np.vstack((tri,node_list[i].simp['simp3'][j]['vert']))
    tri=np.unique(tri,axis=0)
    tri=np.delete(tri,0,axis=0)
    return tri

def find_all_edg(node_list):
    edg=np.array([0,0])
    for i in range(len(node_list)):
        for j in range(len(node_list[i].simp['simp2'])):
            # print(node_list[i].simp['simp2'][j]['vert'])
            edg=np.vstack((edg,node_list[i].simp['simp2'][j]['vert']))
    edg=np.unique(edg,axis=0)
    edg=np.delete(edg,0,axis=0)
    return edg

def border_functor_first(edg,ap_num):
    matrix_first=np.zeros((ap_num,np.size(edg,0)))
    for i in range(np.size(edg,0)):
        for j in range(ap_num):
            if j==edg[i,0]:
                matrix_first[j,i]=-1
            if j==edg[i,1]:
                matrix_first[j,i]=1
    return matrix_first

def border_functor_second(edg,tri):
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



                

def main():
    # ap_pos=ap_pos_generator(ap_num,ap_radii)
    
    node_x=ap_pos[:,0]
    node_y=ap_pos[:,1]
    # ap_radii[4][0]=1.5
    # ap_radii[1][0]=1.5
    # ap_radii[9][0]=1.5
    complex_generator(ap_pos,ap_num,ap_radii)

    # for i in node_list:
    #     print(i.simp['simp2'])
    print("bitch",len(node_list))
    tri=find_all_tri(node_list)
    # print(np.size(tri,0))
    edg=find_all_edg(node_list)
    # print(edg)

    matrix_first=border_functor_first(edg,len(node_list))
    matrix_second=border_functor_second(edg,tri)
    print(np.size(matrix_first,0),np.size(matrix_first,1))
    matrix_zero=np.zeros((1,len(node_list)))
    print("————————————————————————The 1st and 2nd Betti Numbers are:————————————————————")
    print("——————0th homology: %d" % ComputeBettiNumber.bettiNumber(matrix_zero.astype('float'),matrix_first.astype('float')))
    print("——————1st homology: %d" % ComputeBettiNumber.bettiNumber(matrix_first.astype('float'),matrix_second.astype('float')))
    
if __name__ == '__main__':
    main()