import osmnx as ox
import networkx as nx

def coordinate2node(G, point):
    return ox.get_nearest_node(G, point)

def get_shortest_distance(G, source_node, target_node):
    route = nx.shortest_path(G, source_node, target_node, weight = 'length')
    length = nx.algorithms.shortest_path_length(G, source=source_node, target=target_node, weight='length', method='dijkstra')
    return (route, length)

class Point:
    def __init__(self, lat, lng):
        self.lng = lng
        self.lat = lat
        self.next = None
    def to_tuple(self):
        return (self.lat, self.lng)
    def to_dic(self):
        return {"latitude": self.lat, "longitude": self.lng}
    def __str__(self):
        return (self.lat, self.lng)
    
class Order:
    def __init__(self, p1, p2):
        self.source = Point(p1[0], p1[1]) # store
        self.target = Point(p2[0], p2[1]) # user address
        self.source.next = self.target
    
class Solution:
    def __init__(self, orders, start, G):
        self.start = start
        self.orders = orders
        self.G = G
        
    def solve(self):
        reachable_point = []
        point_to_be_reach = []
        
        for order in self.orders:
            reachable_point.append(order.source)
            
            point_to_be_reach.append(order.target)
            point_to_be_reach.append(order.source)
        #print(reachable_point)
        #print(point_to_be_reach)
        #return self.solve_helper(reachable_point, point_to_be_reach, self.start)[0]
        return self.greedy_solve_helper(reachable_point, point_to_be_reach, self.start)

    def greedy_solve_helper(self, reachable_point, point_to_be_reach, start):
        res = []
        while(len(point_to_be_reach) > 0):
            if (type(start) != tuple):
                start = start.to_tuple()
            node_start = coordinate2node(self.G, start)
            temp_routes = []
            min_distance = None
            min_point = None
            for i in reachable_point:
                node_i = coordinate2node(self.G, i.to_tuple())
                route, distance = get_shortest_distance(self.G, node_start, node_i)
                if min_distance == None:
                    min_distance = distance
                    continue
                if min_distance > distance:
                    min_distance = distance
                    min_point = i
            if min_point.next != None:
                reachable_point.append(min_point.next)
            point_to_be_reach.remove(min_point)
            res.append(min_point.to_dic())
        return res
        
        
    def solve_helper(self, reachable_point, point_to_be_reach, start):
        if len(point_to_be_reach) == 0:
            return ([],0)
        
        if (type(start) != tuple):
            start = start.to_tuple()
        node_start = coordinate2node(self.G, start)
        temp_routes = []
        for i in reachable_point:

            node_now = []
            node_now.append(i.to_dic())

            node_i = coordinate2node(self.G, i.to_tuple())
            route, distance = get_shortest_distance(self.G, node_start, node_i)
            #print("distance:", distance)
            
            new_reachable_point = reachable_point.copy()
            if (i.next != None):
                new_reachable_point.append(i.next)
            new_reachable_point.remove(i)
            
            new_point_to_be_reach = point_to_be_reach.copy()
            new_point_to_be_reach.remove(i)
            
            temp_route, temp_distance = self.solve_helper(new_reachable_point, new_point_to_be_reach, i)
            temp_routes.append((node_now + temp_route, distance + temp_distance))
        
        min_distance = temp_routes[0][1]
        min_index = 0
        for i in range(len(temp_routes)):
            temp_distance = temp_routes[i][1]
            if temp_distance < min_distance:
                min_index = i
                min_distance = temp_distance
        
        return temp_routes[min_index]

def route_service(order_list, location):
    orders = []
    start = (location["latitude"], location["longitude"])
    for order in order_list:
        store_point = (order["store"]["latitude"], order["store"]["longitude"])
        address_point = (order["address"]["latitude"], order["address"]["longitude"])
        o = Order(store_point, address_point)
        orders.append(o)

    G = ox.graph_from_point(start, distance=5000, simplify=True)
    s = Solution(orders, start, G)
    route = s.solve()
    return route

if __name__ == "__main__":
    o = {"address":{"latitude":31.025633, "longitude":121.437094}, "store":{"latitude":31.021946663170958, "longitude":121.43843164637974}}
    o2 = {"address":{"latitude":31.025533, "longitude":121.439011}, "store":{"latitude":31.017799847991498, "longitude":121.44034661094726}}
    order_list = []
    order_list.append(o)
    order_list.append(o2)
    location = {"latitude":31.025633, "longitude":121.437094}
    res = route_service(order_list, location)
    print(res)
