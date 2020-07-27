'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-25 20:22:23
@LastEditTime: 2020-07-26 16:24:41
'''
import json

def per(labelsfile: str, predictionfile: str, savefile: str):
    #percentage = labels_NOT_detected/labels_sum

    with open(labelsfile, 'r') as lf:
        labels = json.load(lf)
    with open(predictionfile, 'r') as pf:
        prediction = json.load(pf)


    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    percentage = {'Car':{}, 'Truck':{}, 'Tricar':{}, 'Cyclist':{}, 'Pedestrian':{}, 'DontCare':{}}

    for sname in classlist:
        hname = sname + 'hist'
        tempdict = {'distance':{}, 'direction':{}, 'rotation_y':{}, 'num_points':{}}

        ladist = labels[hname]['distancehist']
        pdist = prediction[hname]['distancehist']
        for k,v in ladist.items():
            if k in pdist:
                tempdict['distance'][k] =  pdist[k]/ladist[k]
            else:
                tempdict['distance'][k] = 0
        
        ladirec = labels[hname]['directionhist']
        pdirec = prediction[hname]['directionhist']
        for k,v in ladirec.items():
            if k in pdirec:
                tempdict['direction'][k] =  pdirec[k]/ladirec[k]
            else:
                tempdict['direction'][k] = 0

        larot = labels[hname]['rotation_yhist']
        prot = prediction[hname]['rotation_yhist']
        for k,v in larot.items():
            if k in prot:
                tempdict['rotation_y'][k] =  prot[k]/larot[k]
            else:
                tempdict['rotation_y'][k] = 0

        lanum = labels[hname]['num_pointshist']
        pnum = prediction[hname]['num_pointshist']
        for k,v in lanum.items():
            if int(k) > 500:
                pass
            elif k in pnum:
                tempdict['num_points'][k] =  pnum[k]/lanum[k]
            else:
                tempdict['num_points'][k] = 0

        percentage[sname] = tempdict

    with open(savefile, 'w') as sf:
        json.dump(percentage, sf)

if '__main__' == __name__:

    labelsfile =  'labelshist.json' 
    predictionfile =  'prehist.json'
    savefile = 'percentage.json'
    per(labelsfile, predictionfile, savefile)
