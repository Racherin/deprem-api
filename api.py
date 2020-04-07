import csv
import requests
import datetime
from datetime import timedelta
from geopy import Nominatim
import re



geolocator = Nominatim(user_agent='depremsayac',timeout=3)
url = 'https://deprem-api.herokuapp.com/'
data = requests.get(url).json()
time = datetime.datetime.now()
yesterdays_time = (datetime.datetime.now() - timedelta(1)).strftime('%Y/%m/%d').replace('/','.')
current_time = time.strftime("%Y/%m/%d").replace('/','.')
yesterdays_earthquake=[]
todays_earthquake=[]
yesterdays_time_format = yesterdays_time.replace(".","")
for i in range(len(data['depremler'])):
        current = data['depremler'][i]
        earthquake = {
                'city':current['Yer'],
                'date':current['Saat'],
                'days':str(current['Tarih']).replace(".","/"),
                'enlem':current['Enlem(N)'],
                'boylam':current['Boylam(E)'],
                'buyukluk':float((current['Buyukluk']['ML'])),
                'derinlik':float(current['Derinlik(km)'])
            }
        if data['depremler'][i]['Tarih']  == yesterdays_time:
            yesterdays_earthquake.append(earthquake) #Dün yaşanan tüm depremler
        elif data['depremler'][i]['Tarih']  == current_time:
            todays_earthquake.append(earthquake) #Dün yaşanan tüm depremler
with open('data/{}.csv'.format(yesterdays_time_format), 'w' , newline='', encoding="utf-8") as file :
    writer = csv.writer(file)
    writer.writerow(["Date","Count"])
    writer.writerow()