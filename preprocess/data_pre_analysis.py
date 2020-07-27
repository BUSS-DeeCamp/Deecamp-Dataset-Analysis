'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-05 20:38:28
@LastEditTime: 2020-07-25 16:45:11
'''
import os
import json
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

def get_data(filename: str, s: str) -> List[List[float]]:

    temp = []
    with open(filename, 'r') as rf:
        for line in rf:
            data_dict = json.loads(line.strip())
            gts = data_dict['gts']
            for x in gts:
                if x['class_name'] == s:
                    info = x['location']+x['dimension']+[x['rotation'][2]]+[x['num_points']]
                    #print((x['location'],x['dimension'],x['rotation'][2],x['num_points']))
                    temp.append(info)
                else:
                    pass                   

    return temp

def write_to_csv(csvfolder: str, k: List[List[float]], s: str):

    df = pd.DataFrame(k, columns=pd.Index(['x','y','z','l','w','h','r','np'], name='info'))
    sdir = os.path.join(csvfolder, s + '.csv')
    df.to_csv(sdir, index=False, header=True)
    aa = df.describe()
    ddir = os.path.join(csvfolder, s + '_describe.csv')
    aa.to_csv(ddir, index=True, header=True)

    

def plot_object_nums(folder: str, obj: List[str], num: List[int]):

    df = pd.DataFrame(nums, index = obj, columns = pd.Index(['nums'], name='info'))
    sdir = os.path.join(folder, 'val_object_nums.csv')
    df.to_csv(sdir, index=True, header=True)

    mm = df.plot.bar(grid=True, figsize=(20,10))
    plt.xlabel('object')
    plt.ylabel('nums')
    plt.title("the numbers of each object in valset")
    fig = mm.get_figure()
    fig.savefig(os.path.join(folder,'object_nums.png'), dpi=300)
    plt.close()

    


def plot_csv(csvfolder: str, plotfolder: str, s: str):

    sdir = os.path.join(csvfolder, s + '.csv')
    #print(sdir)
    df = pd.read_csv(sdir)

    attribute = ['x', 'y', 'z', 'l', 'w', 'h', 'r', 'np']

    for name in attribute:
        mm = df[name].plot.hist(bins=100, grid=True, rwidth = 0.8, figsize=(20,10))
        plt.xlabel("inter region")
        plt.ylabel("Frequency")
        plt.title(name)
        fig = mm.get_figure()
        fig.savefig(os.path.join(plotfolder, s, s+'_'+name+'.png'), dpi=300)
        plt.close()

    return True

if "__main__" == __name__:


    ##1 preprocess txtfile and get List:['location', 'dimension', 'ry', 'num_points']
    ##2 save the List to csvfile
    ##3 load data from csvfile, plot, save to plot folder
    ##4[optional] plot the object_numbers of each class
    need_to_preprocess_file = 'sim_aug_labels.txt'
    csvfolder = 'csv'
    plotfolder = 'plot'
    numobjectfolder = 'object_nums'
    
    typee = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian']
    #typee = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    nums = []
    
    for name in typee:
        dataname = get_data(need_to_preprocess_file, name)
        nums.append(len(dataname))
        write_to_csv(csvfolder, dataname, name)
        #plot_csv('Car')
    
    for name in typee:
        plot_csv(csvfolder, plotfolder, name)
    
    plot_object_nums(numobjectfolder, typee, nums)
