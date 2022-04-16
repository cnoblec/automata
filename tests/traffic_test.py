import os, sys
import matplotlib.pyplot as plt
code = os.path.abspath("../code")
sys.path.append(code)
import traffic

import numpy as np
import matplotlib


traffic.Traffic(init_lattice = [[1, 0, 1, 0, 1, 0]]).animate(10, interval=500, filename='../output/traffic1D-1.gif')
# matplotlib.pyplot.show()


traffic.Traffic(init_lattice = [[1, 1, 1, 1, 0, 0, 1, 0]]).animate(7, interval=500, filename='../output/traffic1D-2.gif')
# matplotlib.pyplot.show()


traffic.Traffic(init_lattice = [[1, 0, 0, 0, 0, 0, 0, 0]]).animate(8, interval=500, filename='../output/traffic1D-3.gif')
# matplotlib.pyplot.show()



init_lattice = np.array([[0,0,2,0,0],
                         [0,0,0,0,0],
                         [0,0,1,0,0],
                         [0,0,0,0,3],
                         [0,4,0,0,0]])
test = traffic.Traffic(init_lattice=init_lattice)

a = test.animate(10, interval=500, filename='../output/traffic2D.gif')

