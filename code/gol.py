import ca
import matplotlib.pyplot as plt
import numpy as np

class Life(ca.CA):
    def __init__(self, shape=None, cell_type=None, lattice=None, neighbour_order=None):
        super().__init__(shape, cell_type, lattice, neighbour_order)

    def update(self, old, new, indx):
        cur = old[indx]
        # indx_n = np.array(self.neighbours(indx)).T
        # print(indx_n[0], indx_n[1])
        # print(old)
        # print(old[indx_n])
        cells = 0
        for n_idx in self.neighbours(indx):
            cells += old[n_idx]

        # if cells >= 1:
        #     print("cur:\t",cur)
        #     print("cells:\t",cells)
        #     print("next:\t",(cur and cells >= 2 and cells <= 3) or (not cur and cells == 3))

        new[indx] = (cur and cells >= 2 and cells <= 3) or (not cur and cells == 3)