'''merging two sorted list with respect to y'''
def merge(l1,l2):
    l=[]
    n=len(l1)
    m=len(l2)
    i=0
    j=0
    while i<n and j<m:
        if (l1[i][1] <= l2[j][1]):
            l.append(l1[i])
            i+=1
        else:
            l.append(l2[j])
            j+=1
    if i==n:
        while j<m:
            l.append(l2[j])
            j+=1
    if j==m:
        while i<n:
            l.append(l1[i])
            i+=1
    return l

'''Defining a class of Xtree(a node) which is storing element of list as node and a list attached with each node sorted wrt y coordinate'''
class Xtree:
    def __init__(self , key):
        self.key = key
        self.left = None
        self.right = None
        self.ylist = []
        
        
'''Defining our required class'''
class PointDatabase:
    def __init__(self , pointlist):
        self.pointlist = pointlist
        self.sortedX = sorted(self.pointlist)
        self.Build2Dtree(self.sortedX)
    '''construction of our 2D tree'''
    def Build2Dtree(self,data_list):
        if not data_list:
            return None
        # '''clear when one element only'''
        elif len(data_list)==1:
            root = Xtree(data_list[0])
            root.ylist = data_list
            return root
        median = (len(data_list)-1)//2
        root = Xtree(data_list[median])
        '''admitting median element also in the tree'''
        root.left = self.Build2Dtree(data_list[:median+1])
        root.right = self.Build2Dtree(data_list[median+1:])
        '''ylist attached to the root is made of list attached to its child(by merging)'''
        root.ylist = merge(root.left.ylist,root.right.ylist)
        return root

    '''finding first element of interest'''
    def findsplit(self , root , r,i):
        ans=None
        while root is not None:
            if root.key[i] <= r[1] and root.key[i]>=r[0]:
                ans= root
                return ans
                
            elif root.key[i]<r[0]:
                root = root.right
            else:
                root =root.left
        return ans
    
    '''checking whether point is in given range or not'''
    def withinrange_1D(self, r , point , i):
        x = point[i]
        if x<=r[1] and x>=r[0]:
            return True
        return False
    '''checking whether point is in given 2d point range or not'''
    def withinrange_2D(self , rx , ry , point):
        if self.withinrange_1D(rx , point , 0) and self.withinrange_1D(ry , point,1):
            return True
        return False

    '''it is just an binary search to return the list of points in given range of y'''
    def query_1d(self,l,r):
        if not l:
            return l
        higher=r[1]
        lower=r[0]
        n=len(l)
        low=0
        hi=n-1
        lower_index=low
        while(hi>=low):
            mid=(hi+low)//2
            if l[mid][1]>lower:
                hi=mid-1
                lower_index=mid
            elif l[mid][1]<lower:
                low = mid + 1
                lower_index=low
            else:
                lower_index=mid
                break
        low=0
        hi=n-1
        higher_index=low
        while(hi>=low):
            mid=(hi+low)//2
            if l[mid][1]>higher:
                hi=mid-1
                higher_index=hi
            elif l[mid][1]<higher:
                low=mid+1
                higher_index=mid
            else:
                higher_index=mid
                break
        if lower_index<0 or higher_index>=len(l):
            return []
        return l[lower_index:higher_index+1]
    '''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
    
    '''Searching here in root for our query converted as range'''
    def searchNearbyWithroot(self, ans, root,rx, ry):
        # start with vsplit
        vsplit=self.findsplit(root,rx,0)
        if vsplit is None:
            return ans
        #if vsplit is a leaf , no further check is there
        if vsplit.left is None and vsplit.right is None:
            if self.withinrange_2D(rx , ry , vsplit.key):
                ans.append(vsplit.key)
        else:
            #for left side of vsplit
            if vsplit.left is not None:
                vl=vsplit.left
                while vl.left != None or vl.right != None:
                    # check wrt x if is in range
                    if vl.key[0] >=rx[0]:
                        #check in y list and admit those which are in range
                        ans +=self.query_1d(vl.right.ylist , ry)
                        vl = vl.left
                    #if x is less then go for right side
                    else:
                        vl = vl.right
                if self.withinrange_2D(rx , ry , vl.key):
                    ans.append(vl.key)

            #similarly for right side of vsplit if there
            if vsplit.right is not None:
                vr=vsplit.right
                while vr.right != None or vr.left != None:
                    if vr.key[0] <=rx[1]:
                        ans += self.query_1d(vr.left.ylist, ry)
                        vr= vr.right
                    else:
                        vr = vr.left
                if self.withinrange_2D(rx , ry , vr.key):
                    ans.append(vr.key)

        return ans                


    '''searchNearby function method'''
    def searchNearby(self,q,d):
        rx=(q[0]-d, q[0]+d)
        ry=(q[1]-d, q[1]+d)
        root=self.Build2Dtree(self.sortedX)
        '''converting in range and constructing tree and calling the search function'''
        return self.searchNearbyWithroot([],root,rx,ry)
        


