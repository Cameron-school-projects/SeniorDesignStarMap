import matplotlib.pyplot as plt
from starMath import *
import matplotlib.patches as patches
import io
from base64 import b64encode
from PIL import Image
def getStarInfo():
    #I assume this will be needed to hold some info? Could be useless/extraneous idk
    return

def drawMap(allStars):
    chart_size = 10
    fig, ax = plt.subplots(figsize=(chart_size, chart_size))
    border = patches.Circle((0, 0), 1, color='navy', fill=True)
    ax.add_patch(border)
    ax.scatter(allStars['x'], allStars['y'],
     s=allStars['mag']
,color='white', marker='.', linewidths=0, 
    zorder=2)
    horizon = patches.Circle((0, 0), radius=1, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)
    #add labels
    # for i, txt in enumerate(allStars['label']):
    #     ax.annotate(txt, (allStars['x'][i], allStars['y'][i]))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf,format="png")
    plt.show()
    #the horrors
    #create and save png
    #returns png
    return b64encode(buf.getvalue()).decode()
