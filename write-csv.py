import csv
import requests
import datetime
from datetime import timedelta
from geopy import Nominatim
import re
import subprocess as cmd



geolocator = Nominatim(user_agent='depremsayac',timeout=3)
url = 'https://deprem-api.herokuapp.com/'
data = requests.get(url).json()
time = datetime.datetime.now()
yesterdays_time = (datetime.datetime.now() - timedelta(1)).strftime('%Y/%m/%d').replace('/','.')
yesterdays_earthquake=[]
yesterdays_time_format = yesterdays_time.replace(".","")
all_eq = []
for i in range(200):
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
            yesterdays_earthquake.append(earthquake)
with open('data/{}.csv'.format(yesterdays_time_format), 'w' , newline='', encoding="utf-8") as file :
    writer = csv.writer(file)
    writer.writerow(["Date","Hour","Latitude","Longitude","Magnitude","Depth","Location","Area"])
    for i in yesterdays_earthquake :
        try :
            area = geolocator.geocode(i['city'])
            if str(str(area.address).split(',')[-2].strip()).startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) and str(area.address).split(',')[3] != 'Türkiye' :
                writer.writerow([i['days'],i['date'],i['enlem'],i['boylam'],float(i['buyukluk']),i['derinlik'],str(area.address).split(',')[-4].strip(),str(area.address).split(',')[-3].strip()])
                continue
            writer.writerow([i['days'],i['date'],i['enlem'],i['boylam'],float(i['buyukluk']),i['derinlik'],str(area.address).split(',')[-3].strip(),str(area.address).split(',')[-2].strip()])
        except:
            if str(i['city']).__contains__('(') :
                s = i['city']
                e = re.search('\(([^)]+)', s).group(1)
                location = geolocator.geocode(e)
                try: 
                    if str(area.address).split(',')[0].startswith('Ege'):
                        writer.writerow([i['days'],i['date'],i['enlem'],i['boylam'],float(i['buyukluk']),i['derinlik'],str(area.address).split(',')[1].strip(),'Ege Bölgesi'])
                    else :
                        writer.writerow([i['days'],i['date'],i['enlem'],i['boylam'],float(i['buyukluk']),i['derinlik'],str(area.address).split(',')[-4].strip(),str(area.address).split(',')[-3].strip()])
                except:
                    continue
            continue
    #writer.writerow(['2020/04/14','02:56:38','41.569','28.7813','4.1','17.6','İstanbul','Marmara Bölgesi'])
        
    pass

cp = cmd.run("git add .", check=True, shell=True)
#print(cp)

message = "update the repository"
test = 'a'



cp = cmd.run("git commit -m 'update'", check=True, shell=True)
cp = cmd.run("git push -u origin master -f", check=True, shell=True)