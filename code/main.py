import ca
import land_use
import matplotlib.animation
import matplotlib.pyplot
import numpy


import importlib


ca = importlib.reload(ca)
land_use = importlib.reload(land_use)



##print(land_use.LandUse(lattice = numpy.array([
##    ["tree:0", "water:1"],
##    ["tree:1", "earth:0"],
##    ["fire"  , "earth"   ]
##])))


x = land_use.LandUse([50, 50])
print(x)
##x.plot()
##matplotlib.pyplot.show()


ani = x.animate("random")
##ani.save("../output/test.gif")
matplotlib.pyplot.show()
