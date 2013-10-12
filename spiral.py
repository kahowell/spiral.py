#!/usr/bin/env python3
'''Program that prints "spiraling" integers.'''
import sys
from collections import namedtuple


class Location:
    '''Represents a location in terms of a 2D grid.'''
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, direction):
        '''Adds this and a compatible object as if they were both 2D vectors.

        Intended to be used to allow a position to be updated by translation
        by a direction.

        '''
        new = Location()
        new.x = self.x + direction.x
        new.y = self.y + direction.y
        return new

    # Required to use as a dict key
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Required to use as a dict key
    def __hash__(self):
        return hash((self.x, self.y))


class Bounds:
    def __init__(self):
        self.min = Location()
        self.max = Location()

# Represents directions using a 2D vector
Direction = namedtuple('Direction', 'x,y')

STARTING_DIRECTION = Direction(1, 0)


class SpiralPrinter(object):
    '''Prints a square spiral starting at 0 up to a given integer.

    Note: The algorithm used builds a two maps of coordinates to integers, and
    thus is constrained by memory (i.e. memory usage is proportional to the
    number requested).

    '''
    def __init__(self, number):
        self.number = number

    def _update_bounds(self, bounds, current_location):
        ''' Updates the passed bounds object, using the current_location.

        If the current_location is out of the original bounds (thus
        invalidating the current bounds), then the method returns True.
        Otherwise, the method returns False.

        '''
        if current_location.x > bounds.max.x:
            bounds.max.x = current_location.x
            return True
        if current_location.y > bounds.max.y:
            bounds.max.y = current_location.y
            return True
        if current_location.x < bounds.min.x:
            bounds.min.x = current_location.x
            return True
        if current_location.y < bounds.min.y:
            bounds.min.y = current_location.y
            return True
        return False

    def print_spiral(self):
        '''Print the spiral for this SpiralPrinter's number.'''
        coords, bounds = self._simulate()
        coords_num_map = self._map_coords_to_nums(coords)
        self._print_simulated(bounds, coords_num_map)

    def _simulate(self):
        # initialize simulation variables
        current_location = Location()
        current_direction = STARTING_DIRECTION
        coords = dict()
        bounds = Bounds()

        # simulate the spiral <number + 1> steps
        for i in range(self.number + 1):
            coords[i] = current_location
            if (self._update_bounds(bounds, current_location)):
                current_direction = self._rotate_direction(current_direction)
            current_location += current_direction
        return coords, bounds

    def _rotate_direction(self, current_direction):
        ''' Rotates the direction 90 degrees clockwise.

        Using linear algebra: | 0  1 | |x| = | 0*x + 1*y| = | y|
                              | -1 0 | |y|   |-1*x + 0*y|   |-x|

        '''
        return Direction(current_direction.y, -current_direction.x)

    def _map_coords_to_nums(self, coords):
        coords_num_map = {}
        for number, coord in coords.items():
            coords_num_map[coord] = number
        return coords_num_map

    def _print_simulated(self, bounds, coords_num_map):
        number_format = '{:>' + str(len(str(self.number))) + '}'
        # iterate "backwards" to normalize coords to geom. coords
        for y in range(bounds.max.y, bounds.min.y - 1, -1):
            self._print_row(number_format, bounds, coords_num_map, y)

    def _print_row(self, number_format, bounds, coords_num_map, y):
        for x in range(bounds.min.x, bounds.max.x + 1):
            number = ''
            if Location(x, y) in coords_num_map:
                number = coords_num_map[Location(x, y)]
            print(number_format.format(str(number)), end='')
            if x < bounds.max.x:
                print(end=' ')
        print('')


class BadArgumentsException(Exception):
    '''Exception for bad command-line arguments.'''
    pass


def main(arguments):
    '''Main function that is invoked by the command-line.

    This function is separate, so it may invoked elsewhere (ex. as a library
    function or as part of a test).

    '''
    if len(arguments) != 2:
        raise BadArgumentsException('Bad number of arguments.')
    try:
        number = int(arguments[1])
    except ValueError:
        raise BadArgumentsException('{0} - not a number.'.format(arguments[1]))
    if number < 0:
        raise BadArgumentsException('Number should be non-negative.')
    SpiralPrinter(number).print_spiral()

if __name__ == '__main__':
    try:
        main(sys.argv)
    except BadArgumentsException as e:
        print(str(e))
        print('Usage:', sys.argv[0], '<number>')
