'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-23 21:43:22
@LastEditTime: 2020-07-25 19:50:31
'''
import json
def s_s_iou(bbox1, bbox2):
    # bbox1(prediction) = [dimension, location] = [w, h, l, x, y, z]
    # bbox2(groundtruth) = [dimension, location] = [w, h, l, x, y, z]
    bx1, bx2, by1, by2, bz1, bz2 = bbox1[3]-bbox1[0]/2, bbox1[3]+bbox1[0]/2, bbox1[4]-bbox1[1]/2, bbox1[4]+bbox1[1]/2, bbox1[5]-bbox1[2]/2, bbox1[5]+bbox1[2]/2,
    
    gx1, gx2, gy1, gy2, gz1, gz2 = bbox2[3]-bbox2[0]/2, bbox2[3]+bbox2[0]/2, bbox2[4]-bbox2[1]/2, bbox2[4]+bbox2[1]/2, bbox2[5]-bbox2[2]/2, bbox2[5]+bbox2[2]/2,
    
    
    v1 = (bx2-bx1)*(by2-by1)*(bz2-bz1)
    v2 = (gx2-gx1)*(gy2-gy1)*(gz2-gz1)
    w = max(0, min(bx2, gx2) - max(bx1,gx1))
    h = max(0, min(by2, gy2) - max(by1,gy1))
    l = max(0, min(bz2, gz2) - max(bz1,gz1))
    inter = w*h*l
    iou = inter/(v1+v2-inter)
    return iou

def process_spc(ltest:dict, ptest:dict, threshold = 0.5) -> dict:
    llength = len(ltest['dimensions'])
    plength = len(ptest['dimensions'])

    scorelist = [0 for i in range(plength)]
    maxscorelist = [0 for i in range(llength)]

    fnlist = [True for i in range(plength)]
    fplist = [True for i in range(llength)]

    
    for i in range(llength):
        bbox2 = ltest['dimensions'][i]+ltest['location'][i]
        for j in range(plength):
            bbox1 = ptest['dimensions'][j]+ptest['location'][j]
            scorelist[j] = s_s_iou(bbox1,bbox2)

        if len(scorelist) == 0:
            maxscore = threshold-1
        else:
            maxscore = max(scorelist)
        maxscorelist[i] = maxscore
    
        if maxscore > threshold:
            maxindex = scorelist.index(maxscore)
            fplist[i] = False
            fnlist[maxindex] = False

            
    
    pc_id = ltest['id']
    tempdict = {'id':pc_id, 'fp':[], 'fn':[]}

    for i in range(llength):
        if fplist[i]:
            tempfp = ltest['dimensions'][i]+ltest['location'][i]+[ltest['rotation_y'][i]]+[ltest['num_points'][i]]
            tempdict['fp'].append(tempfp)
        
    for i in range(plength):
        if fnlist[i]:
            tempfn = ptest['dimensions'][i]+ptest['location'][i]+[ptest['rotation_y'][i]]+[ptest['score'][i]]
            tempdict['fn'].append(tempfn)    
    
    ##return {pc_id:{'fp':[[dimension,location,ry],...], 'fn':[[dimension,location,ry],...]}}
    return tempdict

if '__main__' == __name__:
    
    labelfile = 'labels.json'
    prefile = 'prediction.json'

    with open(labelfile, 'r') as fl:
        labels = json.load(fl)
    with open(prefile, 'r') as fp:
        prediction = json.load(fp)
    
    
    needtosave = {'Car':[], 'Truck':[], 'Tricar':[], 'Cyclist':[], 'Pedestrian':[], 'DontCare':[]}
    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    for sname in classlist:
        for pcindex in range(len(labels[sname])):
            ptest = prediction[sname][pcindex]
            ltest = labels[sname][pcindex]
            result = process_spc(ltest, ptest)
            needtosave[sname].append(result)

    with open('fpfn.json', 'w') as ff:
        json.dump(needtosave, ff)
