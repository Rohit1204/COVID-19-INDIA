from django.shortcuts import render
from newsapi import NewsApiClient
import PIL, PIL.Image
from datetime import datetime
import COVID19Py
# import matplotlib
# from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
# import numpy as np

    
def Home(request):
    stats = []
    States = []
    Confirmed = []

    extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
    URL = 'https://www.mohfw.gov.in/'
    SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed', 'Foreign-Confirmed','Cured',     'Death'] 
    response = requests.get(URL).content 
    soup = BeautifulSoup(response, 'html.parser') 
    header = extract_contents(soup.tr.find_all('th')) 
    stats = [] 
    all_rows = soup.find_all('tr') 
    for row in all_rows: 
        stat = extract_contents(row.find_all('td')) 
        if stat: 
            stats.append(stat)
    records =stats[32]
    
    Confirmed, Cured, Death = records[1:]
    Confirmed = int(Confirmed.split('*')[0])
    Cured = int(Cured)
    Death = int(Death)
    stats= stats[0:32]   
    context = {'performance':stats,'Confirmed':Confirmed,'Cured':Cured,'Death':Death}
    return render(request,"Corona/index.html",context)