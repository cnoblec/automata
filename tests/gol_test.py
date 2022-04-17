import os, sys
code = os.path.abspath("../code")
sys.path.append(code)
import gol

game = gol.Life(shape=(19,19))
game.add_shape((3,3),"pulsar")
ani = game.animate(frames=3, interval=500,filename="../output/gol_pulsar.gif")
game = gol.Life(shape=(10,10))
game.add_shape((3,3),"glider")
ani = game.animate(frames=40, interval=200,filename="../output/gol_glider.gif")
