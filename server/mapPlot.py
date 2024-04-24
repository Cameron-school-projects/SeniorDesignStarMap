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

def drawMap(allStars,constellations,moonPhase,moonAz,moonEl):
    imageToDraw = ""
    constellationLines = []
    chart_size = 2
    fig, ax = plt.subplots(figsize=(30,30))
    border = patches.Circle((0,0),2, color='#000080', fill=True)
    ax.add_patch(border)
    ax.scatter(allStars['x'], allStars['y'],
     s=allStars['mag']
,color=allStars['color'], marker='.', linewidths=2, 
    zorder=2)
    horizon = patches.Circle((0, 0), 2, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)

    if moonPhase <= 0.1 or moonPhase>.93:     #new moon
        imageToDraw = "./images/Moon-8.png"
    elif moonPhase <= 0.19:   #waxing crescent
        imageToDraw = "./images/Moon-7.png"
    elif moonPhase <= .32:   #waxing quarter
        imageToDraw = "./images/Moon-6"
    elif moonPhase <= .45:  #waxing gibbous
        imageToDraw = "./images/Moon-5"
    elif moonPhase <= .57:   #full moon
        imageToDraw = "./images/Moon-4"
    elif moonPhase <= .69:  #waning gibbous
        imageToDraw = "./images/Moon-3"
    elif moonPhase <= .81:   #waning quarter
        imageToDraw = "./images/Moon-2"
    elif moonPhase <= .93:    #waning crescent
        imageToDraw = "./images/Moon-1"
    moon = image.imread(imageToDraw)
    box = OffsetImage(moon,zoom=.15)
    ab = AnnotationBbox(box,(moonAz,moonEl),frameon=False)
    ax.add_artist(ab)
    # for key,value in constellations.items():
    #     ax.add_collection(LineCollection(value,colors="#ffff",linewidths=.5))

    #add labels
    ax.margins(0, 0)
    unlabeledBuf = io.BytesIO()
    plt.axis('off')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.savefig(unlabeledBuf,format="png",dpi=300,bbox_inches='tight')
    for i, txt in enumerate(allStars['label']):
        ax.annotate(txt, (allStars['x'][i], allStars['y'][i]),color="white")

    buf = io.BytesIO()
    # plt.show()
    plt.savefig(buf,format="png",dpi=300,bbox_inches='tight')
    buf = b64encode(buf.getvalue()).decode()
    unlabeledBuf = b64encode(unlabeledBuf.getvalue()).decode()
    return [buf,unlabeledBuf]
