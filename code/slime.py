import ca
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.colors

class SlimeCell():

    def __init__(self, dir=0, ph=0.):
        '''
        Initializes the Slime Cell

        Parameters:
            dir (int): 
                direction of SlimeCell; integer number between 0 and 8 inclusive
                where:
                    * 0 = no direction, i.e., no slime is present
                    * 1 = up
                    * 2 = upper-right diagonal
                    * 3 = right
                    * 4 = lower-right diagonal
                    * 5 = down
                    * 6 = lower-left diagonal
                    * 7 = left
                    * 8 = upper-left diagonal
            
            ph (float):
                pheromone level of SlimeCell, must be > 0
        '''
        self.dir = int(dir)
        self.ph = float(ph)

    def __repr__(self):
        return f"({self.dir}, {self.ph})"

    def __str__(self):
        return f"({self.dir}, {self.ph})"

class Mould(ca.CA):

    # Dictionary defining the allowed steps given the direction integer
    step_dir = {
        1: (-1, 0),
        2: (-1, 1),
        3: ( 0, 1),
        4: ( 1, 1),
        5: ( 1, 0),
        6: ( 1,-1),
        7: ( 0,-1),
        8: (-1,-1)
    }

    # List of possible directions
    dirs = [1,2,3,4,5,6,7,8]

    def __init__(self, width, coverage=0.1, decay=0.1, sensor_offset=9):
        '''
        Initializes the Mould instance

        Parameters:
            width (int):
                width/height of square lattice

            coverage (float):
                fraction of lattice that will consist of slime cells
                must be between 0 and 1

            sensor_offset (int):
                offset distance for lookout points
            
        '''
        super().__init__(shape=(width, width), cell_type=SlimeCell, neighbour_order=ca.NEIGHBOURS2D2OP) # direction of slime mould lattice
        self.decay = decay
        self.sensor_offset = sensor_offset
        self.lookouts = self.get_lookouts()
        prob = coverage/8
        rand_dirs = np.random.choice(a=9, size=self.lattice.shape, p=[1-coverage]+[prob]*8).reshape(self.lattice.shape)
        for i in np.ndindex(self.lattice.shape):
            ph = 1. if rand_dirs[i] > 0 else 0.
            self.lattice[i] = SlimeCell(dir=rand_dirs[i],ph=ph)
        
    def get_lookouts(self):
        '''
        Returns a dictionary containing lookout points offset 
            values for the given sensor offset
        '''
        s = self.sensor_offset
        d = int(s/np.sqrt(2))
        # y, x
        # front, left, right
        lookouts = {
            1: [(-s, 0), (-d,-d), (-d, d)],
            2: [(-d, d), (-s, 0), ( 0, s)],
            3: [( 0, s), (-d, d), ( d, d)],
            4: [( d, d), ( 0, s), ( s, 0)],
            5: [( s, 0), ( d, d), ( d,-d)],
            6: [( d,-d), ( s, 0), ( 0,-s)],
            7: [( 0,-s), ( d,-d), (-d,-d)],
            8: [(-d,-d), ( 0,-s), (-s, 0)]
        }
        return lookouts

    def update(self, old, new, indx):
        '''
        Updates a slime cell at index indx in the old lattice to the new lattice
        This function is split into three stages:
            * The diffusion stage: all pheromones undergo diffusion
            * The motor stage: all slime cells determine if they can move forward or not
            * The sensory stage: all slime cells adjust their direction based on the pheromoness 

        Parameters:
            old (ndarray):
                current step's lattice
            
            new (ndarray):
                next step's lattice

            indx (int):
                index of current slime cell
        '''
        
        if new[indx] is None:
            new[indx] = SlimeCell()
        cur = old[indx]
        dir = cur.dir

        # Diffusion Stage
        #   mean filter/convolution
        ph_sum = cur.ph
        for ni in self.neighbours(indx):
            ph_sum += old[ni].ph
        new[indx].ph += (ph_sum/9)*(1-self.decay)  # scale the mean by the decay factor
        
        if dir > 0:
            # print("cur dir:",dir)
            # print("\tcur indx:",indx)
            # Motor Stage
            #   move everyone in the current direction they face if you can
            step = Mould.step_dir[dir]
            new_idx = (indx[0] + step[0], indx[1] + step[1])
            
            if new[new_idx] is None:
                new[new_idx] = SlimeCell()

            if new[new_idx].dir == 0 and old[new_idx].dir == 0:
                new[new_idx].ph += 1.
            else:
                # pick a random direction to look around
                # do not deposit more ph
                new_idx = indx
                dir = np.random.choice(8) + 1
            # print("\tnew indx:",new_idx)

            # Sensory Stage
            #   this is where we orient the cells for the next step
            best = 0
            sensors = []                                # front, left, right pheromone
            for id in self.lookouts[dir]:
                ph_idx = (indx[0]+id[0],indx[1]+id[1])
                sensors.append(old[ph_idx].ph)
            # print("\tsensors:", sensors)
            # f,l,r = sensors
            best = np.argmax(sensors)                   # direction to face

            if best == 1:       # turn left
                dir -= 1
                if dir <= 0:
                    dir = 8
            elif best == 2:     # turn right
                dir += 1
                if dir >= 9:
                    dir = 1
            
            new[new_idx].dir = dir
            # print("\tnew dir:",dir)
            

    def slimes(self):
        '''
        Returns a lattice of just the slime cells 
        '''
        slimes = np.zeros_like(self.lattice, dtype=int)
        for i in np.ndindex(self.lattice.shape):
            slimes[i] = self.lattice[i].dir
        return slimes
        
    def pheromones(self):
        '''
        Returns a lattice of just the pheromones
        '''
        pheromones = np.zeros_like(self.lattice, dtype=float)
        for i in np.ndindex(self.lattice.shape):
            pheromones[i] = self.lattice[i].ph
        return pheromones

    def animate(self, frames=10, interval=200, filename=None, colours=["white"] + ["black"]*8):
        '''
        Returns an animation
        '''
        cmap = matplotlib.colors.ListedColormap(colours)
        fig = plt.figure()
        
        im = plt.imshow(    self.pheromones(),
                            cmap='gray')
        # plt.axis(False)
        plt.axis("tight")
        plt.axis("image")
        ax = plt.gca()
        # ax.grid(True, 'major', linewidth=2)
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
            im.set_data(self.pheromones())
            return [im]
            
        ani = matplotlib.animation.FuncAnimation(fig, func, frames=frames, blit=True, interval=interval)
        fps = 1/(interval/1000)
        filename is not None and ani.save(filename, dpi=150, writer=matplotlib.animation.PillowWriter(fps=fps))
        return ani