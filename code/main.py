import ca
import gol
import land_use
import matplotlib.animation
import matplotlib.pyplot
import numpy as np
import traffic
from traffic import Traffic


import importlib


ca = importlib.reload(ca)
land_use = importlib.reload(land_use)
traffic  = importlib.reload(traffic)


traffic.Traffic(lattice = [1, 0, 1, 0, 1, 0]).animation(10)
matplotlib.pyplot.show()


traffic.Traffic(lattice = [1, 1, 1, 1, 0, 0, 1, 0]).animation(10)
matplotlib.pyplot.show()


traffic.Traffic(lattice = [1, 0, 0, 0, 0, 0, 0, 0]).animation(10)
matplotlib.pyplot.show()



init_lattice = np.array([[0,0,2,0,0],
                         [0,0,0,0,0],
                         [0,0,1,0,0],
                         [0,0,0,0,3],
                         [0,4,0,0,0]])
test = Traffic(init_lattice=init_lattice)

a = test.animation(10)
writergif = a.PillowWriter(fps=1) 
a.save("test1.gif", writer=writergif)


##print(land_use.LandUse(lattice = numpy.array([
##    ["tree:0", "water:1"],
##    ["tree:1", "earth:0"],
##    ["fire"  , "earth"   ]
##])))


x = land_use.LandUse([50, 50], neighbour_order = 2);x.neighbours((0, 5))
print(x)
##x.plot()
##matplotlib.pyplot.show()


ani = x.animate("random")
##ani.save("../output/test.gif")
matplotlib.pyplot.show()


if __name__ == '__main__':
    
    game = gol.Life(shape=(20,20))
    game.add_shape((3,3),"pulsar")
    ani = game.animate(frames=3, interval=500,filename="../output/gol_pulsar.gif")
    game = gol.Life(shape=(10,10))
    game.add_shape((3,3),"glider")
    ani = game.animate(frames=40, interval=200,filename="../output/gol_glider.gif")
    # matplotlib.pyplot.show()