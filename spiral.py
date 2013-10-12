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
    RIGHT = DirectionVector(1,0)
    DOWN = DirectionVector(0,1)
    LEFT = DirectionVector(-1,0)
    UP = DirectionVector(0,-1)

    DIRECTION_ORDER = [RIGHT, DOWN, LEFT, UP]

class SpiralPrinter(object):
    def __init__(self, number):
        self.number = number

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
        number_length = len(str(self.number))
        number_format = '{:>' + str(number_length) + '}'
        current_location = Location()
        current_stride = 1
        current_direction_idx = 0
        current_direction = Direction.DIRECTION_ORDER[current_direction_idx]
        bounds = Bounds()
        coords = dict()
        for i in range(self.number + 1):
            coords[i] = current_location
            if (self.update_bounds(bounds, current_location)):
                current_direction_idx = (current_direction_idx + 1) % len(Direction.DIRECTION_ORDER)
                current_direction = Direction.DIRECTION_ORDER[current_direction_idx]
            current_location += current_direction
        #process coords
        reverse_coords = dict()
        for number, coord in coords.items():
            reverse_coords[coord] = number
        for y in range(bounds.min.y, bounds.max.y + 1):
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
