import matplotlib.pyplot as plt
import matplotlib.image as image
from starMath import *
import matplotlib.patches as patches
from matplotlib import colors as cl
import io
from base64 import b64encode
from PIL import Image
import numpy as np
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

#takes in a dictionary of star coordinates, labels, and magnitudes
# a dictionary of constellation names and positions,
#moon phase, and moon coordinates
#returns a tuple of base64 strings, encoding the labeled and unlabeled maps
def drawMap(allStars,constellations,moonPhase,moonAz,moonEl):
    imageToDraw = ""
    fig, ax = plt.subplots(figsize=(20,20))
    #add circular border, and scatter stars
    border = patches.Circle((0,0),2, color='#000080', fill=True)
    ax.add_patch(border)
    ax.scatter(allStars['x'], allStars['y'],
     s=allStars['mag']
    ,c=allStars['color'], marker='.', linewidths=2, 
    zorder=2)
    horizon = patches.Circle((0, 0), 2, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)
    
    #check moon phase for corresponding image
    if moonPhase <= 0.1 or moonPhase>.93:     #new moon
        imageToDraw = "./images/Moon-8.png"
    elif moonPhase <= 0.19:   #waxing crescent
        imageToDraw = "./images/Moon-7.png"
    elif moonPhase <= .32:   #waxing quarter
        imageToDraw = "./images/Moon-6.png"
    elif moonPhase <= .45:  #waxing gibbous
        imageToDraw = "./images/Moon-5.png"
    elif moonPhase <= .57:   #full moon
        imageToDraw = "./images/Moon-4.png"
    elif moonPhase <= .69:  #waning gibbous
        imageToDraw = "./images/Moon-3.png"
    elif moonPhase <= .81:   #waning quarter
        imageToDraw = "./images/Moon-2.png"
    elif moonPhase <= .93:    #waning crescent
        imageToDraw = "./images/Moon-1.png"
    moon = image.imread(imageToDraw)
    box = OffsetImage(moon,zoom=.15)
    ab = AnnotationBbox(box,(moonAz,moonEl),frameon=False)
    ax.add_artist(ab)

    #add constellation images
    for key in constellations:
        fileName = "./images/"+key+".png"
        constImage = image.imread(fileName)
        box = OffsetImage(constImage,zoom=.15)
        ab = AnnotationBbox(box,(constellations[key][0],constellations[key][1]),frameon=False)
        ax.add_artist(ab)

    #add labels
    ax.margins(0, 0)
    #adjust whitespaces
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
    unlabeledBuf = io.BytesIO()
    plt.axis('off')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    #save figure, and make the side plots transparent 
    plt.savefig(unlabeledBuf,format="png",dpi=300,bbox_inches='tight',pad_inches=0,transparent=True)
    for i, txt in enumerate(allStars['label']):
        ax.annotate(txt, (allStars['x'][i], allStars['y'][i]),color="white")

    #add constellation labels
    for key in constellations:
        ax.annotate(key,(constellations[key][0],constellations[key][1]),color="white")

    buf = io.BytesIO()
    #save figure, and make the side plots transparent 
    plt.savefig(buf,format="png",dpi=300,bbox_inches='tight',pad_inches=0,transparent=True)
    buf = b64encode(buf.getvalue()).decode()
    unlabeledBuf = b64encode(unlabeledBuf.getvalue()).decode()
    return [unlabeledBuf,buf]
