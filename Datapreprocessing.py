# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 12:34:32 2018

@author: Johannes
"""
import csv
import json
from pprint import pprint

def __MAIN__():
    centroidfile = open("coordinates_file.csv", "w")
    wr = csv.writer(centroidfile, quoting=csv.QUOTE_ALL)
    data = json.load(open("hack4health_RKI-data-scripts\\hack4health_RKI-data-scripts\\survstat\\webservice\\samples\\NodeService\\shapes\\geojson\\Simplified_10p_weightedArea\\County_2016_V8.json"))
    for index in range(len(data["features"])):
        location = data["features"][index]['geometry']['coordinates']
        LK = data["features"][index]['properties']["RKI_NameDE"]
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
        gpsx = gpsx/len(location[0])
        gpsy = gpsy/len(location[0])
        
        output = [LK, gpsx ,gpsy]
        wr.writerow(output)
        
        
    
    
    
__MAIN__()
        

