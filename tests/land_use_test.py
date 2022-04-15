<<<<<<< HEAD
import matplotlib.pyplot
import numpy
import os
import sys





# little bit of a pain in the ass to import scripts from another directory,
# but this seems to do the trick
here = os.path.abspath(sys.path[0])
sys.path.insert(1, os.path.abspath(here + "/../code"))
import land_use
del sys.path[1]





for i, p in enumerate((
    None,
    {
        "water" :  0,
        "earth" :  1,
        "tree"  : 10,
    },
    {
        "water" : 1,
        "earth" : 1,
        "tree"  : 1,
    },
    {
        "water" : 10,
        "earth" :  1,
        "tree"  :  1,
    },
)):
    land_use.LandUse(shape = (50, 50), p = p).animate(
        file = here + f"/../output/land_use_test_probs_{i}.gif",
        how = "random"
    )





# we want each to start with same lattice
lattice = land_use.LandUse(shape = (50, 50)).lattice
lattice = numpy.reshape([str(xx) for xx in lattice.ravel()], lattice.shape)


for i in range(10):
    land_use.LandUse(lattice = lattice, age_parameters = {
        "water_turn_earth_to_tree" : i,
         "tree_turn_earth_to_tree" : i,
    }).animate(
        file = here + f"/../output/land_use_test_earth_to_tree_{i}.gif",
        how = "deterministic"
    )


for i in range(4, 4 + 10):
    land_use.LandUse(lattice = lattice, age_parameters = {
        "fire_to_earth" : i
    }).animate(
        file = here + f"/../output/land_use_test_fire_to_earth_{i}.gif",
        how = "deterministic"
    )


for i in range(7):
    land_use.LandUse(lattice = lattice, age_parameters = {
        "fire_turn_tree_to_fire" : i
    }).animate(
        file = here + f"/../output/land_use_test_fire_spread_{i}.gif",
        how = "deterministic"
    )


for i in range(10):
    n = 1 - numpy.sqrt(0.05 + 0.1 * i)
    land_use.LandUse(lattice = lattice, random_parameters = {
        "water_turn_earth_to_tree" : lambda age : numpy.random.random() < n,
         "tree_turn_earth_to_tree" : lambda age : numpy.random.random() < n,
    }).animate(
        file = here + f"/../output/land_use_test_earth_to_tree_random_{i}.gif",
        how = "random"
    )


for i in range(10):
    n = 0.95 - 0.1 * i
    land_use.LandUse(lattice = lattice, random_parameters = {
        "fire_turn_tree_to_fire" : lambda age : numpy.random.random() < n
    }).animate(
        file = here + f"/../output/land_use_test_fire_spread_random_{i}.gif",
        how = "random"
    )

=======
# bruh
>>>>>>> fb8973587732b3d6b5dc6805245d64f6807502cf
