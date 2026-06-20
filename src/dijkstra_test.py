"""dijkstra_test.py  - Is a performance test for Dijkstra's Algorithm.

 Runs Dijkstra's algorithm 10 times on the sample graph loaded from the csv.
  Measures and prints the execution time for each run in milliseconds.
  Prints the average execution time."""

# import pythons time module to measure how long each algorithm takes.
import time
# import custom graph class from graph.py to load graph data and manage nodes/edges.
from graph import Graph
# import the dijkstra algorithm from dijkstra.py
from dijkstra import dijkstra


# define a function to run the Dijkstra's algorithm multiple times.
def run_dijkstra_test():
    # create an instance of the graph class (initially empty)
    graph = Graph()
    # load the graph data from a csv file into the graph instance.
    graph.load_from_csv("data/location_network.csv")

    # define the starting point for the algorithm. all shortest paths will be calculated from this node
    source = "Intersection A"
    # initialize an empty list to store the time in milliseconds of each run.
    times = []

    # loop to run the algorithm 10 times
    for i in range(10):
        # record start time using perf_counter
        start_time = time.perf_counter()
        # run the algorithm on the graph from the source node.
        dijkstra(graph, source)
        # record the end time using perf_counter
        end_time = time.perf_counter()

        # convert to milliseconds b/c time.time() gives seconds as a float so multiply by 1000.
        elapsed = (end_time - start_time) * 1000
        # adds the elapsed time to the times list.
        times.append(elapsed)
        # print the result for this run.
        print(f"Run {i + 1}: {elapsed:.4f} ms")

    # calculate the average execution time
    average = sum(times) / len(times)
    # print the average time in the same format
    print(f"\nAverage Execution Time (Dijkstra): {average:.4f} ms")


# standard python idiom to ensure run_dijkstra_test only runs when this file is executed directly.
if __name__ == "__main__":
    run_dijkstra_test()
