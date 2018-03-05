import sys
import numpy as np

def read_file(filename):
    '''
    Read the input file
    '''

    NB_COLUMNS = 6

    with open(filename, 'r') as f:
        line = f.readline()
        init_grid = [int(n) for n in line.split()]
        max_rides = init_grid[3]

        rides = np.zeros([max_rides, NB_COLUMNS], dtype=int)

        for row in range(max_rides):
            line = f.readline()
            rides[row, :] = [int(n) for n in line.split()]

    return init_grid, rides

def write_file(num_cars, rides_to_write, filename):
    '''
    Write the output file
    '''
    cars_used = len(rides_to_write)
    output_rows = max(num_cars, cars_used)

    with open(filename, 'w') as f:
        for row in range(output_rows):
            if (row < cars_used):
                f.write(' '.join(map(str,rides_to_write[row])) + '\n')
            else:
                f.write('0\n')
