import os, sys
import matplotlib.pyplot as plt
code = os.path.abspath("../code")
sys.path.append(code)
import slime

sm = slime.Mould(200)
sm.animate(frames=100, interval=100, filename="../output/slime200.gif")
