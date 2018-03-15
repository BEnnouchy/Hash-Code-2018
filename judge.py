# -*- coding: utf-8 -*-

import numpy as np
import math
import sys
import argparse
import logging

from time import sleep, time
from tqdm import tqdm, trange

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class Car:
    # Make iterable
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, id, rides):
        self._registry.append(self)
        self.id = id
        self.coords = [0, 0]
        self.rides_assigned = rides
        self.step = 0

    def __str__(self):
        return "%d: %s at (%d, %d), ride: %d, remaining_steps: %d" % \
               (self.id, self.state, self.coords[0], self.coords[1], \
                self.ride.id if self.ride else -1, self.steps_to_goal)

class Ride:
    # Make iterable
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, id, start, end, early_start, latest_finish, done):
        self._registry.append(self)
        self.id = id
        self.start = start
        self.end = end
        self.early_start = early_start
        self.latest_finish = latest_finish
        self.score = Ride.distance(start, end)
        self.done = done

    @staticmethod
    def distance(origin, destination):
        return abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])

    def valid_ride(self, step):
        return step + Ride.distance(self.start, self.end) < self.latest_finish

    def early_ride(self, step):
        return step <= self.early_start

    def __str__(self):
        return "%d: [%d, %d] -> [%d, %d], early_start: %d, latest_finish: %d, score: %d" % \
               (self.id, self.start[0], self.start[1], self.end[0], self.end[1], \
               self.early_start, self.latest_finish, self.score)

def main():
    # ## Main function ###

    # Get Start time
    start_time = time()

    # Define logger
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Defining the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_file', help="location of the input problem file",
                        type=str)
    parser.add_argument('-s', '--sol_file', help="location of the solution file",
                        type=str)

    # Default files
    #input_file = './in/a_example.in'
    #input_file = './in/b_should_be_easy.in'
    #input_file = './in/c_no_hurry.in'
    input_file = './in/d_metropolis.in'
    #input_file = './in/e_high_bonus.in'

    output_file = input_file.replace('in', 'out')

    # Parsing the arguments
    args = parser.parse_args()
    if args.in_file:
        input_file = args.in_file
    if args.sol_file:
        solution_file = args.sol_file

    def file_len(filename):
        with open(filename, 'r') as f:
            for i, l in enumerate(f):
                pass
        return i+1

    def read_in_file(filename): # Read the input problem file

        with open(filename, 'r') as f:
            line = f.readline()
            init_grid = [int(n) for n in line.split()]

            # Numpy structured array not used in algorithm
            dt = np.dtype([('start_row', 'uint16'), ('start_col', 'uint16'), \
            ('end_row', 'uint16'), ('end_col', 'uint16'), \
            ('bonus', 'uint16'), ('latest_finish', 'uint16'), ('ride_done', '?')])

            rides = np.zeros(init_grid[3], dtype=dt)

            for row in range(init_grid[3]):
                line = f.readline()
                rides[row] = tuple([np.uint16(n) for n in line.split()]) + (False, )

        return init_grid, rides

    def red_sol_file(filename):

            if file_len(filename) == num_cars:
                with open(filename, 'r') as f:
                    rides = [f.readline().split()]
            else:
                pass

    # Get inputs
    grid, rides_grid = read_file(input_file)

    # Store the grid
    grid_size = [grid[0], grid[1]]
    num_cars = grid[2]
    max_rides = grid[3]
    bonus = grid[4]
    time_max = grid[5]

    # Instanciate cars
    cars = [Car(i) for i in range(num_cars)]

    # Instanciate rides
    for idx, row in enumerate(rides_grid):
        rides = [Ride(idx, (rides_grid[idx]['start_row'], rides_grid[idx]['start_col']), \
        (rides_grid[idx]['end_row'], rides_grid[idx]['end_col']), rides_grid[idx]['bonus'], \
        rides_grid[idx]['latest_finish'], rides_grid[idx]['ride_done'])]

    for time_step in trange(time_max):
        logger.debug("Time step : %d" % time_step)
        purge_rides(rides, time_step)

    # Get Stop time
    stop_time = time()

    elapsed_time = stop_time - start_time

    logger.debug("Time elapsed : %.2f " % elapsed_time)

if __name__ == '__main__':
    main()
