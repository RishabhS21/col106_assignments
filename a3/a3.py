class PointDatabase:
    def __init__(self , pointlist):
        self.pointlist = pointlist
        # self.sortedX = sorted(self.pointlist)
        
    def searchNearby(self,q,d):
        l=[]
        for point in self.pointlist:
            xd=abs(q[0]-point[0])
            yd=abs(q[1]-point[1])
            if xd<d and yd<d:
                l.append(point)
        return l
# pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),
#  (9,2), (10,5)])
# print(pointDbObject.searchNearby((5,5), 1))\
# print(pointDbObject.searchNearby((4,8), 2))
# print(pointDbObject.searchNearby((10,2), 1.5))
