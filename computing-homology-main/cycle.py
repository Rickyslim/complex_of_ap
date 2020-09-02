# from copy import deepcopy as dc

# # 用集合去除重复路径
# ans = set()

# def dfs(graph,trace,start):
#     trace = dc(trace)  # 深拷贝，对不同起点，走过的路径不同
#     # print(trace)
#     # 如果下一个点在trace中，则返回环
#     if start in trace:
#         index = trace.index(start)
#         tmp = [str(i) for i in trace[index:]]
#         ans.add( str(' '.join(tmp)))
#         print(trace[index:])
#         return

#     trace.append(start)

#     # 深度优先递归递归
#     for i in graph[start]:
#         dfs(graph,trace,i)
 
# # graph = {1: [2,33], 2: [1,7], 33:[1,6],6:[33,7],7: [2,6,8,12], 8: [7,13],
# #                 13: [8,12], 12: [13,7,17,16], 16: [12,21],17:[12,21],21:[16,17]}  # 包含大小环test图
# graph = {8:[9,13],9:[8,13],13:[9,18,19],18:[13,19],19:[19,18,20],20:[19]}  # 包含大小环test图

# dfs(graph,[],8)

# print(ans)
#Python3.6
class point(): #定义类
    def __init__(self,x,y):
        self.x=x
        self.y=y   

def cross(p1,p2,p3):#跨立实验
    x1=p2.x-p1.x
    y1=p2.y-p1.y
    x2=p3.x-p1.x
    y2=p3.y-p1.y
    print(x1)
    print(y1)
    print(x2)
    print(y2)
    print()
    return x1*y2-x2*y1     

def IsIntersec(p1,p2,p3,p4): #判断两线段是否相交

    #快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
    if(max(p1.x,p2.x)>=min(p3.x,p4.x)    #矩形1最右端大于矩形2最左端
    and max(p3.x,p4.x)>=min(p1.x,p2.x)   #矩形2最右端大于矩形最左端
    and max(p1.y,p2.y)>=min(p3.y,p4.y)   #矩形1最高端大于矩形最低端
    and max(p3.y,p4.y)>=min(p1.y,p2.y)): #矩形2最高端大于矩形最低端

    #若通过快速排斥则进行跨立实验

        if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0
           and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
            D=1
        else:
            D=0
    else:
        D=0
    return D

p1=point(7.6110   , 7.1534)
p2=point(9.3658   , 6.4799)
p3=point(9.1192   ,10.3639)
p4=point(9.0611    ,4.4881)
print(cross(p1,p2,p3))
print(cross(p1,p2,p4))
print(cross(p3,p4,p1))
print(cross(p3,p4,p2))
r=IsIntersec(p1,p2,p3,p4)
# print(r)

