import datetime
from data import graph
from energymonitor import energy_monitor, main_battery

# Every trip taken by the car is stored as an instance of the class below.
class Trip:

    def __init__(self, name, distance, date):
        self.name = name
        self.distance = distance
        self.date = date
    
# This class was part of my original design, but I have not made use of it in this code, due to the implementation
# of Dijkstra's algorithm.
class Location:

    def __init__(self, name, lat_coord, long_coord):
        self.name = name
        self.lat_coord = lat_coord
        self.long_coord = long_coord
    
    def get_coords(self):
        coords = "{}N, {}E".format(self.lat_coord, self.long_coord)
        return coords
    
    def get_name(self):
        return self.name
    

# Besides the UserInterface, the RoutePlanner class is the main operation.
class RoutePlanner:
    trips_taken = {}

    # RoutePlanner is initialized with a copy of the graph dictionary, to avoid manipulation of the original.
    def __init__(self, roads):
        self.original_graph = roads.copy()

    def get_destination(self):
        return input("Where would you like to travel?: ")
    
    def get_origin(self, car):
        return car.get_current_location()

    # Method based on Dijkstra's algorithm to find the shortest route between origin and destination, based on the 'graph' dictionary.
    # When the shortest route has been found and the EnergyMonitor has approved the route, the trip is added ot the 'trips_taken' dictionary.
    # This dictionary is the main source of data for the MaintenanceMonitor class.
    def calculate_route(self, graph, origin, destination):
        unvisited_nodes = self.original_graph.copy()
        # Variable representing infinity is created. This is part of Dijkstra's algorithm. The original distance between nodes is represented as infinity.
        infinity = float("inf")
        distances = {}
        route = []
        path = {}

        for nodes in unvisited_nodes:
            #print(nodes)
            distances[nodes] = infinity
        distances[origin] = 0

        while unvisited_nodes:
            min_node = min(unvisited_nodes, key=distances.get)
            for node, value in unvisited_nodes[min_node].items():
                #print(node)
                if value + distances[min_node] < distances[node]:
                    distances[node] = value + distances[min_node]
                    path[node] = min_node
            unvisited_nodes.pop(min_node)
        node = destination

        while node != origin:
            try:
                route.insert(0, node)
                node = path[node]
            except Exception:
                print("Cannot reach destination!")
                break
        route.insert(0, origin)

        if distances[destination] != infinity:
            approval = self.check_battery(distances[destination])
            if approval:
                trip_num = 1
                while "Trip{}".format(trip_num) in self.trips_taken:
                    trip_num += 1
                trip_name = "Trip{}".format(trip_num)
                trip_date = datetime.datetime.now().strftime("%d/%m/%Y")
                trip_distance = distances[destination]
                trip = Trip(trip_name, trip_distance, trip_date)
                self.trips_taken[trip_name] = {'km': trip.distance, 'date': trip.date}
            return distances[destination], route, approval
    
    # This method also uses Dijkstra's algorithm to calculate the route to the nearest charging station.
    def calculate_charging(self, graph, origin, destination):
        unvisited_nodes = self.original_graph.copy()
        infinity = float("inf")
        distances = {}
        route = []
        path = {}

        for nodes in unvisited_nodes:
            #print(nodes)
            distances[nodes] = infinity
        distances[origin] = 0

        while unvisited_nodes:
            min_node = min(unvisited_nodes, key=distances.get)
            for node, value in unvisited_nodes[min_node].items():
                #print(node)
                if value + distances[min_node] < distances[node]:
                    distances[node] = value + distances[min_node]
                    path[node] = min_node
            unvisited_nodes.pop(min_node)
        node = destination

        while node != origin:
            try:
                route.insert(0, node)
                node = path[node]
            except Exception:
                print("Cannot reach destination!")
                break
        route.insert(0, origin)

        return distances[destination], route

    # This method uses the "calculate_route()" and "calculate_charging()" methods to either tell the user to charge the car,
    # or move the car to the nearest charging station automatically.
    def suggest_charging(self, graph, origin, charging_stations):
        nearest_station = None
        smallest_distance = float("inf")
        for station in charging_stations:
            if origin in charging_stations:
                return "You are next to a charging station. Charge your car before travelling to your desired location!"
            distance, route = self.calculate_charging(graph, origin, station)
            if distance < smallest_distance:
                smallest_distance = distance
                nearest_station = station
            else:
                pass
        charging_approval = self.check_battery(smallest_distance)
        if charging_approval:
            self.calculate_route(graph, origin, nearest_station)
            main_battery.set_current_level(75)
            return "Your car needs to be charged and will be travelling to {}, which is {} km away from here.".format(nearest_station, smallest_distance)
        else:
            return "Your car needs to be charged, but no station is reachable at the moment. Please contact roadside assistance."
        

    def check_battery(self, distance):
        if energy_monitor.route_approval(main_battery, distance):
            return True
        else:
            return False
    
    def get_trips(self):
        return self.trips_taken

route_planner = RoutePlanner(graph)



        
# ---  GENERAL TESTS ---
# The below code was used to test the Route Planner class. To avoid circular imports, I have initialized a version of the class to be used in other files.



# print(route_planner.calculate_route(graph, "The Pearl", "Aspire")) # WORKS
# print(route_planner.suggest_charging(graph, "Corniche", charging_stations)) # WORKS
# print(route_planner.get_trips()) # WORKS
# print(main_battery.get_current_level()) # WORKS


# References (more detail in the ReadMe file):
# I used the following books/articles/websites for the implementation of Dijkstra's Algorithm:
# Grokking Algorithms: An Illustrated Guide for Programmers and Other Curious People by Aditya Bhargava (2016): https://www.amazon.com/Grokking-Algorithms-illustrated-programmers-curious/dp/1617292230/ref=sr_1_4?crid=176VUVU2Z5I9M&keywords=dijkstra+algorithm&qid=1680117245&sprefix=%2Caps%2C647&sr=8-4
# GeeksforGeeks: https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
# Stackabuse: https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/dijkstras-algorithm/
# Algo Daily: https://algodaily.com/lessons/an-illustrated-guide-to-dijkstras-algorithm/python







    
