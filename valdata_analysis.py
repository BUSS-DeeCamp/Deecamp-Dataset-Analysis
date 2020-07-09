'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-05 20:38:28
@LastEditTime: 2020-07-09 20:59:11
'''
import os
import json
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

def get_data(s: str) -> List[List[float]]:

    temp = []
    with open('./labels_filer/val_filter.txt') as rf:
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

def write_to_csv(k: List[List[float]], s: str) -> bool:

    df = pd.DataFrame(k, columns=pd.Index(['x','y','z','l','w','h','r','np'], name='info'))
    sdir = os.path.join('./valdata', 'val_'+s + '.csv')
    df.to_csv(sdir, index=False, header=True)
    aa = df.describe()
    ddir = os.path.join('./valdata', 'val_'+s + '_describe.csv')
    aa.to_csv(ddir, index=True, header=True)

    return True

def plot_csv(s: str) -> bool:

    sdir = os.path.join('./valdata', 'val_'+s + '.csv')
    #print(sdir)
    df = pd.read_csv(sdir)

    attribute = ['x', 'y', 'z', 'l', 'w', 'h', 'r', 'np']

    for name in attribute:
        mm = df[name].plot.hist(bins=100, grid=True, rwidth = 0.8, density = True, figsize=(20,10))
        plt.xlabel("category")
        plt.ylabel("numbers")
        fig = mm.get_figure()
        fig.savefig(os.path.join('./valplot',s,'val_'+s+'_'+name+'.png'))
        plt.close()

    return True

if "__main__" == __name__:

    plot_csv('Car')
    plot_csv('Truck')
    plot_csv('Tricar')
    plot_csv('Cyclist')
    plot_csv('Pedestrian')
    plot_csv('DontCare')
    
    '''
    Car = get_data('Car')
    print(len(Car))
    write_to_csv(Car, 'Car')
    plot_csv('Car')

    Truck = get_data('Truck')
    print(len(Truck))
    write_to_csv(Truck, 'Truck')
    plot_csv('Truck')

    Tricar = get_data('Tricar')
    print(len(Tricar))
    write_to_csv(Tricar, 'Tricar')
    plot_csv('Tricar')

    Cyclist = get_data('Cyclist')
    print(len(Cyclist))
    write_to_csv(Cyclist, 'Cyclist')
    plot_csv('Cyclist')

    Pedestrian = get_data('Pedestrian')
    print(len(Pedestrian))
    write_to_csv(Pedestrian, 'Pedestrian')
    plot_csv('Pedestrian')
    
    DontCare = get_data('DontCare')
    print(len(DontCare))
    write_to_csv(DontCare, 'DontCare')
    plot_csv('DontCare')
    '''