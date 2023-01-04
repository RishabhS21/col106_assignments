# Implementation of heap from scratch
# Storing a list as well which will give position of ith ball in our heap
class MinHeap:
    def __init__(self,n):
        self.data=[]
        self.index_list=[i for i in range(n)]
        
    def parent(self , j):
        return (j-1)//2

    def left(self , j):
        return 2*j+1
    
    def right(self , j):
        return 2*j+2
    
    def has_left(self , j):
        return self.left(j) <len(self.data)
    
    def has_right(self,j):
        return self.right(j)<len(self.data)
    
    def swap(self , j , i):
        self.data[i] , self.data[j] = self.data[j] , self.data[i]
        ind1=self.data[i][1]
        ind2=self.data[j][1]
        self.index_list[ind1],self.index_list[ind2]=self.index_list[ind2],self.index_list[ind1]

    def heapup(self , j):
        while j!=0 and self.data[self.parent(j)]>self.data[j]:
            self.swap(j,self.parent(j))
            j = self.parent(j)
            if j==0:
                break

    def heapdown(self,j):
        currentInd = j
        while self.has_left(currentInd):
            smallInd = self.left(currentInd)
            if self.has_right(currentInd) and self.data[self.right(currentInd)]<self.data[self.left(currentInd)]:
                smallInd = self.right(currentInd)
            if self.data[smallInd] <self.data[currentInd]:
                self.swap(currentInd,smallInd)
                currentInd=smallInd
            else:
                break 

    def insert(self, val):
        self.data.append(val)
        self.heapup(len(self.data)-1)
    
    def heapify(self):
        j = len(self.data)-1
        while(j>=0):
            self.heapdown(j)
            j=j-1
            
    def getMin(self):
        if (len(self.data))==0:
            return None
        return self.data[0]
    
    def extractMin(self):
        if (len(self.data))==0:
            return None
        self.swap(0 , len(self.data)-1)
        ans =  self.data.pop()
        self.heapdown(0)
        return ans

    def updateNode(self,pos,update):
        self.data[pos]=update
        self.heapup(pos)
        self.heapdown(pos)

# infinity is a larger value, we can take any value graeter than T here
infinity=float('inf')
def truncated(n):
    return (n*(10**4)//1)/(10**4)

# "initialHeap" helper function will collect all collisions intially for all corresponding balls (store infinity as time if collision is not possible) 
def initialHeap(x,v):
    
    n=len(x)
    if n==0:
        return None
    H=MinHeap(n-1)
    for i in range(n-1):
        vapp = v[i+1]-v[i]
        if(vapp<0):
            t=(x[i+1]-x[i])/abs(vapp)
            H.data.append((t,i))
        else:
            H.data.append((infinity,i))
    H.heapify()
    return H


# Updating collision of balls (i+1)th and (i-1)th if ith is colliding
def updateNearbyCol(ind,H,x,v,time, time_list):
    index_list=H.index_list
    if (ind>0):
        vapp1=v[ind]-v[ind-1]
        t1=time_list[ind-1]
        if(vapp1<0):
            t=(x[ind]-x[ind-1]-v[ind-1]*(time-t1))/abs(vapp1)
            H.updateNode(index_list[ind-1], (t+time,ind-1))
        else:
            H.updateNode(index_list[ind-1], (infinity,ind-1))

    if (ind < len(v)-2):
        vapp2=v[ind+2]-v[ind+1]
        t2=time_list[ind+2]
        if(vapp2<0):
            t=(x[ind+2]+v[ind+2]*(time-t2)-x[ind+1])/abs(vapp2)
            H.updateNode(index_list[ind+1], (t+time,ind+1))
        else:
            H.updateNode(index_list[ind+1], (infinity,ind+1))
    
    
# Main function will extract minimum time wala coolision and will append it to list with position
# We will update nearby collisions of ith ball
def listCollisions(M,x,v,m,T):
    l=[]
    latest_time_wrt_index=[0]*((len(M)))
    collision_count=0
    time = 0
    H=initialHeap(x, v)
    if H==None:
        return l
    while collision_count<m and time<T:
        col = H.extractMin()
        if(col[0]>T):
            break
        else:
            collision_count+=1
            time=col[0]
            ind = col[1]
            v1=v[ind]
            v2=v[ind+1]
            latest_time1=latest_time_wrt_index[ind]
            latest_time2=latest_time_wrt_index[ind+1]           
            H.insert((infinity,ind))
            latest_time_wrt_index[ind]=latest_time_wrt_index[ind+1]=time
            x[ind]=x[ind+1]=x[ind]+v[ind]*(time-latest_time1)
            l.append(((time),ind,(x[ind])))           
            v[ind]= ((M[ind]-M[ind+1])*v1 +2*M[ind+1]*v2)/(M[ind]+M[ind+1])
            v[ind+1]= ((2*M[ind]*v1)-((M[ind]-M[ind+1])*v2)) /(M[ind]+M[ind+1])
            updateNearbyCol(ind,H,x,v,time,latest_time_wrt_index)
    return l  

    
