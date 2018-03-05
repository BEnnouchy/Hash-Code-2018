import numpy as np
import math
import argparse

from time import sleep, time
from tqdm import tqdm, trange

from ioFiles import read_file, write_file

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class Car(object):
    #Make iterable
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, number):
        self._registry.append(self)
        self.number = number
        self.row_pos = 0
        self.col_pos = 0
        self.is_taken = False
        self.has_begun_ride = False
        self.assigned_ride = None
        self.rides = []

    def take_ride(self, ride):
        self.is_taken = True
        self.assigned_ride = ride
        self.rides.extend(ride)

    def release_car(self):
        self.is_taken = False
        self.has_begun_ride = False
        self.assigned_ride = None

    def move(self, goal_x, goal_y):
        if self.row_pos < goal_x:
            self.row_pos += 1
        elif self.row_pos > goal_x:
            self.row_pos -= 1
        elif self.col_pos < goal_y:
            self.col_pos += 1
        elif self.col_pos > goal_y:
            self.col_pos -= 1
        else:   #At destination
            self.release_car()

def main():
    '''
    Main function
    '''

    #Defining the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_file', help="location of the input file",
                        type=str)
    parser.add_argument('-o', '--out_file', help="location of the output file",
                        type=str)

    #Default files
    input_file = './in/a_example.in'
    output_file = './out/rides.out'

    #Parsing the arguments
    args = parser.parse_args()
    if args.in_file:
        input_file = args.in_file
    if args.out_file:
        output_file = args.out_file

    def distance_of_ride(rides, ride):
        return abs(rides[ride][0] - rides[ride][2]) + abs(rides[ride][1] - rides[ride][3])

    def distance_to_start(car, rides, ride):
        return abs(rides[ride][2] - car.row_pos) + abs(rides[ride][3] - car.col_pos)

    def purge_rides(time_step):
        for ride in range(max_rides):
             if rides_with_scores[ride, 8] == True:
                 #If ride can not be complished, it is purged
                 if rides_with_scores[ride][0] < time_max - time_step:
                     rides_with_scores[ride, 8] == False
        return True

    def can_be_finished(car, ride, time_step):
        result = False
        if distance_to_start(car, rides_with_scores, ride) + rides_with_scores[ride][0] < rides_with_scores[ride][8] - time_step:
            result = True
        return result

    def can_have_bonus(car, ride, time_step):
        result = False
        if distance_to_start(car, rides_with_scores, ride) + time_step < rides_with_scores[ride][7]:
            result = True
        return result

    def assign_rides_and_move(time_step):
        for car in car_list:
            if car.is_taken == False:
                best_ride = find_best_ride(car, time_step)
                if best_ride != -1:
                    car.assigned_ride=best_ride
                    car.rides.append(best_ride)
                    rides_with_scores[best_ride, 8] = False
                    car.is_taken = True
            elif car.has_begun_ride ==  True:
                car.move(rides_with_scores[car.assigned_ride][4], rides_with_scores[car.assigned_ride][5])
            elif car.has_begun_ride ==  False:
                car.move(rides_with_scores[car.assigned_ride][2], rides_with_scores[car.assigned_ride][3])
        return True

    def find_best_ride(car, time_step):
        best_ride = 0
        for ride in range(max_rides):
            if rides_with_scores[ride, 8] == True:
                if can_be_finished(car, ride, time_step):
                    best_ride = ride
                    break
        return best_ride

    def write_rides():
        rides_taken = []

        for car in car_list:
            temp_list = car.rides
            temp_list.insert(0, len(car.rides))
            rides_taken.append(temp_list)
        return rides_taken

    grid, rides = read_file(input_file)

    #Store the grid
    grid_size = [grid[0], grid[1]]
    num_cars = grid[2]
    max_rides = grid[3]
    bonus = grid[4]
    time_max = grid[5]

    #Instanciate cars
    car_list = []
    for i in range(num_cars):
        car_list.append(Car(i))

    #Store distance (i.e. points) with each ride
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
