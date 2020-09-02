import numpy as np
class cluster_generator():
    def __init__(self):
        pass
    def get_cluster_radii(self,cluster,ap_radii):
        cluster_radii=ap_radii[cluster[0][0]-1]
        for i in range(1,np.size(cluster,0)):
            cluster_radii=np.vstack((cluster_radii,ap_radii[cluster[i][0]-1]))
        return cluster_radii
    def get_cluster_inner_node(self,cluster_radii):
        for i in range(np.size(cluster_radii,0)):
            if cluster_radii[i]==1.6:
                return i
                break
    def get_cluster_ap_pos(self,cluster,ap_pos):
        cluster_pos=ap_pos[cluster[0][0]-1]
        for i in range(1,np.size(cluster,0)):
            cluster_pos=np.vstack((cluster_pos,ap_pos[cluster[i][0]-1]))
        return cluster_pos
    def merge_to_one(self,cluster,cluster_pos,cluster_radii,cluster_pos_tmp,cluster_radii_tmp):
        for i in range(np.size(cluster,0)):
            cluster_pos_tmp[cluster[i][0]-1]=cluster_pos[i]
            cluster_radii_tmp[cluster[i][0]-1]=cluster_radii[i]
