#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:20:28 2018

@author: juwinkler
"""

import json
from matplotlib import pyplot as p  #contains both numpy and pyplot
import numpy as np
import pandas as pd

# Create a dictionary that contains landkreis longitude and latitude information 
# which is accessible via the landkreis name (currently only polygons supported)
def getLandKreisDict(landKreisFilePath):
    # Load in our data
    data = json.load(open(landKreisFilePath))
    # Create a dict to store the landkreis information
    landkreis_geoInfo = {}    
    
    for county in data['features']:
        if(county['geometry']['type']!='MultiPolygon'):
            x_values = [x[0] for x in county['geometry']['coordinates'][0]]
            y_values = [x[1] for x in county['geometry']['coordinates'][0]]
            # Get length of the lists
            list_length = len(x_values)
            index = 0                
            coordinate_string = '[['
            for y,x in zip(y_values,x_values):
                current_coordinate_string = '['+str(x)+','+str(y)+']'
                index= index+1
                # If we are not at the end of our list, there has to be a comma in between:
                if(index<list_length):
                    current_coordinate_string = current_coordinate_string+','
                coordinate_string = coordinate_string+ current_coordinate_string
            coordinate_string = coordinate_string+ ']]'   
            landkreis_geoInfo[county['properties']['RKI_NameDE']] =   coordinate_string       
    return landkreis_geoInfo

# Loop through all instances of disease information saved and add it to a geojson
# file  
def addDiseaseGeoData(diseaseFilePath):
    # Load in our data
    data = pd.read_csv(diseaseFilePath,encoding='iso-8859-15')
    feature_string = '{"type": "FeatureCollection","features": ['
    for index, row in data.iterrows():
        if(row['county'] in landkreis_geoInfo):
            feature_string = feature_string +'{"type": "Feature","properties": {'
            feature_string = feature_string + '"Injured": ' + '1'+','
            feature_string = feature_string + '"Killed": ' + '0'+','
            feature_string = feature_string + '"Factor1": "Unspecified"'+','
            feature_string = feature_string + '"Hour": ' + '18'+','
            feature_string = feature_string + '"Day": ' + '"Fri"'+','
            feature_string = feature_string + '"Casuality": ' + '1'+','
            feature_string = feature_string + '"Year": ' + str(row['year'])+','
            feature_string = feature_string + '"Week": ' + str(row['week'])+','
            feature_string = feature_string + '"Slidervalue": ' + str((row['year']-2001)*52+row['week'])+','
            if(np.isnan(row['incidence'])):
                print('Error')
                row['incidence'] = 52.00000
            # Do the color coding:       
            if(row['incidence']<100):
                feature_string = feature_string + '"Color": ' + '"#FEE0DF"'+','   
            elif(row['incidence']<200):
                feature_string = feature_string + '"Color": ' + '"#FEC1BF"'+',' 
            elif(row['incidence']<300):
                feature_string = feature_string + '"Color": ' + '"#F27D79"'+',' 
            elif(row['incidence']<400):
                feature_string = feature_string + '"Color": ' + '"#A95855"'+',' 
            elif(row['incidence']<1000):
                feature_string = feature_string + '"Color": ' + '"#750400"'+',' 
            else:
                feature_string = feature_string + '"Color": ' + '"#A80600 "'+','   
            feature_string = feature_string + '"Incidents": ' + str(row['incidence'])   
            # Depending on the incident value, compute the corresponding color: 
            
            feature_string = feature_string + '},"geometry": { "type": "Polygon","coordinates": ' +landkreis_geoInfo[row['county']] + '}}'
            if(index !=len(data)-1):
                feature_string = feature_string + ','
    # bis 100, bis 200, bis 300, bis 400, groesser als 1000, groesser als 2000
       #print(feature_string)
    feature_string = feature_string + ']}'         
    return feature_string
    

################################# MAIN STUFF ##################################

landkreis_geoInfo = getLandKreisDict("hack4health_RKI-data-scripts/survstat/webservice/samples/NodeService/shapes/geojson/Simplified_3p_weightedArea/County_2016_V8.json")
#maserData_geojsonString = addDiseaseGeoData("MasernInput.csv")

stomachData_geojsonString = addDiseaseGeoData("threelastweeks2016.csv")




