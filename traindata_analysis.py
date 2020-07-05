import os
import json
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

def get_data(s: str) -> List[List[float]]:

    temp = []
    with open('./labels_filer/train_filter.txt') as rf:
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

    df = pd.DataFrame(k, columns=pd.Index(['x','y','z','l','h','w','r','np'], name='info'))
    sdir = os.path.join('./traindata', 'train_'+s + '.csv')
    df.to_csv(sdir, index=False, header=True)
    aa = df.describe()
    ddir = os.path.join('./traindata', 'train_'+s + '_describe.csv')
    aa.to_csv(ddir, index=True, header=True)

    return True


def plot_csv(s: str) -> bool:

    sdir = os.path.join('./traindata', 'train_'+s + '.csv')
    #print(sdir)
    df = pd.read_csv(sdir)

    mm0 = df['x'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm0.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_x.png'))

    mm1 = df['y'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm1.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_y.png'))

    mm2 = df['z'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm2.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_z.png'))

    mm3 = df['l'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm3.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_l.png'))

    mm4 = df['h'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm4.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_h.png'))

    mm5 = df['w'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm5.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_w.png'))

    mm6 = df['r'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm6.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_r.png'))
    
    mm7 = df['np'].plot.hist(bins=100, grid=True, figsize=(20,10))
    fig = mm7.get_figure()
    fig.savefig(os.path.join('./trainplot',s,'train_'+s+'_np.png'))


    return True

if "__main__" == __name__:

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

