import numpy as np
from sysSetting import systemSetting
class hole_locator():
    def __init__(self):
        self.visited = []
        self.trace = []
        self.has_circle = False

    def find_hole_border_point(self,node_num,node_list):
        hole_border_ap=np.array([0])
        hole_border_edge=np.array([0,0])
        for i in range(len(node_list[node_num].simp['simp2'])):
            if len(node_list[node_num].simp['simp2'][i]['neighb'])<2:
                hole_border_ap=np.vstack((hole_border_ap,np.setdiff1d(node_list[node_num].simp['simp2'][i]['vert'],node_num)))
                hole_border_edge=np.vstack((hole_border_edge,node_list[node_num].simp['simp2'][i]['vert']))
        hole_border_ap=np.delete(hole_border_ap,0,axis=0)
        hole_border_edge=np.delete(hole_border_edge,0,axis=0)
        return hole_border_ap,hole_border_edge

    def find_hole_border(self,node_list,apnum):
        hole_border_ap_list=np.array([0])
        hole_border_edg_list=np.array([0,0])
        for i in range(len(node_list)):
            hole_border_ap,hole_border_edg=self.find_hole_border_point(i,node_list)
            if hole_border_ap.size!=0:
                hole_border_ap_list=np.vstack((hole_border_ap_list,hole_border_ap))
                hole_border_edg_list=np.vstack((hole_border_edg_list,hole_border_edg))    
        hole_border_ap_list=np.delete(hole_border_ap_list,0,axis=0)
        hole_border_edg_list=np.delete(hole_border_edg_list,0,axis=0)
        hole_border_ap_list=np.unique(hole_border_ap_list,axis=0)
        delete_border=np.where(hole_border_ap_list>apnum)
        hole_border_ap_list=np.delete(hole_border_ap_list,delete_border[0],axis=0)
        hole_border_edg_list=np.unique(hole_border_edg_list,axis=0)
        delete_border=np.where(hole_border_edg_list[:,0]>apnum)
        hole_border_edg_list=np.delete(hole_border_edg_list,delete_border[0],axis=0)
        for i in range(np.size(hole_border_edg_list,0)):
            if hole_border_edg_list[i,1] not in hole_border_ap_list:
                hole_border_ap_list=np.vstack([hole_border_ap_list,hole_border_edg_list[i,1]])
        return hole_border_ap_list,hole_border_edg_list
    
    def find_neighbor(self,apno,hole_border_edg_list):
        neighb=[]
        for i in range(np.size(hole_border_edg_list,0)):
            if apno in hole_border_edg_list[i,:].tolist():
                neighb.extend(np.setdiff1d(hole_border_edg_list[i,:],apno).tolist())
        return neighb
    
    def dfs(self,node_index,hole_border_edg_list,visited,trace,has_circle):

        if (node_index in visited):
            if (node_index in trace):
                has_circle = True
                trace_index = trace.index(node_index)
                for i in range(trace_index, len(trace)):
                    print(str(trace[i]) + ' ', end='')
                print('\n', end='')
                return
            return
    
        visited.append(node_index)
        trace.append(node_index)
        if(node_index !=''):
            neighbor = self.find_neighbor(node_index,hole_border_edg_list)
            for neighb in neighbor:
                self.dfs(neighb,hole_border_edg_list,visited,trace,has_circle)
        trace.pop()
    
    def classify_border_ap(self,hole_border_edg_list):
        visited=[]
        trace=[]
        has_circle=False
        self.dfs(0,hole_border_edg_list,visited,trace,has_circle)
        if(has_circle==True):
            print('bish u got it!')
    
    def bitch(self):
        self.visited.append('caonima!')