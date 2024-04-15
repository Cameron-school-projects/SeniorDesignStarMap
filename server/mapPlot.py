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
    # r=10
    # fig = plt.figure(figsize=(50,50))
    # ax = fig.add_subplot(projection="polar")
    # area = 100 * r**2
    # c = ax.scatter(allStars['x'],allStars['y'],r,linewidths=.4)
    # ax.set_thetamin(-90)
    # ax.set_thetamax(90)
    # plt.axis('off')
    # ax.set_theta_zero_location("N")
    # plt.savefig('test.png')
    # plt.show()
    constellationLines = []
    chart_size = 2
    fig, ax = plt.subplots(figsize=(30,30))
    border = patches.Circle((0,0),2, color='navy', fill=True)
    ax.add_patch(border)
    ax.scatter(allStars['x'], allStars['y'],
     s=5
,color='white', marker='.', linewidths=2, 
    zorder=2)
    horizon = patches.Circle((0, 0), 2, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)
    # constellation = image.imread("tarus.png")
    # box = OffsetImage(constellation,zoom=.15)
    # ab = AnnotationBbox(box,constellations['Taurus'][0],frameon=False)
    # ax.add_artist(ab)
    # for key,value in constellations.items():
    #     ax.add_collection(LineCollection(value,colors="#ffff",linewidths=.5))

    #add labels
    # footnoteText = ""
    ax.margins(0, 0)
    # buf = io.BytesIO()
    plt.axis('off')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.autoscale(enable=True,axis='both',tight=None)
    # plt.savefig(buf,format="png",dpi=300)
    plt.savefig('unlabeled.png',dpi=300)
    for i, txt in enumerate(allStars['label']):
        ax.annotate(txt, (allStars['x'][i], allStars['y'][i]),color="white")

    # plt.axis('off')
    ax.margins(0, 0)
    # buf = io.BytesIO()
    plt.axis('off')
    # plt.savefig(buf,format="png",dpi=300)
    plt.savefig('labeled.png',dpi=300)
    plt.show()
    #the horrors
    #create and save png
    #returns png
    # return b64encode(buf.getvalue()).decode()
