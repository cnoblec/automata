import os, sys
import matplotlib.pyplot as plt
import numpy as np
code = os.path.abspath("../code")
sys.path.append(code)
import slime

# Generic test
# sm = slime.Mould(200)
# sm.animate(frames=100, interval=100, filename="../output/slime_mould_tests/slime200.gif")


# Sensor offset tests:

# sm = slime.Mould(200, sensor_offset=9)
# sm.animate(frames=100, interval=100, filename="../output/slime_mould_tests/offset9.gif")

# sm = slime.Mould(200, sensor_offset=1)
# sm.animate(frames=100, interval=100, filename="../output/slime_mould_tests/offset1.gif")

# sm = slime.Mould(200, sensor_offset=30)
# sm.animate(frames=200, interval=100, filename="../output/slime_mould_tests/offset30.gif")

sm = slime.Mould(200, coverage=0.05)
sm.add_food((50,100), size=20)
sm.add_food((150,100), size=20)

sm.animate(frames=300, interval=100, filename="../output/slime_mould_tests/2_sources.gif")

sm = slime.Mould(200, coverage=0.05)
sm.add_food((50,50), size=10)
sm.add_food((150,50), size=10)
sm.add_food((150,150), size=10)
sm.add_food((50,150), size=10)

sm.animate(frames=400, interval=100, filename="../output/slime_mould_tests/4_sources.gif")



# Sensor offset vs. coverage %


# so = np.array([3, 9, 15, 21, 27])
# pop = np.linspace(0.1, 0.9, 3)

# plot = np.empty((len(so)*200, len(pop)*200))
# x = 0
# y = 0
# for offset in so:
#     for p in pop:
#         sm = slime.Mould(200, sensor_offset=offset, coverage=p)
#         sm.evolve(50)
#         plot[y:y+200, x:x+200] = sm.pheromones()
#         x+=1
#         print(f"Done offset {offset} with pop% {p}")
#     y+=1

# plt.imshow(plot, cmap='gray')
# fig, ax = plt.subplots()
# ax.set_xticks(np.linspace(0.1*200, 0.9*200, len(pop)))
# ax.set_yticks(np.linspace(0, len(so)*200, len(so)))
# ax.set_xticklabels(pop)
# ax.set_yticklabels(so)
# ax.grid(linewidth=1)
# plt.show()
