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

    def extract_contents(row): return [x.text.replace('\n', '') for x in row]
    URL = 'https://www.mohfw.gov.in/'
    SHORT_HEADERS = ['SNo', 'State', 'Indian-Confirmed',
                     'Foreign-Confirmed', 'Cured',     'Death']
    response = requests.get(URL).content
    soup = BeautifulSoup(response, 'html.parser')
    header = extract_contents(soup.tr.find_all('th'))
    stats = []
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        if stat:
            stats.append(stat)
    records = stats[36]

    active, Cured, Death, Confirmed = records[2:]
    print(records)
    Confirmed = (Confirmed.split('*')[0])
    Cured = (Cured)
    Death = (Death)
    Active = (active)
    stats = stats[0:35]
    print(stats[1])
    context = {'performance': stats, 'Confirmed': Confirmed,
               'Cured': Cured, 'Death': Death, 'Active': Active}
    return render(request, "Corona/index.html", context)


def Symptoms(request):
    # Creating empty lists to store data
    stats = []
    States = []
    Confirmed = []
    # Getting the required data
    extract_content = lambda row : [x.text.replace('\n','') for x in row]
    URL = 'https://www.mohfw.gov.in/'
    HEADINGS = ['SNO', 'State','Indian-Confirmed','Foreign-confirmed','Cured','Death']
    response = requests.get(URL).content
    soup  = BeautifulSoup(response,'html.parser')
    header = extract_content(soup.tr.find_all('th'))
    # Data Arrangements ops
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_content(row.find_all('td'))
        stats.append(stat[1:3])
    stats = stats[0:34]    
    new_stats = [[i[0].lower(), int(i[1])] for i in stats if len(i) != 0]
    new_stats.pop()
    for i in new_stats:
        if i[0] == 'delhi':
            i[0] = 'nct of delhi'
        if i[0] == 'telengana':
            i[0] = 'telangana'
        if i[0] == 'arunachal pradesh':
            i[0] = 'arunanchal pradesh'
        if i[0] == 'andaman and nicobar islands':
            i[0] == 'andaman and nicobar'
    print(new_stats)   
    return render(request,"Corona/symptoms.html",{'new_stats':new_stats})

def News(request):
    newsapi = NewsApiClient(api_key='81959fd211d94f60bbfd44026bc96104')
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
    'q': 'COVID-19', # query phrase
    'pageSize': 20,  # maximum is 100
    'apiKey': '81959fd211d94f60bbfd44026bc96104' # your own API key
}
    response = requests.get(url, params=parameters)
    response_json = response.json()
    print(response_json)
    dates = datetime.now().date()

    desc = []
    news = []
    img = []
    url = []

    for i in response_json['articles']:
        news.append(i['title'])
        url.append(i['url'])
        desc.append(i['description'])
        img.append(i['urlToImage'])

    mylist = zip(news, desc, img,url)
    return render(request,"Corona/news.html",context={"mylist":mylist,'dates':dates})