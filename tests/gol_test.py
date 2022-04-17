import os, sys
code = os.path.abspath("../code")
sys.path.append(code)
import gol

game = gol.Life(shape=(20,20))
game.add_shape((3,3),"pulsar")
ani = game.animate(frames=3, interval=500,filename="../output/gol_test/gol_pulsar.gif")
game = gol.Life(shape=(10,10))
game.add_shape((3,3),"glider")
ani = game.animate(frames=40, interval=200,filename="../output/gol_test/gol_glider.gif")
