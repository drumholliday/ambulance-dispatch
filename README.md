# Ambulance Dispatch Routing System

## Overview

The Ambulance Dispatch Routing System is a Python-based simulation that models how a municipality could dispatch ambulances to emergency calls using graph-based routing algorithms. The program processes ambulance staging locations, emergency call data, call priorities, and location network data from CSV files to determine which ambulance should respond to each call.

This project was originally developed for WGU D795: Applied Algorithms and Reasoning. This repository preserves the original algorithmic dispatch system and provides a foundation for future expansion, including a frontend interface, API layer, visual route display, and additional dispatch logic.

## Purpose

The purpose of this project is to design, build, and test an ambulance dispatch prototype that can:

* Process emergency call data from simulation files
* Prioritize calls based on urgency
* Determine the fastest route from each ambulance to the call location
* Select the ambulance with the shortest response time
* Create a dispatch record for each call
* Log dispatch results to a CSV file
* Measure route-finding algorithm performance

## Competencies Demonstrated

This project demonstrates the following competencies:

### Designs Algorithms to Optimize Performance

The application uses graph-based route calculations to optimize ambulance response time and resource usage.

### Implements Diverse Algorithmic Techniques

The project applies data structures, routing algorithms, CSV processing, priority handling, and dispatch simulation logic to solve a complex computational problem.

### Optimizes Algorithm Performance

The project includes performance timing logic to measure the execution time spent finding the fastest route for dispatched calls.

## Scenario

A municipality needs an automated system to assist with dispatching ambulances for emergency calls. The system must determine the best ambulance to dispatch based on call priority, ambulance staging location, travel time, and the fastest route to the emergency location.

The dispatch system follows these rules:

1. Process the highest priority calls first.
2. For calls with the same priority, process them in the order they were received.
3. Determine the fastest route from each ambulance staging location to the call location.
4. Select the ambulance with the fastest time to the call location.
5. Create a dispatch record containing:

   * Call ID
   * Call type
   * Call location
   * Selected ambulance
   * Route to call location
   * Time to call location
6. Append each dispatch record to a CSV log file.
7. Reset the ambulance to its staging location after the call is logged.
8. Continue until all calls have been dispatched.

## Current Implementation

The current implementation uses Dijkstra's algorithm to calculate the fastest route between ambulance staging locations and emergency call locations.

Dijkstra's algorithm is well suited for this simulation because the location network can be represented as a weighted graph, where:

* Locations are represented as vertices
* Roads or travel paths are represented as edges
* Travel times are represented as edge weights

The algorithm evaluates possible paths and selects the route with the lowest total travel time.

## Features

* Loads ambulance data from CSV files
* Loads emergency call data from CSV files
* Loads call priority data from CSV files
* Loads location network data from CSV files
* Builds a graph representation of the location network
* Processes calls by priority and receipt order
* Calculates the fastest route to each call location
* Selects the ambulance with the shortest response time
* Creates dispatch records
* Writes dispatch results to a CSV log file
* Tracks route-finding execution time
* Includes test output and result screenshots
* Provides a clean foundation for future full-stack expansion

## Technologies Used

* Python
* CSV files
* Custom graph data structures
* Dijkstra's algorithm
* Python standard library
* Git
* GitHub

## Project Structure

```text
ambulance-dispatch/
├── data/
│   ├── ambulance.csv
│   ├── call_priority.csv
│   ├── calls.csv
│   └── location_network.csv
│
├── images/
│   ├── dijkstra_test_results.png
│   └── dijkstras_main_results.png
│
├── src/
│   ├── logs/
│   │   └── ambulance_call_log.csv
│   ├── dijkstra.py
│   ├── dijkstra_test.py
│   ├── dispatch.py
│   ├── graph.py
│   └── main.py
│
├── .gitignore
├── README.md
└── commit_history.txt
```

## Data Files

The simulation uses the following CSV files:

### `ambulance.csv`

Contains ambulance information, including ambulance identifiers and staging locations.

### `calls.csv`

Contains emergency call information, including call IDs, call types, locations, and call order.

### `call_priority.csv`

Contains priority values used to determine which call types should be processed first.

### `location_network.csv`

Contains the location network used to build the graph for route calculations.

## Main Source Files

### `main.py`

Runs the ambulance dispatch simulation.

### `dispatch.py`

Contains the dispatch logic used to process calls, evaluate ambulances, select the best ambulance, and create dispatch records.

### `graph.py`

Defines the graph structure used to represent the location network.

### `dijkstra.py`

Implements Dijkstra's algorithm for finding the fastest route between locations.

### `dijkstra_test.py`

Contains testing logic for validating the route-finding algorithm.

## How the Dispatch Process Works

The dispatch process follows these steps:

1. Load the simulation data from CSV files.
2. Build a graph from the location network data.
3. Load and sort emergency calls by priority.
4. For each call, evaluate all available ambulances.
5. Use the route-finding algorithm to calculate travel time from each ambulance staging location to the call location.
6. Select the ambulance with the fastest travel time.
7. Create a dispatch record.
8. Append the dispatch record to the call log.
9. Reset the ambulance to its staging location.
10. Continue processing until all calls are dispatched.

## Algorithm

### Dijkstra's Algorithm

Dijkstra's algorithm finds the shortest path from a starting location to a destination location in a weighted graph.

In this project, it is used to determine the fastest route from each ambulance staging location to an emergency call location.

### Big O Time Complexity

The time complexity depends on the graph representation and priority queue implementation.

For a graph with `V` vertices and `E` edges, Dijkstra's algorithm commonly has a time complexity of:

```text
O((V + E) log V)
```

when implemented with a priority queue.

### Big O Space Complexity

The space complexity is generally:

```text
O(V)
```

because the algorithm stores distances, visited locations, and previous location references.

## Performance Measurement

The project includes timing logic to measure the total execution time spent finding the fastest route for dispatched calls.

Performance testing can be used to:

* Compare route-finding algorithms
* Identify bottlenecks
* Evaluate scalability
* Support future optimization decisions

## Running the Project

From the project root directory, run:

```bash
python src/main.py
```

Depending on your Python environment, you may need to use:

```bash
python3 src/main.py
```

## Running the Test File

To run the Dijkstra test file:

```bash
python src/dijkstra_test.py
```

or:

```bash
python3 src/dijkstra_test.py
```

## Output

The program generates dispatch records that include:

* Call ID
* Call type
* Call location
* Selected ambulance
* Route to the call location
* Time to the call location

Dispatch records are written to:

```text
src/logs/ambulance_call_log.csv
```

## Example Dispatch Record

A dispatch record may contain information similar to:

```text
Call ID=101, Call Type=Cardiac Emergency, Call Location=Location A, Selected Ambulance=Ambulance 2, Route=A->B->C, Time to Call Location=8
```

## Future Enhancements

Planned or possible future improvements include:

* Add a frontend dashboard for viewing calls and dispatch results
* Add a backend API using FastAPI or Flask
* Display route paths visually on a map or network diagram
* Add support for additional routing algorithms
* Compare multiple algorithms in the same application
* Add database storage for calls, ambulances, and dispatch records
* Add user controls for uploading new simulation files
* Add filtering and search for dispatch history
* Add more detailed performance reports
* Add unit tests for dispatch and graph logic
* Add Docker support for easier deployment

## Possible Full-Stack Expansion

This project could be expanded into a full-stack emergency dispatch prototype with:

* Python backend API
* React or Angular frontend
* Dashboard for call queue management
* Dispatch history table
* Route visualization
* Performance metrics page
* CSV upload functionality
* Database-backed storage

## Academic Note

This project was originally created for academic purposes and intended for personal learning, portfolio development, and future project expansion.

## Author

Drum Holliday

## License

This project is currently for educational and portfolio purposes. A formal license can be added later if the project is prepared for public reuse.

