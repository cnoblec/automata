import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap





import ca
import matplotlib.animation as ani
import matplotlib.colors as col





INFO = np.array([
    [NOCAR := 0, "white" ],
    [RIGHT := 1, "red"   ],
    [DOWN  := 2, "blue"  ],
    [LEFT  := 3, "green" ],
    [UP    := 4, "purple"]
], dtype = object)
DIRS = INFO[:, 0]
COLS = INFO[:, 1]
CMAP = ListedColormap(COLS)
del INFO





class Traffic(ca.CA):
    
    
    def __init__(self, shape = None, lattice = None):
        
        
        nargs = (shape is not None) + (lattice is not None)
        if nargs < 1:
            raise ValueError("provide either 'shape' or 'lattice'")
        if nargs > 1:
            raise ValueError("only one of 'shape' and 'lattice' can be used")
        which = "shape" if (shape is not None) else "lattice"
        
        
        if shape is not None:
            shape = numpy.empty(shape).shape
        else:
            lattice = np.asarray(lattice, dtype = int)
            shape = lattice.shape
        do_check = True
        if len(shape) == 1:
            if lattice is not None:
                if   np.isin(lattice, [NOCAR, RIGHT, LEFT]).all():
                    shape = (1,) + shape
                elif np.isin(lattice, [NOCAR, DOWN , UP  ]).all():
                    shape = shape + (1,)
                else:
                    raise ValueError("invalid 'lattice', 1 dimensional traffic should have all left-right or down-up")
                do_check = False  # because we already did it
            else:
                shape = (1,) + shape
        if len(shape) != 2:
            raise NotImplementedError(f"invalid '{which}', {len(shape)} dimensional traffic automata are not yet implemented")
        if (lattice is not None) and do_check:
            if not np.isin(lattice, DIRECTIONS).all():
                raise ValueError(f"invalid 'lattice', contains directions outside of {DIRECTIONS}")                
        super().__init__(
            shape = shape,
            cell_type = int,
            neighbour_order = None
        )
        if lattice is not None:
            tmp = self.lattice.ravel()
            tmp[:] = lattice.ravel()
        else:
            for indx in np.ndindex(self.lattice.shape):
                self.lattice[indx] = np.random.choice(
                    DIRECTIONS
                )
        return
    
    
    def neighbour(self, indx, direction):
        if   direction == RIGHT:
            return (indx[0]    , indx[1] + 1)
        elif direction == DOWN:
            return (indx[0] + 1, indx[1]    )
        elif direction == LEFT:
            return (indx[0]    , indx[1] - 1)
        elif direction == UP:
            return (indx[0] - 1, indx[1]    )
        raise ValueError("invalid 'direction' argument")
        return
    
    
    def update(self, old, new, indx):
        xx = old[indx]
        
        
        if xx == NOCAR:
            return
        
        
        next_pos = self.neighbour(indx, xx)
        if (old[next_pos] == NOCAR) and \
           (new[next_pos] == NOCAR):
            new[indx] = NOCAR
            new[next_pos] = xx
            return
        
        
        new[indx] = xx
        return


    def plot(self):
        x = self.lattice
        im = plt.imshow(
            x,
            cmap = CMAP,
            vmin = 0, vmax = 4
        )
        arrows = []
        indxs = []
        deltas = []
        for indx in np.ndindex(x.shape):
            xx = x[indx]
            if xx == NOCAR:
                continue
            indxs.append(indx)
            if xx == RIGHT:
                delta = ( 0,  1)
            elif xx == DOWN:
                delta = ( 1,  0)
            elif xx == LEFT:
                delta = ( 0, -1)
            elif xx == UP:
                delta = (-1,  0)
            else:
                raise ValueError(f"invalid direction {xx}")
            deltas.append(delta)
            arrows.append(plt.arrow(
                indx[1] - delta[1]/4.0, indx[0] - delta[0]/4.0,
                delta[1]/2.0, delta[0]/2.0,
                length_includes_head = True,
                head_width = 0.15, width = 0.0625,
                color = "white", ec = "black"
            ))
        SHAPE = x.shape
        return (im, arrows, indxs, deltas, SHAPE)
    
    
    def animate(self, frames = 200, interval = 1000):
        fig = plt.figure()
        im, arrows, indxs, deltas, SHAPE = self.plot()
        def fun(frame):
            self.evolve()
            im.set_array(self.lattice)
            for arrow , indx , delta , i                  in zip(
                arrows, indxs, deltas, range(len(arrows))
            ):
                # if the cell has no car, the car has moved, so
                # update indxs[i] and move the arrow
                if self.lattice[indx] == NOCAR:
                    indxs[i] = indx = ( (indx[0] + delta[0]) % SHAPE[0] , (indx[1] + delta[1]) % SHAPE[1] )
                    arrow.set_data(
                        x = indx[1] - delta[1]/4.0,
                        y = indx[0] - delta[0]/4.0
                    )
            return (im, *arrows)
        def init():
            # i can't believe this fixes the issue, it feels like a joke
            im.set_data(self.lattice)
            return (im,)
        return ani.FuncAnimation(
            fig, fun, init_func = init,
            frames = np.arange(frames),
            blit = True, interval = interval
        )
    
    
    pass

