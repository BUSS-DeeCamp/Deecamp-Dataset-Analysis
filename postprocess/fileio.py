'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-23 21:44:06
@LastEditTime: 2020-07-24 23:01:54
'''

import json
def label_class_info(lv:dict, oclass:str)-> dict:
    
    mixid = []
    selectname = lv['name']
    for i in range(len(selectname)):
        if selectname[i] == oclass:
            mixid.append(i)
            
    tempdict = {'id':lv['id'], 'length':len(mixid), 'name':[], 'dimensions':[], 'location':[], 'rotation_y':[], 'num_points': [] }
    for i in mixid:
        tempdict['name'].append(lv['name'][i]) 
        tempdict['dimensions'].append(lv['dimensions'][i])
        tempdict['location'].append(lv['location'][i])
        tempdict['rotation_y'].append(lv['rotation_y'][i])
        tempdict['num_points'].append(lv['num_points'][i])
        #tempdict['length'] = len(mixid)
        #tempdict['id'] = lv['id']
        
    return tempdict
    
def label_main():
    with open('tlabels.json', 'r') as fl:
        lll = json.load(fl)
    
    needtosave = {'Car':[], 'Truck':[], 'Tricar':[], 'Cyclist':[], 'Pedestrian':[], 'DontCare':[]}
    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    for lv in lll:
        for sclass in classlist:
            tempdict = label_class_info(lv, sclass)
            needtosave[sclass].append(tempdict)
            
    with open('labels.json', 'w') as fl1:
        json.dump(needtosave, fl1)
        


def pre_class_info(lv:dict, oclass:str)-> dict:
    
    mixid = []
    selectname = lv['name']
    for i in range(len(selectname)):
        if selectname[i] == oclass:
            mixid.append(i)
            
    tempdict = {'id':lv['metadata']['image_idx'], 'length':len(mixid), 'name':[], 'dimensions':[], 'location':[], 'rotation_y':[], 'score': [] }
    for i in mixid:
        tempdict['name'].append(lv['name'][i]) 
        tempdict['dimensions'].append(lv['dimensions'][i])
        tempdict['location'].append(lv['location'][i])
        tempdict['rotation_y'].append(lv['rotation_y'][i])
        tempdict['score'].append(lv['score'][i])
        #tempdict['length'] = len(mixid)
        #tempdict['id'] = lv['metadata']['image_idx']
        
    return tempdict
    
def pre_main():
    with open('tpre.json', 'r') as fl:
        lll = json.load(fl)
    
    needtosave = {'Car':[], 'Truck':[], 'Tricar':[], 'Cyclist':[], 'Pedestrian':[], 'DontCare':[]}
    classlist = ['Car', 'Truck', 'Tricar', 'Cyclist', 'Pedestrian', 'DontCare']
    for lv in lll:
        for sclass in classlist:
            tempdict = pre_class_info(lv, sclass)
            needtosave[sclass].append(tempdict)
            
    with open('prediction.json', 'w') as fl1:
        json.dump(needtosave, fl1)
        

if '__main__' == __name__: 
    label_main()
    pre_main()
