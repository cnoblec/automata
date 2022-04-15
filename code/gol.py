from typing import Literal
import ca
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.colors
import numpy as np

class Life(ca.CA):

    patterns =  {
                "glider":   np.array([  [0,1,0],
                                        [0,0,1],
                                        [1,1,1]]
                                    ),
                "blinker":  np.array([  [0,1,0],
                                        [0,1,0],
                                        [0,1,0]]
                                    ),
                "beacon":   np.array([  [1,1,0,0],
                                        [1,0,0,1],
                                        [0,0,1,1]]
                                    ),
                "pulsar":   np.array([  [0,0,1,1,0,0,0,0,0,1,1,0,0],
                                        [0,0,0,1,1,0,0,0,1,1,0,0,0],
                                        [1,0,0,1,0,1,0,1,0,1,0,0,1],
                                        [1,1,1,0,1,1,0,1,1,0,1,1,1],
                                        [0,1,0,1,0,1,0,1,0,1,0,1,0],
                                        [0,0,1,1,1,0,0,0,1,1,1,0,0],
                                        [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        [0,0,1,1,1,0,0,0,1,1,1,0,0],
                                        [0,1,0,1,0,1,0,1,0,1,0,1,0],
                                        [1,1,1,0,1,1,0,1,1,0,1,1,1],
                                        [1,0,0,1,0,1,0,1,0,1,0,0,1],
                                        [0,0,0,1,1,0,0,0,1,1,0,0,0],
                                        [0,0,1,1,0,0,0,0,0,1,1,0,0]]
                                    ),
                }

    def __init__(self, shape=None, lattice=None):
        super().__init__(shape, int, lattice, ca.NEIGHBOURS2D2OP)

    def update(self, old, new, indx):
        cur = old[indx]

        cells = 0
        for n_idx in self.neighbours(indx):
            cells += old[n_idx]

        new[indx] = (cur and cells >= 2 and cells <= 3) or (not cur and cells == 3)
        return

    def add_shape(self, indx, pattern: Literal["glider", "blinker", "beacon", "pulsar"], fliph=False, flipv=False, transpose=False):
        # indx of top left corner of pattern block
        
        pattern_arr = Life.patterns[pattern]

        if pattern_arr.shape > self.lattice.shape:
            raise AssertionError(f"invalid 'pattern' with shape: '{pattern_arr.shape}' will not fit in lattice of size '{self.lattice.shape}'")

        shape_slice = tuple(slice(idx, idx+pattern_arr.shape[i]) for i,idx in enumerate(indx))

        self.lattice[shape_slice] = pattern_arr
        return

    def animate(self, frames=10, interval=200, filename=None, colours=["white","black"]):
        cmap = matplotlib.colors.ListedColormap(colours)
        fig = plt.figure()
        
        im = plt.imshow(    self.lattice,
                            cmap=cmap,
                            vmin=0,
                            vmax=1)
        # plt.axis(False)
        plt.axis("tight")
        plt.axis("image")
        ax = plt.gca()
        ax.grid(True, 'major', linewidth=2)
        ax.set_xticks(np.arange(-.5, len(self.lattice), 1))
        ax.set_yticks(np.arange(-.5, len(self.lattice), 1))
        plt.tick_params(which='both',
                        bottom=False,
                        top=False,
                        left=False,
                        right=False,
                        labelbottom=False,
                        labelleft=False) 

        def func(frame):
            self.evolve()
            im.set_data(self.lattice)
            return [im]
            
        ani = matplotlib.animation.FuncAnimation(fig, func, frames=frames, blit=True, interval=interval)
        filename is not None and ani.save(filename)
        return ani
