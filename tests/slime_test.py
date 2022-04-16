import os, sys
import matplotlib.pyplot as plt
code = os.path.abspath("../code")
sys.path.append(code)
import slime

sm = slime.Mould(200)
plt.imshow(sm.slimes()[0])
plt.show()
# print(sm.lattice)
print(sm.slimes()[1])
sm.evolve(1)
# print(sm.lattice)

plt.imshow(sm.slimes()[0])
plt.show()
print(sm.slimes()[1])

ani = sm.animate(frames=100, interval=100, filename="../output/slime200.gif")
# writergif = ani.PillowWriter(fps=5) 
# ani.save("../output/slime200.gif", writer=writergif)
# ani.save("../output/slime200.gif")
# plt.show()
print(sm.slimes()[1])
