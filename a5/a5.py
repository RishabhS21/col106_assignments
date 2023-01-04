from math import inf
# to get absolute parent of a vertex, whenever index itself itself is starting
def searchAbsoluteParent(parent, i):
    if parent[i] == i:
        return i
    parent[i]=searchAbsoluteParent(parent, parent[i])
    return parent[i]

# taking union on the basis of rank to avoid high unbalancing of tree
def apply_union(parent, rank, x, y):
    if rank[x] < rank[y]:
        parent[x] = y
    elif rank[x] > rank[y]:
        parent[y] = x
    else:
        parent[y] = x
        rank[x] += 1

# to find a spanning tree corresponding to graph given
def mst(V,graph):
    result = []
    i, e = 0, 0
    graph = sorted(graph, key=lambda item: item[2])
    graph.reverse()
    parent = []
    rank = []
    for node in range(V):
        parent.append(node)
        rank.append(0)
    while e < V - 1:
        u, v, w =graph[i]
        i = i + 1
        x = searchAbsoluteParent(parent, u)
        y = searchAbsoluteParent(parent, v)
        if x != y:
            e = e + 1
            result.append((u, v, w))
            apply_union(parent, rank, x, y)
    
    return result

# making an adjacency list out of given links with spanning tree
def adjacencyList(n,links):
    links = mst(n,links)
    l=[[] for i in range(n)]
    for edge in links:
        l[edge[0]].append((edge[2],edge[1]))
        l[edge[1]].append((edge[2],edge[0]))
    return l

# final function to find max cap and route 
def findMaxCapacity(n, links, s, t):
    l=adjacencyList(n,links)
    routeWithCap=[(inf,s)]
    is_visited=[0 for i in range(n)]
    is_visited[s]=1
    i=0
    while True:
        current=l[routeWithCap[-1][1]][i]
        if routeWithCap[-1][1]==t:
            break
        if not is_visited[current[1]]:
            i=0
            routeWithCap.append(current)
            is_visited[current[1]]=1
        elif is_visited[current[1]] and current==l[routeWithCap[-1][1]][-1]:
            i=0
            routeWithCap.pop()
        else:
            i+=1
    cap=min(routeWithCap, key=lambda item: item[0])[0]
    route=[]
    for v in routeWithCap:
        route.append(v[1])
    return cap ,route
