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
##COLS = [tuple([round(xx * 255) for xx in col.to_rgba(x)]) for x in INFO[:, 1]]
DIRECTIONS = INFO[:, 0]
COLS       = INFO[:, 1]
CMAP       = ListedColormap(COLS)
del INFO





class Traffic(ca.CA):
    
    
    def __init__(self, shape = None, lattice = None):
        if not (lattice is None):
            if not (shape is None):
                raise ValueError("only one of 'shape' and 'lattice' can be used")
            lattice = np.asarray(lattice, dtype = int)
            shape = lattice.shape
        else:
            shape = numpy.empty(shape).shape
        if len(shape) == 1:
            shape = (1,) + shape
        if len(shape) != 2:
            raise NotImplementedError(f"invalid 'shape', {len(shape)} dimensional traffic automata are not yet implemented")
        super().__init__(
            shape = shape,
            cell_type = int,
            neighbour_order = None
        )
        if not (lattice is None):
            for x in lattice.ravel():
                if not (x in DIRECTIONS):
                    raise ValueError(f"invalid direction {x}")
            tmp = self.lattice.ravel()
            tmp[:] = lattice.ravel()
        else:
            for indx in np.ndindex(self.lattice.shape):
                self.lattice[indx] = np.random.choice(
                    DIRECTIONS
                )
        return
    
    
    def neighbour(self, indx, direction):
        if direction == RIGHT:
            return (indx[0]    , indx[1] + 1)
        elif direction == UP:
            return (indx[0] - 1, indx[1]    )
        elif direction == LEFT:
            return (indx[0]    , indx[1] - 1)
        elif direction == DOWN:
            return (indx[0] + 1, indx[1]    )
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
        return ani.FuncAnimation(
            fig, fun, frames = np.arange(frames),
            blit = True, interval = interval
        )
    
    
    pass

