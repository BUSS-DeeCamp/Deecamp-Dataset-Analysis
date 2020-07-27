'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-09 19:46:21
@LastEditTime: 2020-07-10 11:53:10
'''
import os
import json
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

def get_data(s: str) -> List[List[float]]:

    temp = []
    kittirootpath = '/home/phosphenesvision/Deecamp/kitti/training/label_2'
    for filename in os.listdir(kittirootpath):
        labelpath = os.path.join(kittirootpath,filename )
        with open(labelpath, 'r') as rf:
            lines = rf.readlines()
            for l in lines:
                l = l.strip('\n')
                store = l.split(' ')
                if store[0] == s:
                    kk = list(map(float, store[8:]))
                    temp.append(kk)
                                 

    return temp

def write_to_csv(k: List[List[float]], s: str) -> bool:

    df = pd.DataFrame(k, columns=pd.Index(['x','y','z','l','w','h','r'], name='info'))
    sdir = os.path.join('./kittitraindata', 'train_'+s + '.csv')
    df.to_csv(sdir, index=False, header=True)
    aa = df.describe()
    ddir = os.path.join('./kittitraindata', 'train_'+s + '_describe.csv')
    aa.to_csv(ddir, index=True, header=True)

    return True

def plot_object_nums(obj: List[str], num: List[int]) -> bool:

    df = pd.DataFrame(nums, index = obj, columns = pd.Index(['nums'], name='info'))
    sdir = os.path.join('./object_nums', 'object_nums.csv')
    df.to_csv(sdir, index=True, header=True)

    mm = df.plot.bar(grid=True, figsize=(20,10))
    plt.xlabel('object')
    plt.ylabel('nums')
    plt.title("the numbers of each object")
    fig = mm.get_figure()
    fig.savefig(os.path.join('./object_nums','object_nums.png'), dpi=300)
    plt.close()

    return True

def plot_csv(s: str) -> bool:

    sdir = os.path.join('./kittitraindata', 'train_'+s + '.csv')
    #print(sdir)
    df = pd.read_csv(sdir)

    attribute = ['x', 'y', 'z', 'l', 'w', 'h', 'r']

    for name in attribute:
        mm = df[name].plot.hist(bins=100, grid=True, rwidth = 0.8, figsize=(20,10))
        plt.xlabel("inter region")
        plt.ylabel("Frequency")
        plt.title(name)
        fig = mm.get_figure()
        fig.savefig(os.path.join('./kittitrainplot',s,'train_'+s+'_'+name+'.png'), dpi=300)
        plt.close()
    

    return True

if "__main__" == __name__:

    typee = ['Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc', 'DontCare']
    nums = []
    
    for name in typee:
        dataname = get_data(name)
        nums.append(len(dataname))
        write_to_csv(dataname, name)
        #plot_csv('Car')
    
    plot_object_nums(typee, nums)
    
    for name in typee:
        plot_csv(name)

    