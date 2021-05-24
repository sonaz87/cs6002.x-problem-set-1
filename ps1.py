###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1 - written by me
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    remaining_cows = cows.copy()
    cows_transported = []
    current_selection = []
    total_weight = 0
    cows_to_delete = []
    best_cow = None
        
        #removing cows that weigh more than the transport capacity
    for cow in remaining_cows:
        if remaining_cows[cow] > limit:
            cows_to_delete.append(cow)
    
    for i in cows_to_delete:
        remaining_cows.pop(i)
    
        # arranging transportation for the rest:
    while len(remaining_cows) > 0:
        best_weight = 0
        
            # chosing a cow that can be added to the next trip:

        for cow in remaining_cows:
            if (remaining_cows[cow] > best_weight) and remaining_cows[cow] <= (limit - total_weight) :
                best_weight = remaining_cows[cow]
                best_cow = cow
        
        # if no best cow was selected:
        if best_cow == None:
            
            # if current trip is empty, exit:
            if len(current_selection) == 0:
                break
            else:
                cows_transported.append(current_selection)
                current_selection = []
                total_weight = 0
        
        # if a cow was selected, add it to the current selection and update total weight / remove cow for avaialble list  
        
        else:
            current_selection.append(best_cow)
            total_weight = total_weight + cows[best_cow]
            remaining_cows.pop(best_cow)
            best_cow = None
                

        if len(remaining_cows) == 0:
            # print("finally got here")
            cows_transported.append(current_selection)
            
            
            # if the current selection is max weight, add it to transport    
        if total_weight == limit:
            cows_transported.append(current_selection)
            current_selection = []
            total_weight = 0
        


    return cows_transported


# Problem 2 - written by me
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    best_weight = 0
    total_weight = 0
    cows_transported = []
    best_combination = None
    remaining_cows = cows.copy()
    while len(remaining_cows) > 0:
        for item in get_partitions(remaining_cows.keys()):
            for combo in item:
                total_weight = 0
                for cow in combo:
                    total_weight += cows[cow]
                if total_weight > best_weight and total_weight <= limit:
                    best_combination = combo
                    best_weight = total_weight


        cows_transported.append(best_combination)
        for cow in best_combination:
            remaining_cows.pop(cow)
            best_combination = None
            best_weight = 0
                    
    return cows_transported
            


        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    start = time.time()
    print(greedy_cow_transport(cows, limit))
    end = time.time()
    print(end - start)
    
    start = time.time()
    print(brute_force_cow_transport(cows, limit))
    end = time.time()
    print(end - start)


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)

# print(greedy_cow_transport(cows, limit))
# print(brute_force_cow_transport(cows, limit))

compare_cow_transport_algorithms()

