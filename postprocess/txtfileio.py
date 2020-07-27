'''
@Description:  
@Author: Zhang Zhanpeng
@Github: https://github.com/phosphenesvision
@Date: 2020-07-24 22:41:40
@LastEditTime: 2020-07-24 22:56:26
'''
import json

if '__main__' == __name__:

    
    needtosave = []
    txtfile = 'val_filter.txt'
    with open(txtfile, 'r') as rf:
        for line in rf:

            data_dict = json.loads(line.strip())
            tempdict = {'id': data_dict['id'], 'length': 0, 'name':[], 'dimensions':[], 'location':[], 'rotation_y':[], 'num_points': []}

            gts = data_dict['gts']
            for x in gts:
                tempdict['name'].append(x['class_name']) 
                tempdict['dimensions'].append(x['dimension'])
                tempdict['location'].append(x['location'])
                tempdict['rotation_y'].append(x['rotation'][2])
                tempdict['num_points'].append(x['num_points'])
                tempdict['length'] += 1

            needtosave.append(tempdict)

    savefile = 'tlabels.json'
    with open(savefile, 'w') as wf:
        json.dump(needtosave, wf)
                   
