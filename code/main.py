import ca
import gol
import land_use
import matplotlib.animation
import matplotlib.pyplot
import numpy as np
import traffic


# import importlib


# ca = importlib.reload(ca)
# land_use = importlib.reload(land_use)
# traffic  = importlib.reload(traffic)


# traffic.Traffic(lattice = [1, 0, 1, 0, 1, 0]).animate()
# matplotlib.pyplot.show()


# traffic.Traffic(lattice = [1, 1, 1, 1, 0, 0, 1, 0]).animate()
# matplotlib.pyplot.show()


# traffic.Traffic(lattice = [1, 0, 0, 0, 0, 0, 0, 0]).animate()
# matplotlib.pyplot.show()


# ani = traffic.Traffic(
#     lattice = [
#         [3, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [1, 0, 2, 1, 0],
#         [0, 4, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#     ]
# ).animate(frames = 20, interval = 1000)
# ani.save("../output/traffic-demo.gif")


# ##print(land_use.LandUse(lattice = numpy.array([
# ##    ["tree:0", "water:1"],
# ##    ["tree:1", "earth:0"],
# ##    ["fire"  , "earth"   ]
# ##])))


# x = land_use.LandUse([50, 50], neighbour_order = 2);x.neighbours((0, 5))
# print(x)
# ##x.plot()
# ##matplotlib.pyplot.show()


# ani = x.animate("random")
# ##ani.save("../output/test.gif")
# matplotlib.pyplot.show()


if __name__ == '__main__':
    
    # init_board = np.array([ [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0]])

    # game = gol.Life(lattice=init_board)
    game = gol.Life(shape=(20,20))
    game.add_shape((3,3),"pulsar")

    # print(game.lattice)

    # game.update(game.lattice, game.lattice, (5,3))
    # print(game.lattice)

    # steps = 10
    # for _ in range(steps):
    #     game.evolve()
    #     print(game.lattice)

    ani = game.animate(frames=3, interval=500,filename="output/gol_pulsar.gif")
    # matplotlib.pyplot.show()