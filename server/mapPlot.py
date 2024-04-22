import matplotlib.pyplot as plt
import matplotlib.image as image
from starMath import *
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import io
from base64 import b64encode
from PIL import Image
import numpy as np
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
def getStarInfo():
    #I assume this will be needed to hold some info? Could be useless/extraneous idk
    return

def drawMap(allStars,constellations):
    constellationLines = []
    chart_size = 2
    fig, ax = plt.subplots(figsize=(30,30))
    border = patches.Circle((0,0),2, color='navy', fill=True)
    ax.add_patch(border)
    ax.scatter(allStars['x'], allStars['y'],
     s=allStars['mag']
,color=allStars['color'], marker='.', linewidths=2, 
    zorder=2)
    horizon = patches.Circle((0, 0), 2, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)
    # constellation = image.imread("tarus.png")
    # box = OffsetImage(constellation,zoom=.15)
    # ab = AnnotationBbox(box,constellations['Taurus'][0],frameon=False)
    # ax.add_artist(ab)
    for key,value in constellations.items():
        ax.add_collection(LineCollection(value,colors="#ffff",linewidths=.5))

    #add labels
    # footnoteText = ""
    ax.margins(0, 0)
    # unlabeledBuf = io.BytesIO()
    plt.axis('off')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    # plt.autoscale(enable=True,axis='both',tight=None)
    # plt.savefig(unlabeledBuf,format="png",dpi=300)
    # plt.savefig('unlabeled.png',dpi=300)
    for i, txt in enumerate(allStars['label']):
        ax.annotate(txt, (allStars['x'][i], allStars['y'][i]),color="white")

    # plt.axis('off')
    # ax.margins(0, 0)
    buf = io.BytesIO()
    plt.axis('off')
    plt.show()
    # plt.savefig("unlabeled.png",format="png",dpi=300)
    # plt.savefig('labeled.png',dpi=300)
    #the horrors
    #create and save png
    #returns png
    # buf = b64encode(buf.getvalue()).decode()
    # unlabeledBuf = b64encode(unlabeledBuf.getvalue()).decode()
    # return [buf,unlabeledBuf]
