#!/usr/bin/env python3
import sys

class Location:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __add__(self, direction):
        new = Location()
        new.x = self.x + direction[0]
        new.y = self.y + direction[1]
        return new

    def __eq__(self, other):
        if type(other) == type(self):
            return self.x == other.x and self.y == other.y
        else:
            return self.x == other[0] and self.y == other[1]

    def __hash__(self):
        return hash((self.x, self.y))

class Bounds:
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def __str__(self):
        return 'bounds: ' + '(' + ','.join([str(item) for item in [self.min_x, self.min_y, self.max_x, self.max_y]]) + ')'

class Direction:
    RIGHT = (1,0)
    DOWN = (0,1)
    LEFT = (-1,0)
    UP = (0,-1)

    DIRECTION_ORDER = [RIGHT, DOWN, LEFT, UP]

class SpiralPrinter(object):
    def __init__(self, number):
        self.number = number

    def print(self):
        self.print_spiral(self.number)

    @staticmethod
    def update_bounds(bounds, current_location):
        if current_location.x > bounds.max_x:
            bounds.max_x = current_location.x
            return True
        if current_location.y > bounds.max_y:
            bounds.max_y = current_location.y
            return True
        if current_location.x < bounds.min_x:
            bounds.min_x = current_location.x
            return True
        if current_location.y < bounds.min_y:
            bounds.min_y = current_location.y
            return True
        return False

    def print_spiral(self, number):
        number_length = len(str(number))
        number_format = '{:>' + str(number_length) + '}'
        current_location = Location()
        current_stride = 1
        current_direction_idx = 0
        current_direction = Direction.DIRECTION_ORDER[current_direction_idx]
        bounds = Bounds()
        coords = dict()
        for i in range(number + 1):
            coords[i] = current_location
            if (self.update_bounds(bounds, current_location)):
                current_direction_idx = (current_direction_idx + 1) % len(Direction.DIRECTION_ORDER)
                current_direction = Direction.DIRECTION_ORDER[current_direction_idx]
            current_location += current_direction
        #process coords
        reverse_coords = dict()
        for number, coord in coords.items():
            reverse_coords[coord] = number
        for y in range(bounds.min_y, bounds.max_y + 1):
            for x in range(bounds.min_x, bounds.max_x + 1):
                number = ''
                if (x,y) in reverse_coords:
                    number = reverse_coords[(x,y)]
                print(number_format.format(str(number)), end=' ')
            print('')

if __name__ == '__main__':
    SpiralPrinter(int(sys.argv[1])).print()
