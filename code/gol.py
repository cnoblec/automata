from turtle import color
import ca
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.colors
import numpy as np

class Life(ca.CA):
    def __init__(self, shape=None, lattice=None):
        super().__init__(shape, int, lattice, ca.NEIGHBOURS2D8OP)
        if shape is not None:
            self.lattice[:] = 0 # set the lattice to be zeros instead of empty

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
        return

    def add_shape(self, indx, pattern, fliph=False, flipv=False, transpose=False):
        # indx of top left corner of pattern block
        patterns =    {
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
        pattern_arr = patterns[pattern]

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
        plt.axis(False)
        plt.axis("tight")
        plt.axis("image")

        def func(frame):
            self.evolve()
            im.set_data(self.lattice)
            return [im]
            
        ani = matplotlib.animation.FuncAnimation(fig, func, frames=frames, blit=True, interval=interval)
        filename is not None and ani.save(filename)
        return ani
