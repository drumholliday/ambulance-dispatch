"""graph.py - defines the graph class used to represent the roads
Loads the intersections and roads from the data given in the csv files into an adjacency list and an edge dictionary.
Looks up neighbors and calculates the total traffic delay along a given path."""

# import the built-in csv module to read csv files
import csv

# import the defaultdict from Python's collection to
# auto-create a default value if a key doesn't exist yet.
# This is used to create a list of neighbors for each location
from collections import defaultdict


# define the Graph class to represent the road network of addresses, intersections, distances, etc.)
class Graph:
    # constructor (__init__) that sets up an empty graph using a defaultdict where each key will be a location
    # and its value will be a list of (neighbor, weight) pairs.
    def __init__(self):
        self.adj_list = defaultdict(list)
        # track full data for each edge to use in delay calculations.
        self.edges = {}

    # method that reads the graph data from the csv file
    # with the columns Start, End, Travel Time, and Traffic Delay.
    def load_from_csv(self, file_path):
        # open the file at the path that is given to read using 'r' mode.
        with open(file_path, 'r') as csvfile:
            # use DictReader to read each row
            reader = csv.DictReader(csvfile)
            # loop through each row of the csv file
            for row in reader:
                start = row['Start']
                end = row['End']
                # convert travel time to a number
                travel_time = float(row['Travel Time'])
                # Convert traffic delay to a number
                traffic_delay = float(row['Traffic Delay'])
                # travel time plus traffic delay equals total weight
                total_weight = travel_time + traffic_delay
                # add this connection (edge) to the graph adjacency list. (example) 'Intersection A': [('Intersection B', 7.5)]
                self.adj_list[start].append((end, total_weight))

                # save full edge to store complete info for each edge to calculate total delay for a path.
                self.edges[(start, end)] = {
                    "travel_time": travel_time,
                    "traffic_delay": traffic_delay,
                    "total_weight": total_weight
                }

    # method that belongs to the graph class and returns a list of neighbors for a given node (location).
    def get_neighbors(self, node):
        # if the node does not exist return an empty list.
        return self.adj_list.get(node, [])
        # method that returns a list of all starting nodes (keys) in the graph.
    def get_nodes(self):
        return list(self.adj_list.keys())

    # takes a full path or list nodes from ambulance data to call
    # and calculates the total traffic delay along the path by summing the delay for each segment.
    # accepts a list of nodes such as 'A', 'B', 'C', 'D'
    def get_total_delay(self, path):
        # initialize variable total_delay to 0
        total_delay = 0
        # loop through the path one segment at a time.
        for i in range(len(path) - 1):
            # loop through the path one segment at a time from node i to node i + 1
            start = path[i]
            end = path[i + 1]
            # define the start and end for the current edge (ex A -> B, then B -> C)
            edge = (start, end)
            # create a tuple key that matches how edges are stored in self.edges
            if edge in self.edges:
                total_delay += self.edges[edge]["traffic_delay"]
            # check for reverse edge in case the connection between 2 nodes runs in both directions (A -> B but not B -> A)
            else:
                reverse_edge = (end, start)
                # if found add the reverse edge's delay instead.
                # if the forward direction exists then use it, (ex A -> B)
                # otherwise check if the reverse direction exists and use that instead (ex B -> A)
                if reverse_edge in self.edges:
                    total_delay += self.edges[reverse_edge]["traffic_delay"]
        # return the total traffic delay for the full path
        return total_delay
