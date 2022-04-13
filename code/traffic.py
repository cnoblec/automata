import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patheffects as PathEffects

import ca
import matplotlib.animation as ani
import matplotlib.colors as colours
import matplotlib
matplotlib.use("TkAgg")


# Define subclass of CA for traffic:
class Traffic(ca.CA):

    # This dictionary gives the index shift to find the neighbour 
    # given the car's direction
    car_dict = {
        0 : ( 0,  0), 
        1 : ( 0, +1),
        2 : (+1,  0),
        3 : ( 0, -1),
        4 : (-1,  0),
    }

    # This dictionary 
    car_arrows = {
        0 : '',
        1 : '\u2192',
        2 : '\u2193',
        3 : '\u2190',
        4 : '\u2191'
    }

    car_cmap = ListedColormap(['white', 'red','blue','green','purple'])

    def __init__(self, init_lattice):
        #self.lattice = init_lattice
        super().__init__(cell_type = int, lattice = init_lattice)
        self.shape = init_lattice.shape

    def update_lattice(self):
        temp_lattice = self.empty()

        indices = ca.arrayIndexes(self.shape)
        for i in indices:
            ival = self.lattice[i]
            if ival == 0:
                continue
            nf = Traffic.car_dict[ival]
            neighbour = (i[0]+nf[0], i[1]+nf[1])

            if temp_lattice[neighbour] == 0 and self.lattice[neighbour] == 0:
                temp_lattice[neighbour] = ival
            else:
                temp_lattice[indx] = ival
        self.lattice = temp_lattice

    def update(self, old, new, indx):
        ival = old[indx]
        if ival == 0:
            return
        nf = Traffic.car_dict[ival]
        neighbour = (indx[0]+nf[0], indx[1]+nf[1])

        if new[neighbour] == 0 and old[neighbour] == 0:
            new[neighbour] = ival
        else:
            new[indx] = ival
        return

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
            self.update_lattice()
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

