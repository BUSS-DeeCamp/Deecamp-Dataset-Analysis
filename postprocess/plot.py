'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-26 16:57:48
@LastEditTime: 2020-07-26 22:20:50
'''

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

def plot_specific_class(process:dict, name:str, root:str):

    savepath = os.path.join(root, sname)
    distance = process['distance']
    direction = process['direction']
    ry = process['rotation_y']
    numsp = process['num_points']
    
    ####process direction
    tf = []
    for k, v in direction.items():
        tf.append([float(k), v])
    np.random.seed(918575300)
    N = len(tf)
    theta = np.array(tf)[:,0]
    '''
    for i in range(N):
        if theta[i] < 0:
            theta[i] += 6.3
    '''
    radii = np.array(tf)[:,1]
    width = [0.1]*N
    colors = plt.cm.plasma(np.random.rand(N))
    ax = plt.subplot(111, projection='polar')
    ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
    fig = ax.get_figure()
    figname = sname + 'direction.png'
    savefile = os.path.join(savepath,figname)
    try:
        fig.savefig(savefile, dpi=300)
    except FileNotFoundError:
        os.mkdir(savepath)
        fig.savefig(savefile, dpi=300)
    plt.close()


    ####process rotation_y
    tf = []
    for k, v in ry.items():
        tf.append([float(k), v])
    np.random.seed(918575300)
    N = len(tf)
    theta = np.array(tf)[:,0]
    '''
    for i in range(N):
        if theta[i] < 0:
            theta[i] += 6.3
    '''
    radii = np.array(tf)[:,1]
    width = [0.1]*N
    colors = plt.cm.plasma(np.random.rand(N))
    ax = plt.subplot(111, projection='polar')
    ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
    fig = ax.get_figure()
    figname = sname + 'ry.png'
    savefile = os.path.join(savepath,figname)
    try:
        fig.savefig(savefile, dpi=300)
    except FileNotFoundError:
        os.mkdir(savepath)
        fig.savefig(savefile, dpi=300)
    plt.close()
    
def sort_list(t:dict)->List:
    ab = []
    for k,v in t.items():
        ab.append([int(float(k)),round(v,3)])
    abc = sorted(ab, key=(lambda ab: [ab[0]]))
    
    return abc

def plotdistance(t: List, save: str):
    
    plt.figure(figsize=(10,10),dpi=80)
    for i in range(len(t)):
        df = pd.DataFrame(t[i])
        plt.plot(df[0], df[1],label = classlist[i])
    
    plt.xlabel('Distance',size = 26)
    plt.ylabel('Miss rate', size=26)
    plt.xticks(size = 24)
    plt.yticks(size = 24)
    plt.title('Distance-Miss rate', size = 30)

    plt.legend(loc='lower right', fontsize=16 )
    plt.savefig(save+'distance.png', dpi=300)
    plt.close()

def plotnumpoints(t: List, save: str):
    
    plt.figure(figsize=(10,10),dpi=80)
    for i in range(len(t)):
        df = pd.DataFrame(t[i])
        plt.plot(df[0], df[1],label = classlist[i])
    
    plt.xlabel('Num points',size = 26)
    plt.ylabel('Miss rate', size=26)
    plt.xticks(size = 24)
    plt.yticks(size = 24)
    plt.title('Num points-Miss rate', size = 30)

    plt.legend(loc='upper right', fontsize=16 )
    plt.savefig(save+'numpoints.png', dpi=300)
    plt.close()

if '__main__' == __name__:

    fromfile = 'percentage.json'
    with open(fromfile, 'r') as pf:
        data = json.load(pf)
    
    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian']
    saveroot = './result/'
    saveroot2 = './result/Mixed/'
    k1 = []
    k2 = []
    for sname in classlist:
        plot_specific_class(data[sname], sname, saveroot)
        mk1 = sort_list(data[sname]['distance'])
        k1.append(mk1)
        mk2 = sort_list(data[sname]['num_points'])
        k2.append(mk2)
    #datacardirec = data['Car']['direction']
    plotdistance(k1, saveroot2)
    plotnumpoints(k2, saveroot2)
