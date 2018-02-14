# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:56:44 2018

@author: Johannes
"""
import tweepy
import json
import csv
import pandas as pd

consumer_key = "XXX"
consumer_secret = "XXX"

access_key = "XXX-XXX"
access_secret = "XXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def make_tweet(names,diseases,incedence):
    
    tweet = "Gesundheitsupdate für folgende Landkreise mit der Krankheit "+ str(diseases[0])+" und der Infektionsrate pro 100.000 Bürger*innen:"+"\n"+"\n" + str(names[0]) +": " + str(int(incedence[0])) + "\n" + str(names[1])+": " + str(int(incedence[1])) + "\n" + str(names[2])+": " + str(int(incedence[2]))
    api.update_status(tweet)

def load_data():
    data = pd.read_csv("prediction_1_2017.csv", encoding = "latin-1")
    data = data.sort_values(["incidence"],ascending = False)
    top3names = data["county"][:3]
    top3disease = data["disease"][:3]
    top3inc = data["incidence"][:3]
    
    namelist = []
    diseaselist = []
    incedencelist = []
    
    for nmindex in top3names:
        namelist.append(nmindex)
    for disindex in top3disease:
        diseaselist.append(disindex)
    for incindex in top3inc:
        incedencelist.append(incindex)
        
    make_tweet(namelist,diseaselist,incedencelist)

load_data()
    

    
    
    
    
    
    
