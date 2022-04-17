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

    # This dictionary gives the unicode strings for the directional arrows
    car_arrows = {
        0 : '',
        1 : '\u2192',
        2 : '\u2193',
        3 : '\u2190',
        4 : '\u2191'
    }

    # Colour map for car cells
    car_cmap = ListedColormap(['white', 'red', 'blue', 'green', 'purple'])

    def __init__(self, init_lattice):
        '''
        Initialize the Traffic instance

        Parameters:
            init_lattice: 
                initial conditions for the lattice featuring a numpy array
                of integers ranging from 0 to 4 (inclusive)
        '''
        super().__init__(cell_type = int, lattice = init_lattice)
        self.shape = self.lattice.shape

    def update_lattice(self):
        '''
        Update the entire lattice by looking at every cell and following these rules:
            * If a cell has a car in it, check to see if the next cell in its 
                direction is empty, if so move the car
            * The "next cell" consists of the neighbouring cell in both the 
                lattice and a temporary lattice containing all new movements
            * If a cell has a car in it and cannot move to the next one, it 
                stays in that original cell
        This function updates the self.lattice attribute

        Returns:
            None
        '''
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
                temp_lattice[i] = ival
        self.lattice = temp_lattice
        return

    def update(self, old, new, indx):
        '''
        Update the cell at index indx according to these rules:
            * If a cell has a car in it, check to see if the next cell in its 
                direction is empty, if so move the car
            * The "next cell" consists of the neighbouring cell in both the 
                lattice and a temporary lattice containing all new movements
            * If a cell has a car in it and cannot move to the next one, it 
                stays in that original cell

        Parameters:
            * old: previous step's lattice
            * new: current step's lattice (also referred to as temp_lattice)
            * indx: location of cell to move

        Returns:
            None
        '''
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
        '''
        Displays the lattice

        Parameters:
            * title: a string for the plot's title

        Returns:
            * fig: the figure instance
            * ax: the axes instance
            * im: the imshow instance
            * arrows: the list of text arrow labels
        '''
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
                x += self.shape[1]
            y = i[0]
            if y < 0:
                y += self.shape[0]

            text = ax.text(x, y, label, ha="center", va="center", color="w", size=25)
            text.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])
            arrows.append(text)

        return fig, ax, im, arrows
    
    def animate(self, N_steps, title='', interval=200, filename=None):
        '''
        Animates the traffic instance over N steps

        Parameters:
            * N_steps: integer number of steps to run simulation for
            * title: string representing the title of the plot; 
                     will be followed by "n steps" where n is the step #

        Returns:
            Animation of traffic simulation
        '''
        fig, ax, im, arrows = self.display(title)

        def init():
            im.set_data(self.lattice)
            return im,

        def animator(frame):
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
                    x += self.shape[1]
                y = i[0]
                if y < 0:
                    y += self.shape[0]
                text = ax.text(x, y, label, ha="center", va="center", color="w", size=25)
                text.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])

            return im,
        animation = ani.FuncAnimation(
            fig, animator, init_func = init,
            frames = np.arange(N_steps),
            blit = True, interval=interval,
        )

        if filename is not None:
            fps = 1/(interval/1000)
            animation.save(filename, dpi=100, writer=matplotlib.animation.PillowWriter(fps=fps))

        return animation
