import ca
import gol
import land_use
import matplotlib.animation
import matplotlib.pyplot
import numpy as np
import traffic


import importlib


ca = importlib.reload(ca)
gol = importlib.reload(gol)
land_use = importlib.reload(land_use)
traffic = importlib.reload(traffic)





##print(land_use.LandUse(lattice = numpy.array([
##    ["tree:0", "water:1"],
##    ["tree:1", "earth:0"],
##    ["fire"  , "earth"   ]
##])))


x = land_use.LandUse([50, 50], neighbour_order = ca.NEIGHBOURS2D2OP);x.neighbours((0, 5))
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
