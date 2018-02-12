# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 12:34:32 2018

@author: Johannes
"""
import csv
import numpy as np
import json
from pprint import pprint

def __MAIN__():
    centroidfile = open("coordinates_file_norm.csv", "w")
    
    data = json.load(open("hack4health_RKI-data-scripts\\hack4health_RKI-data-scripts\\survstat\\webservice\\samples\\NodeService\\shapes\\geojson\\Simplified_10p_weightedArea\\County_2016_V8.json"))
    
    LKlist = []
    xcordlist = []
    ycordlist = []
    
    totalx = 0.0
    totaly = 0.0
    totallen = 0.0
    for index in range(len(data["features"])):
        location = data["features"][index]['geometry']['coordinates']
        totallen += len(location)
        LK = data["features"][index]['properties']["RKI_NameDE"]
        locx = 0.0
        locy = 0.0
        
        for element in location[0]:
            if type(element[0]) == type(0.1):
                locx += element[0]
            else:
                locx += element[0][0]
            if type(element[1]) == type(0.1):
                locy += element[1]
            else:
                locy += element[0][1]
        totalx += locx/len(location[0])
        totaly += locy/len(location[0])
    totalx = totalx/totallen
    totaly = totaly/totallen
    
    for index in range(len(data["features"])):
        location = data["features"][index]['geometry']['coordinates']
        LK = data["features"][index]['properties']["RKI_NameDE"]
        LKlist.append(LK)
        gpsx = 0.0
        gpsy = 0.0
        for element in location[0]:
            if type(element[0]) == type(0.1):
                gpsx += element[0]
            else:
                gpsx += element[0][0]
            if type(element[1]) == type(0.1):
                gpsy += element[1]
            else:
                gpsy += element[0][1]
        gpsx = gpsx/len(location[0]) - totalx
        gpsy = gpsy/len(location[0]) - totaly
        xcordlist.append(gpsx)
        ycordlist.append(gpsy)
    finx = np.std(xcordlist)
    finy = np.std(ycordlist)
    
    wr = csv.writer(centroidfile, quoting=csv.QUOTE_ALL)
    for iterator in range(len(LKlist)):
        output = [LKlist[iterator],xcordlist[iterator] - finx ,ycordlist[iterator] - finy]
        wr.writerow(output)
    
    
    
__MAIN__()
        

