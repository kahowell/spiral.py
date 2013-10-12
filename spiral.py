#!/usr/bin/env python3
import sys
from collections import namedtuple


class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, direction):
        new = Location()
        new.x = self.x + direction.x
        new.y = self.y + direction.y
        return new

    ''' Eq function required to use as a key later. '''
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    ''' Hash function required to use as a key later. '''
    def __hash__(self):
        return hash((self.x, self.y))

class Bounds:
    def __init__(self):
        self.min = Location()
        self.max = Location()

DirectionVector = namedtuple('DirectionVector', 'x,y')

class Direction:
    STARTING = DirectionVector(1,0)

class SpiralPrinter(object):
    def __init__(self, number):
        self.number = number

    ''' Updates the passed bounds object, using the current_location.
        If the current_location is out of the original bounds (thus
        invalidating the current bounds), then the method returns True.
        Otherwise, the method returns False.
    '''
    @staticmethod
    def update_bounds(bounds, current_location):
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
        coords, bounds = self._simulate()
        reverse_coords = self._reverse_coords(coords)
        self._print_simulated(bounds, reverse_coords)

    def _simulate(self):
        # initialize simulation variables
        current_location = Location()
        current_direction = Direction.STARTING
        coords = dict()
        bounds = Bounds()

        # simulate the spiral <number + 1> steps
        for i in range(self.number + 1):
            coords[i] = current_location
            if (self.update_bounds(bounds, current_location)):
                current_direction = self._rotate_direction(current_direction)
            current_location += current_direction
        return coords, bounds

    def _rotate_direction(self, current_direction):
        # this is equivalent mathematically to a 90 deg. ccw rotation, so we
        # can use matrix math: | 0 -1 | |x| = |0*x + -1*y| = |-y|
        #                      | 1  0 | |y|   |1*x +  0*y|   | x|
        return DirectionVector(-current_direction.y, current_direction.x)

    def _reverse_coords(self, coords):
        reverse_coords = {}
        for number, coord in coords.items():
            reverse_coords[coord] = number
        return reverse_coords

    def _print_simulated(self, bounds, reverse_coords):
        number_format = '{:>' + str(len(str(self.number))) + '}'
        for y in range(bounds.min.y, bounds.max.y + 1):
            self._print_row(number_format, bounds, reverse_coords, y)

    def _print_row(self, number_format, bounds, reverse_coords, y):
        for x in range(bounds.min.x, bounds.max.x + 1):
            number = ''
            if Location(x,y) in reverse_coords:
                number = reverse_coords[Location(x,y)]
            print(number_format.format(str(number)), end='')
            if x < bounds.max.x:
                print(end=' ')
        print('')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<number>')
        sys.exit(1)
    try:
        number = int(sys.argv[1])
    except ValueError:
        print('Error:', sys.argv[1], '- not a number')
        sys.exit(2)
    SpiralPrinter(number).print_spiral()
