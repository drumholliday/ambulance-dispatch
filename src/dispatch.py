"""dispatch.py - loads and prepares ambulance and call data.
Contains helper functions to read data from the ambulance.csv file and calls.csv file.
Assigns priority levels from 1-3 to each call using a provided dictionary.
Returns data in structures to dispatch and route ambulances to calls."""

import csv


# load ambulance.csv data
def load_ambulances(file_path):
    # create an empty list to hold the ambulances.
    ambulances = []
    # open the file at the path that is given to read using 'r' mode.
    with open(file_path, 'r') as csvfile:
        # use DictReader to read each row
        reader = csv.DictReader(csvfile)
        # loop through each row of the csv file
        for row in reader:
            # each ambulance is stored as (name, location) tuple
            ambulances.append((row['Ambulance Number'], row['Staging Location']))
    return ambulances


# Load calls from calls.csv
# add priority_dict as a parameter to assign numeric priority to each call type.
def load_calls(file_path, priority_dict):
    calls = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # reads the type of emergency from the current row in calls.csv
            call_type = row['Call Type']
            # look up the priority value in the priority_dict,
            # if call type is found return the corresponding number. if not found then default 3 (low priority)
            priority = priority_dict.get(call_type, 3)

            # store each call as a dictionary
            call = {
                'id': int(row['Call ID']),
                'location': row['Location'],
                'type': row['Call Type'],
                'priority': priority
            }
            calls.append(call)
        return calls
