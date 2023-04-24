#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Matt Brown (mb2), Chirantana Krishnappa (chikrish), and Venkata Dinesh Gopu (vgopu)
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import sys
from math import tanh
# The cost function calculates and returns the cost of the path traveled based on the selected cost_func
# The path parameter is a list of nodes (cities) along the path of travel
# The cost_func parameter is a string that can be either segements, distance, time, or delivery
def city_gps():
    gps={}
    with open('city-gps.txt','r') as f:
        for row in f.readlines():
            newplace=row.split()
def segmentsOfRoad():
    seg={}
    with open('road-segments.txt','r') as f:
        for row in f.readlines():
            newSeg=row.split()
def DistanceBwPlaces(newplace1,newplace2,gps):
    if newplace1 not in gps.keys() or newplace2 not in gps.keys():
        return 0
    updatedPlaces=tuple(sorted((newplace1,newplace2)))
    locOfPlace1=gps.get(updatedPlaces[0])
    locOfPlace2=gps.get(updatedPlaces[1])
    return findDistance(locOfPlace1,locOfPlace2)

def g(path, cost_func):
    cost = 0
    if cost_func == 'segments':
        print('calculating the number of segments traveled')
        # The number of segments is equal to the number of items in the path list minus one
        cost = len(path) - 1
    elif cost_func == 'distance':
        print('caculating the distance traveled')
        #for n in path:
        #    cost += 'Get the distance'
    elif cost_func == 'time':
        print('caculating the time to travel')
        #for n in path:
        #    cost += 'Get the distance and multiply by the speed'
    elif cost_func == 'delivery':
        print('caculating the time to travel')
    return cost

# The heuristic function calculates the straight line distance from a given city to the goal city
# The start_city parameter is a successor for a state
def h(start_city, goal_city):
    print('Calculating heuristic')
    # Load the file 'city-gps.txt'
    # For a good example of calculating distance given GPS coordinates see 
    # https://www.geeksforgeeks.org/program-distance-two-points-earth/
    
def get_successors(city, segments, cost_func):
    print('Getting successors')
    #find all cities that match the given town name in either the to or from part of the road segments data 
    # order the successors by the sum of the heuristic and the selected sot function
    # return the succesors in an ordered list


def get_route(start, end, cost):
    route_taken = []
    total_miles = 0
    total_hours = 0
    total_delivery_hours = 0
    
    fringe = []
    explored = []
    
    if start == end:
        # no traveling required
        return {"total-segments" : len(route_taken), 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-delivery-hours" : total_delivery_hours, 
            "route-taken" : route_taken}
    
    #load the file 'road-segments.txt' and store in variable segments
    
    fringe += [(start, []),]
    
    while len(fringe) > 0:
        (city, path) = fringe.pop(0)
        
        #if city == end:
        #    return the dictionary
        
        #for s in get_successors(city, segments, cost):
            #if s in explored:
                # Don't explore, move to next successor
                #continue
            #else:
                #explore.append(s)
                #fringe.append((s, path+[city,]))
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : 51., 
            "total-hours" : 1.07949, 
            "total-delivery-hours" : 1.1364, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


