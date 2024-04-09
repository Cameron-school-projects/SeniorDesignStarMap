import matplotlib.pyplot as plt
from starMath import *
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import io
from base64 import b64encode
from PIL import Image
import numpy as np
def getStarInfo():
    #I assume this will be needed to hold some info? Could be useless/extraneous idk
    return

def drawMap(allStars,constellations):
    # r=10
    # fig = plt.figure()
    # ax = fig.add_subplot(projection="polar")
    # area = 100 * r**2
    # c = ax.scatter(allStars['x'],allStars['y'],r)
    # plt.show()
    # allStars['x'] = (allStars['x'] - np.min(allStars['x']) / (np.max(allStars['x']) - np.min(allStars['x']))) * (3 - -3) + -3
    # allStars['y'] = (allStars['y'] - np.min(allStars['y']) / (np.max(allStars['y']) - np.min(allStars['y']))) * (3 - -3) + -3
    constellationLines = []
    chart_size = 2
    fig, ax = plt.subplots()
    border = patches.Rectangle((-2,-2),4,4, color='navy', fill=True)
    ax.add_patch(border)
    ax.scatter(allStars['x'], allStars['y'],
     s=5
,color='white', marker='.', linewidths=2, 
    zorder=2)
    # horizon = patches.Rectangle((0, 0), 4,4, transform=ax.transData)
    # for col in ax.collections:
    #     col.set_clip_path(horizon)
    for key,value in constellations.items():
        ax.add_collection(LineCollection(value,colors="#ffff",linewidths=.5))

    #add labels
    # footnoteText = ""
    # for i, txt in enumerate(allStars['label']):
    #     ax.annotate(txt, (allStars['x'][i], allStars['y'][i]),color="white")
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(-2, 2)
    # plt.autoscale(enable=True,axis='both',tight=None)
    plt.axis('off')
    ax.margins(0, 0)
    buf = io.BytesIO()
    plt.savefig(buf,format="png")
    plt.show()
    #the horrors
    #create and save png
    #returns png
    # return b64encode(buf.getvalue()).decode()
