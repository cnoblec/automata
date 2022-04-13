import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patheffects as PathEffects

import ca
import matplotlib.animation as ani
import matplotlib.colors as colours
import matplotlib
matplotlib.use("TkAgg")

class SlimeCell:

    directions = ["UP", "RIGHT", "DOWN", "LEFT"]

    lookout_points = {
        "UP"    : [( 0,  2), (-1,  1), ( 1,  1)],
        "DOWN"  : [( 0, -2), (-1, -1), ( 1, -1)],
        "LEFT"  : [(-2,  0), (-1,  1), (-1, -1)],
        "RIGHT" : [( 2,  0), ( 1, -1), ( 1, -1)],
    }

    def __init__(self, value, direction=None):
        self.value = value
        self.direction = direction

    def __add__(self, other):
        return SlimeCell(self.value + other.value, self.direction)

    def __sub__(self, other):
        return SlimeCell(self.value - other.value, self.direction)


class SlimeMould(ca.CA):

    def __init__(self, init_lattice, decay_factor):
        '''
        init_lattice must only contain 0s and 1s, directions will be assigned randomly
        '''
        slime_lattice = self.generate_slime_lattice(init_lattice)
        self.lattice = slime_lattice
        self.shape = self.lattice.shape
        self.df = decay_factor # float value subtracted from every cell at every step


    def generate_slime_lattice(self, lattice):
        slime_lattice = np.empty(self.shape, dtype=SlimeCell)

        indices = ca.arrayIndexes(self.shape)
        for i in indices:
            direction = np.random.choice(SlimeCell.directions)
            cell = SlimeCell(lattice[i], direction)
            slime_lattice[i] = cell

        return slime_lattice


    def generate_float_lattice(self, slime_lattice):
        float_lattice = np.empty(self.shape, dtype=np.float64)

        indices = ca.arrayIndexes(self.shape)
        for i in indices:
            float_lattice[i] = float(slime_lattice[i].value)

        return float_lattice


    def update(self):
        temp_lattice = self.empty()

        indices = ca.arrayIndexes(self.shape)
        for i in indices:
            if self.lattice[i] == 1:
                dir = self.lattice[i].direction

                neighbour_values = []
                neighbours = SlimeCell.lookout_points[dir]
                for nf in neighbours:
                    loc = (i[0]+nf[0], i[1]+nf[1])
                    neighbour_values.append(self.lattice[loc].value)
                new_index = np.argmax(neighbour_values)
                new_loc = neighbours[new_index]

                new_dir = np.random.choice(SlimeCell.directions)

        return