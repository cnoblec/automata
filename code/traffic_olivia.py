import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patheffects as PathEffects

import ca
import matplotlib.animation as ani
import matplotlib.colors as colours
import matplotlib
matplotlib.use("TkAgg")

# Define class for a car cell:
class CarCell:

    car_dict = {
        0 : "empty", 
        1 : "right",
        2 : "down",
        3 : "left",
        4 : "up",
        "empty" : 0,
        "right" : 1,
        "down"  : 2,
        "left"  : 3,
        "up"    : 4,
    }

    car_colours = {
        "empty" : "white",
        "right" : "red",
        "down"  : "blue",
        "left"  : "green",
        "up"    : "purple"
    }

    def __init__(self, val=None, direction=None):
        self.val = val
        self.dir = direction
        
        if val is None:
            self.val = car_dict[direction]
        if direction is None:
            self.dir = car_dict[val]

        self.col = car_colours[self.dir]

# Define subclass of CA for traffic:
class Traffic(ca.CA):

    car_dict = {
        0 : (0,0), 
        1 : (0,+1),
        2 : (+1,0),
        3 : (0,-1),
        4 : (-1,0),
    }

    car_arrows = {
        0 : '',
        1 : '→',
        2 : '↓',
        3 : '←',
        4 : '↑'
    }

    car_cmap = ListedColormap(['white', 'red','blue','green','purple'])

    def __init__(self, init_lattice):
        self.lattice = init_lattice
        self.shape = init_lattice.shape

    def update(self):
        temp_lattice = self.empty()

        indices = ca.arrayIndexes(self.shape)
        for i in indices:
            ival = self.lattice[i]
            nf = Traffic.car_dict[ival]
            neighbour = (i[0]+nf[0], i[1]+nf[1])

            if temp_lattice[neighbour] == 0 and self.lattice[neighbour] == 0:
                temp_lattice[neighbour] = ival
            elif self.lattice[i] != 0:
                temp_lattice[i] = ival
            else:
                continue
        self.lattice = temp_lattice

    def display(self, title=''):
        fig, ax = plt.subplots(figsize=(10,7))
        im = ax.imshow(self.lattice, cmap=Traffic.car_cmap, vmin=0, vmax=4)
        ax.set_title(title)

        indices = ca.arrayIndexes(self.shape)
        arrows = []
        for i in indices:
            ival = self.lattice[i]
            label = Traffic.car_arrows[ival]
            x = i[1]
            if x < 0:
                x += self.shape[0]
            y = i[0]
            if y < 0:
                y += self.shape[1]

            text = ax.text(x, y, label, ha="center", va="center", color="w", size=25)
            text.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])
            arrows.append(text)

        plt.show()
        return fig, ax, im, arrows
    
    def animation(self, N_steps, title=''):
        fig, ax, im, arrows = self.display(title)

        def init():
            im.set_data(self.lattice)
            return im,

        def animate(frame):
            # Clear arrows
            c = len(ax.texts)
            for _ in range(c):
                matplotlib.artist.Artist.remove(ax.texts[0])

            # Update lattice and image
            self.update()
            im.set_array(self.lattice)

            # Set new title with step number
            ax.set_title(f"{title} {frame} steps")

            # Add new arrows
            indices = ca.arrayIndexes(self.shape)
            for i in indices:
                ival = self.lattice[i]
                label = Traffic.car_arrows[ival]
                x = i[1]
                if x < 0:
                    x += self.shape[0]
                y = i[0]
                if y < 0:
                    y += self.shape[1]
                text = ax.text(x, y, label, ha="center", va="center", color="w", size=25)
                text.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])

            return im,

        return ani.FuncAnimation(
            fig, animate, init_func = init,
            frames = np.arange(N_steps),
            blit = True, interval=1000,
        )


init_lattice = np.array([[0,0,2,0,0],
                         [0,0,0,0,0],
                         [0,0,1,0,0],
                         [0,0,0,0,3],
                         [0,4,0,0,0]])
test = Traffic(init_lattice=init_lattice)
# test.display()
# test.update()
# test.update()
a = test.animation(10)
writergif = ani.PillowWriter(fps=1) 
a.save("test1.gif", writer=writergif)
