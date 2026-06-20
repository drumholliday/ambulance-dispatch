"""main.py is the entry point for the ambulance dispatch prototype using Dijkstra's algorithm.

 - Loads the data from the given csv files.
 - Uses the algorithm to compute the shortest paths.
 - Uses graph.py to model locations and calculate traffic delays.
 - Assigns ambulances to calls based on the shortest path and the priority each call type is given.
 - Logs the results and the total amount of time the algorithm ran, the total time computing the routes,
   the average time per route, and the total time spent on all route calculations"""

# import time to measure time performance using time_perf_counter() for high rez timing.
import time
# import os to ensure the log file exists when creating the output file.
import os
# import csv to read files
import csv
# import load_ambulances, load_calls from dispatch.py
from dispatch import load_ambulances, load_calls
# import graph data
from graph import Graph
# NEW import dijkstra_path
from dijkstra import dijkstra_path


# load priority calls from call_priority,csv
def load_call_priorities(file_path):
    # initialize an empty dictionary called priorities,
    # will eventually store the mapping between call type and its numeric priority.
    priorities = {}
    # opens the csv file specified by file_path for reading and newline="" for
    # reading csv files to avoids line breaks etc.
    with open(file_path, newline="") as csvfile:
        # call_priority uses commas so using a delimiter set =','
        reader = csv.DictReader(csvfile, delimiter=',')
        print("Detected headers:", reader.fieldnames)
        # loop through each row in the file, each row is a dictionary w/ keys Call Type and Priority
        for row in reader:
            # clean_row used as a precautionary measure to clean up the keys and values (k) and (v) from each row in the csv file.
            # k.strip() removes whitespace from column headers
            # v.strip() removes whitespace from actual data in each field.
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            # take in string Call Type and convert the string Priority into an integer, add to the priority dictionary
            priorities[clean_row['Call Type']] = int(clean_row['Priority'])
    # return the final dictionary
    return priorities


# define a main function to run the program when it starts
def main():
    graph = Graph()
    graph.load_from_csv('../data/location_network.csv')

    # load ambulances, calls and call priorities.
    ambulances = load_ambulances("../data/ambulance.csv")
    call_priorities = load_call_priorities("../data/call_priority.csv")
    calls = load_calls("../data/calls.csv", call_priorities)

    # create a dedicated logs folder to contain the ambulance_call_logs.csv file.
    log_dir = "logs"
    # ensure the logs directory exists, if not then create it
    os.makedirs(log_dir, exist_ok=True)
    # full path to the log file inside the logs folder.
    log_file_path = os.path.join(log_dir, "ambulance_call_log.csv")
    # clear the dispatch logs using "w" (write mode) in order to have a clean test run w/o saving all the previous data.
    open(log_file_path, "w").close()

    # print the loaded ambulances.
    print("\nAmbulances:")
    for amb in ambulances:
        print(f" {amb[0]} is at {amb[1]}")

    # ensure the highest priority represented by number 1 are processed first, then by called ID to maintain order of arrival.
    # using the variable c for call instead of call to avoid using outer scope since call has already been used.
    def sort_key(c):
        return c['priority'], int(c['id'])
    # sort calls by priority then caller id
    calls.sort(key=sort_key)

    # print the call info
    print("\nEmergency Calls:")
    for call in calls:
        print(f" Call ID {call['id']} at {call['location']} ({call['type']}) [Priority {call['priority']}]")

    # print a section header for readability.
    print("\nDispatch ambulances to emergency calls:")

    # initialize the total route time variable to track the total time spent computing routes using the algorithm.
    total_route_time = 0

    # create a new counter to count how many times the algorithm is called.
    algo_count = 0

    # start a loop through each call once
    for call in calls:
        # each call is dictionary (id, location, type)
        call_id = call['id']
        call_location = call['location']
        call_type = call['type']
        # placeholder variables to track the best ambulance for the call.
        # best_amb is the fastest and is initially none since we don't know yet
        best_amb = None
        # best_path is the shortest path the best_amb would take, initially none.
        best_path = None
        # best_time is the best time found so far, inf is infinity to ensure actual time will be less.
        best_time = float('inf')

        # loop through each ambulance to find the fastest. amb is a tuple ex. (ambulance 1, Intersection A)
        for amb in ambulances:
            # amb_name = amb[0] # comment out b/c it is not used until it is redeclared on line 119
            amb_location = amb[1]
            # create start_time to time how long Dijkstra's algorithm takes for one ambulance.
            start_time = time.perf_counter()
            # use dijkstra's algorithm to compute the shortest path from amb location to call location.
            path, travel_time = dijkstra_path(graph, amb_location, call_location)
            # look up traffic delay for the whole path

            # increment the algo counter each time it is run.
            algo_count += 1
            # calculate the total traffic delay of the path using the graph's edge.
            delay = graph.get_total_delay(path)
            # add base travel time and traffic delay to get total time take for amb to reach the call location.
            total_time = travel_time + delay

            # capture the timestamp at the end of Dijkstra's calculation for a single ambulance.
            end_time = time.perf_counter()
            # adds the elapsed time for this one route calculation to a running total.
            total_route_time += (end_time - start_time)

            # if the amb is faster than any previously checked, update best_time to new fastest
            # and store best_path and best_amb
            if total_time < best_time:
                best_time = total_time
                best_path = path
                best_amb = amb
        # after the loop finishes we know the best amb for the call
        amb_name, amb_location = best_amb

        # print statements for output
        print(
            f"\n{amb_name} dispatched from {amb_location} to Call {call_id} at {call_location} for {call_type} [Priority {call['priority']}]")
        print(f" > Path: {' -> '.join(best_path)}")
        print(f" > Travel Time (base): {best_time - graph.get_total_delay(best_path):.4f}")
        print(f" > Traffic Delay: {graph.get_total_delay(best_path):.4f}")
        print(f" > Total Time: {best_time:.4f}")

        # build dispatch record by creating a dictionary with all info to store in dispatch log.
        dispatch_record = {
            "Call ID": call_id,
            "Call Type": call_type,
            "Call Location": call_location,
            "Selected Ambulance": amb_name,
            "Route to Call Location": "->".join(best_path),
            "Time to the Call Location": f"{best_time:.4f}"
        }
        # append 'a' the log entry to ambulance_call_log.csv using key=value {k} and {v} format for each item.
        with open(log_file_path, 'a') as logfile:
            logfile.write(', '.join([f"{k}={v}" for k, v in dispatch_record.items()]) + "\n")
    # print the Embedded Counter Calculations
    print(f"\nTotal algorithm runs: {algo_count}")
    print(f"Total time computing routes: {total_route_time:.6f} ms")
    # calculate the average in milliseconds
    average_ms = (total_route_time / algo_count) * 1000
    print(f'Average time per route: {average_ms:.4f} ms')
    print(f"\nTotal time spent on all route calculations: {total_route_time:.4f} ms")


# checks if the file is being run directly and isn't imported by another file.
if __name__ == "__main__":
    main()
