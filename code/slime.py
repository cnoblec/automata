import ca
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.colors

class SlimeCell():
    def __init__(self, dir=0, ph=0.):
        self.dir = int(dir)
        self.ph = float(ph)
    def __repr__(self):
        return f"({self.dir}, {self.ph})"
    def __str__(self):
        return f"({self.dir}, {self.ph})"

class Mould(ca.CA):
    # y, x
    # front, left, right
    lookouts = {
        1: [(-9, 0), (-6,-6), (-6, 6)],
        2: [(-6, 6), (-9, 0), ( 0, 9)],
        3: [( 0, 9), (-6, 6), ( 6, 6)],
        4: [( 6, 6), ( 0, 9), ( 9, 0)],
        5: [( 9, 0), ( 6, 6), ( 6,-6)],
        6: [( 6,-6), ( 9, 0), ( 0,-9)],
        7: [( 0,-9), ( 6,-6), (-6,-6)],
        8: [(-6,-6), ( 0,-9), (-9, 0)]
    }

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

    dirs = [1,2,3,4,5,6,7,8]

    def __init__(self, width, coverage=0.1): # sensor_offset=9
        super().__init__(shape=(width, width), cell_type=SlimeCell, neighbour_order=ca.NEIGHBOURS2D2OP) # direction of slime mould lattice
        self.decay = 0.1
        # self.sensor_offset = 9
        prob = coverage/8
        rand_dirs = np.random.choice(a=9, size=self.lattice.shape, p=[1-coverage]+[prob]*8).reshape(self.lattice.shape)
        for i in np.ndindex(self.lattice.shape):
            ph = 1. if rand_dirs[i] > 0 else 0.
            self.lattice[i] = SlimeCell(dir=rand_dirs[i],ph=ph)

    def update(self, old, new, indx):
        
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
            for id in Mould.lookouts[dir]:
                ph_idx = (indx[0]+id[0],indx[1]+id[1])
                sensors.append(self.lattice[ph_idx].ph)
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
        slimes = np.zeros_like(self.lattice, dtype=int)
        count = 0
        for i in np.ndindex(self.lattice.shape):
            slimes[i] = self.lattice[i].dir
            if self.lattice[i].dir > 0:
                count +=1
        return slimes, count
        
    def pheromones(self):
        pheromones = np.zeros_like(self.lattice, dtype=float)
        for i in np.ndindex(self.lattice.shape):
            pheromones[i] = self.lattice[i].ph
        return pheromones

    def animate(self, frames=10, interval=200, filename=None, colours=["white"] + ["black"]*8):
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
        filename is not None and ani.save(filename, dpi=300, writer=matplotlib.animation.PillowWriter())
        return ani