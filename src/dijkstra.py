"""dijkstra.py - Implements Dijkstra's algorithm to find the shortest path in a network.

The model has 2 functions:
dijkstra()- calculates the shortest distance from a starting node to all other nodes.
dijkstra_path()- finds the shortest path and total distance between a start and end node,
    and reconstructs the path itself.
Both functions use a priority queue implemented as a mini-heap using Python's heapq."""

# import heapq which is pythons built in priority que model which implements a mini-heap.
import heapq


# define the dijkstra function to compute the shortest distance from a start_node to all other nodes in the graph.
def dijkstra(graph, start_node):
    # initialize all distances to infinity
    distances = {node: float('inf') for node in graph.get_nodes()}
    # set distance from the starting node to itself as 0 b/c we are already there.
    distances[start_node] = 0
    # initialize a variable pq (for priority queue) so the one with the smallest distance always comes first
    # pq is a list of places to visit, and pq is set to start_node and has gone 0 distance (1 tuple).
    pq = [(0, start_node)]

    # keep looping as long as there are nodes to visit in the queue
    while pq:
        # initialized variables for current distance and current node
        # get the node with the shortest distance so far from the heap
        # using the built-in function heapq.heappop() and pop the node with the smallest distance .
        current_distance, current_node = heapq.heappop(pq)

        # if a shorter path has already been found skip the node
        if current_distance > distances[current_node]:
            continue

        # updated get neighbors[current_node] to get neighbors(current_node) b/c Graph is a custom class
        # that does not support subscript access. The method returns a list of (neighbor, weight) tuples for this node,
        for neighbor, weight in graph.get_neighbors(current_node):
            # calculate how far the neighbor is by adding current node's distance to weight of the edge to the neighbor.
            distance = current_distance + weight
            # if the new distance is shorter than what the currently stored distance then update it.
            if distance < distances[neighbor]:
                # update if shorter path
                distances[neighbor] = distance
                # add neighbor back into the queue and check its neighbors later.
                heapq.heappush(pq, (distance, neighbor))
    # return a dictionary with the shortest distance to every node
    return distances


# define a function called dijkstra_path that takes graph, start_node, end_node
def dijkstra_path(graph, start_node, end_node):
    # create a dictionary called distances to hold the shortest travel time from start node to all other nodes.
    distances = {node: float('inf') for node in graph.get_nodes()}
    # keep track of the path taken to each node, initialize the previous node as None, Used later to reconstruct the actual path.
    previous_nodes = {node: None for node in graph.get_nodes()}
    # starting point set to 0 travel time since we are currently there.
    distances[start_node] = 0
    # create pq (priority queue) with start_node at a distance of 0.
    # this is the foundation of Dijkstra's greedy algorithm always picking the next shortest path.
    pq = [(0, start_node)]

    while pq:
        # current_distance is how far we have traveled to get to that point.
        # current_node is the location we're exploring
        # heappop removes and returns the node with the shortest time so far.
        current_distance, current_node = heapq.heappop(pq)

        # if we have reached the destination node we can stop.
        if current_node == end_node:
            break
        # if we have already found a shorter path to current_node then skip this to avoid reprocessing a longer path.
        if current_distance > distances[current_node]:
            continue
        # each neighbor comes with a weight which in graph.py 33 is total_weight is travel_time + traffic_delay
        # get all directly connected neighbors of the current_node
        for neighbor, total_weight in graph.get_neighbors(current_node):
            # calculate the total distance to reach this neighbor from the current_node
            distance = current_distance + total_weight
            # if the new path is shorter (less than any previous path) to this neighbor, update.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # record how we reached this neighbor and use later to reconstruct the shortest path.
                previous_nodes[neighbor] = current_node
                # add the neighbor to the pq to check its neighbors later. the queue sorts nodes by shortest distance.
                # heapq.heappush inserts the neighbor with the updated distance.
                heapq.heappush(pq, (distance, neighbor))

    # reconstruct the shortest path by going backward from end_node to start_node using previous_nodes
    # store the shortest path from start_node to end_node
    path = []
    # start going backwards from end_node using previous_nodes
    node = end_node
    while node is not None:
        # insert each node at the front of the list to build a path from start to end.
        path.insert(0, node)
        # move one step backwards on the shortest path.
        node = previous_nodes[node]
    # return the path (a list of nodes from the start_node to the end_node) and the total distance.
    return path, distances[end_node]
