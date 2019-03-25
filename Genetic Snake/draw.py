from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
someX, someY = 0.5, 0.5
fig,ax = plt.subplots()
currentAxis = plt.gca()
##zoom out
def drawRectangle(posx=0.5, posy=0.5, width=0.2, height=0.2, color = [1,0,0,1]):
    currentAxis.add_patch(Rectangle((posx, posy), width, height, alpha=color[3], facecolor=(color[0],color[1],color[2])))

drawRectangle()
plt.tight_layout()

plt.show()