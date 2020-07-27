'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-25 19:52:19
@LastEditTime: 2020-07-26 21:51:48
'''
import json
import math

from typing import List

def compute_3d_distance(x:List[float]) -> float:

    #def lidar coordinate: lidar_location = [-2.87509, -0.00462392, 1.83632]
    lidar_location = [-2.87509, -0.00462392, 1.83632]
    a = math.pow((x[0]- lidar_location[0]), 2)
    b = math.pow((x[1]- lidar_location[1]), 2)
    c = math.pow((x[2]- lidar_location[2]), 2)

    return math.sqrt(a+b+c)

def compute_bev_direction(x:List[float]) -> float:
    #def lidar coordinate: lidar_location = [-2.87509, -0.00462392, 1.83632]
    lidar_location = [-2.87509, -0.00462392, 1.83632]
    a = x[0]- lidar_location[0]
    b = x[1]- lidar_location[1]
    theta = math.atan2(b,a)

    return theta

def writejson(fpfnpath: str, disdirpath: str):

    with open(fpfnpath, 'r') as fpfn:
        data = json.load(fpfn)

    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    disdir = {'Car':{}, 'Truck':{}, 'Tricar':{}, 'Cyclist':{}, 'Pedestrian':{}, 'DontCare':{}}
    for sname in classlist:
        fpfn = data[sname]

        fp = []
        for v in fpfn:
            fp += v['fp']

        tempdict = {'distance':[], 'direction':[], 'rotation_y':[], 'num_points':[]}
        for i in range(len(fp)):
            d = compute_3d_distance(fp[i][3:6])
            t = compute_bev_direction(fp[i][3:6])
            r = fp[i][6]
            n = fp[i][7]
            tempdict['distance'].append(d)
            tempdict['direction'].append(t)
            tempdict['rotation_y'].append(r)
            tempdict['num_points'].append(n)
        
        disdir[sname] = tempdict

    histdisdir = {'Carhist':{}, 'Truckhist':{}, 'Tricarhist':{}, 'Cyclisthist':{}, 'Pedestrianhist':{}, 'DontCarehist':{}}
    metrics = ['distance', 'direction', 'rotation_y', 'num_points']
    for sname in classlist:
        hname = sname + 'hist'
        hdata = disdir[sname]

        tempdictp = {'distancehist': {}, 'directionhist': {}, 'rotation_yhist':{}, 'num_pointshist':{}}
        
        
        for i in hdata['distance']:
            newi = i//10
            newi = newi * 10
            if newi in tempdictp['distancehist']:
                tempdictp['distancehist'][newi] += 1
            else:
                tempdictp['distancehist'][newi] = 1
    
        
        for i in hdata['direction']:
            newi = round(i, 1)
            if newi in tempdictp['directionhist']:
                tempdictp['directionhist'][newi] += 1
            else:
                tempdictp['directionhist'][newi] = 1

        for i in hdata['rotation_y']:
            newi = round(i, 1)
            if newi in tempdictp['rotation_yhist']:
                tempdictp['rotation_yhist'][newi] += 1
            else:
                tempdictp['rotation_yhist'][newi] = 1
    
        
        for i in hdata['num_points']:
            newi = i//50
            newi = newi * 50
            if newi in tempdictp['num_pointshist']:
                tempdictp['num_pointshist'][newi] += 1
            else:
                tempdictp['num_pointshist'][newi] = 1
        
        
        histdisdir[hname] = tempdictp

    disdir.update(histdisdir)
    with open(disdirpath, 'w') as fdd:
        json.dump(disdir, fdd)
    

def writelabelsjson(fromfile: str, savefile: str):

    with open(fromfile, 'r') as ff:
        data = json.load(ff)

    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    disdir = {'Car':{}, 'Truck':{}, 'Tricar':{}, 'Cyclist':{}, 'Pedestrian':{}, 'DontCare':{}}
    for sname in classlist:
        fpfn = data[sname]

        fp = []
        fr = []
        fn = []
        for v in fpfn:
            fp += v['location']
            fr += v['rotation_y']
            fn += v['num_points']

        tempdict = {'distance':[], 'direction':[], 'rotation_y':[], 'num_points':[]}
        for i in range(len(fp)):
            d = compute_3d_distance(fp[i])
            t = compute_bev_direction(fp[i])
            r = fr[i]
            n = fn[i]
            tempdict['distance'].append(d)
            tempdict['direction'].append(t)
            tempdict['rotation_y'].append(r)
            tempdict['num_points'].append(n)
        
        disdir[sname] = tempdict

    
    histdisdir = {'Carhist':{}, 'Truckhist':{}, 'Tricarhist':{}, 'Cyclisthist':{}, 'Pedestrianhist':{}, 'DontCarehist':{}}
    
    for sname in classlist:
        hname = sname + 'hist'
        hdata = disdir[sname]

        tempdictp = {'distancehist': {}, 'directionhist': {}, 'rotation_yhist':{}, 'num_pointshist':{}}
        
        for i in hdata['distance']:
            newi = i//10
            newi = newi * 10
            if newi in tempdictp['distancehist']:
                tempdictp['distancehist'][newi] += 1
            else:
                tempdictp['distancehist'][newi] = 1
        
        for i in hdata['direction']:
            newi = round(i, 1)
            if newi in tempdictp['directionhist']:
                tempdictp['directionhist'][newi] += 1
            else:
                tempdictp['directionhist'][newi] = 1

        for i in hdata['rotation_y']:
            newi = round(i, 1)
            if newi in tempdictp['rotation_yhist']:
                tempdictp['rotation_yhist'][newi] += 1
            else:
                tempdictp['rotation_yhist'][newi] = 1
    
        
        for i in hdata['num_points']:
            newi = i//50
            newi = newi * 50
            if newi in tempdictp['num_pointshist']:
                tempdictp['num_pointshist'][newi] += 1
            else:
                tempdictp['num_pointshist'][newi] = 1
        
        
        histdisdir[hname] = tempdictp
    
    disdir.update(histdisdir)
    
    with open(savefile, 'w') as sf:
        json.dump(disdir, sf)


if '__main__' == __name__:
    
    
    fpfnpath = 'fpfn.json'
    disdirpath = 'prehist.json'
    writejson(fpfnpath, disdirpath)
    labelpath = 'labels.json'
    labelsdisdir = 'labelshist.json'
    writelabelsjson(labelpath, labelsdisdir)
