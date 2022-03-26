import ca
import land_use
import matplotlib.animation
import matplotlib.pyplot
import numpy
import traffic


import importlib


ca = importlib.reload(ca)
land_use = importlib.reload(land_use)
traffic  = importlib.reload(traffic)


traffic.Traffic(lattice = [1, 0, 1, 0, 1, 0]).animate()
matplotlib.pyplot.show()


traffic.Traffic(lattice = [1, 1, 1, 1, 0, 0, 1, 0]).animate()
matplotlib.pyplot.show()


traffic.Traffic(lattice = [1, 0, 0, 0, 0, 0, 0, 0]).animate()
matplotlib.pyplot.show()


tf = traffic.Traffic(
    lattice = [
        [3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 2, 1, 0],
        [0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
)


tf.plot()
matplotlib.pyplot.show()


tf.animate(frames = 20, interval = 1000)
matplotlib.pyplot.show()


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
