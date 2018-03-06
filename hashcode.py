import numpy as np
import math
import sys
import argparse
import logging

from enum import Enum
from time import sleep, time
from tqdm import tqdm, trange

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class State(Enum):
    IDLE = 0
    WAITING = 1
    TO_NEXT_START = 2
    RIDING = 3
    STOPPING = 4

class Car:
    # Make iterable
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, id):
        self._registry.append(self)
        self.id = id
        self.coords = [0, 0]
        self.state = State.IDLE
        self.ride_assigned = None
        self.steps_to_goal = 0
        self.rides_done = []

    def output(self):
        return "%d %s" % (len(self.rides_done), ' '.join(map(str, self.rides_done)))

    def __str__(self):
        return "%d: %s at (%d, %d), ride: %d, remaining_steps: %d" % \
               (self.id, self.state, self.coords[0], self.coords[1], \
                self.ride.id if self.ride else -1, self.steps_to_goal)

class Ride:
    # Make iterable
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, id, start, end, early_start, latest_finish):
        self._registry.append(self)
        self.id = id
        self.start = start
        self.end = end
        self.early_start = early_start
        self.latest_finish = latest_finish
        self.score = Ride.distance(start, finish)

    @staticmethod
    def distance(origin, destination):
        return abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])

    def __str__(self):
        return "%d: [%d, %d] -> [%d, %d], early_start: %d, latest_finish: %d, score: %d" % \
               (self.id, self.start[0], self.start[1], self.end[0], self.end[1], \
               self.early_start, self.latest_finish, self.score)

def main():
    # ## Main function ###

    # Define logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Defining the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_file', help="location of the input file",
                        type=str)
    parser.add_argument('-o', '--out_file', help="location of the output file",
                        type=str)

    # Default files
    input_file = './in/a_example.in'
    output_file = './out/rides.out'

    # Parsing the arguments
    args = parser.parse_args()
    if args.in_file:
        input_file = args.in_file
    if args.out_file:
        output_file = args.out_file

    # Define module functions
    def read_file(filename): # Read the input file

        with open(filename, 'r') as f:
            line = f.readline()
            init_grid = [int(n) for n in line.split()]
            max_rides = init_grid[3]

            dt = np.dtype([('start_row', 'u8'), ('start_col', 'u8'), \
            ('end_row', 'u8'), ('end_col', 'u8'), \
            ('bonus', 'u8'), ('latest_finish', 'u8')])

            rides = np.zeros(max_rides, dtype=dt)

            for row in range(max_rides):
                line = f.readline()
                rides[row] = tuple([np.uint8(n) for n in line.split()])

        return init_grid, rides

    def write_file(num_cars, cars, filename): # Write the output file

        with open(filename, 'w') as f:
            for car in cars:
                f.write(' '.join(car.output()) + '\n')

    # Get inputs
    grid, rides_grid = read_file(input_file)

    print(rides_grid)

    # Store the grid
    grid_size = [grid[0], grid[1]]
    num_cars = grid[2]
    max_rides = grid[3]
    bonus = grid[4]
    time_max = grid[5]

    # Define variables
    rides = []

    # Instanciate cars
    cars = [Car(i) for i in range(num_cars)]

    for idx, row in enumerate(rides_grid):
        print(row)
        a = rides_grid[idx]['start_row']
        print(a)

    # Instanciate rides
    '''rides = [Ride(idx, (idx][start_row], rides_grid[idx][start_col]), \
    (rides_grid[idx][end_row], rides_grid[idx][end_col]), rides_grid[idx][bonus], \
    rides_grid[idx][latest_finish]) for idx in rides_grid]
    '''
    # Store distance (i.e. points) with each ride
    scores = np.zeros([max_rides, 2], dtype=int)
    for i in range(max_rides):
        scores[i, 0] = distance_of_ride(rides, i)
        scores[i, 1] = scores[i, 0] + bonus

    ride_OK = np.full([max_rides, 1], True)

    rides_with_scores = np.append(scores, rides, axis=1)
    rides_with_scores = np.append(rides_with_scores, ride_OK, axis=1)

    '''
    rides_with_scores = np.sort(rides_with_scores, axis=0)[::-1]
    print(rides_with_scores[rides_with_scores[:,2].argsort()][::-1])
    '''

    for time_step in trange(time_max):
        purge_rides(time_step)
        assign_rides_and_move(time_step)

    rides_taken = write_rides()

    write_file(num_cars, rides_taken, './out/rides.out')

if __name__ == '__main__':
    main()
