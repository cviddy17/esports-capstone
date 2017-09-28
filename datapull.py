import requests
import pandas as pd
import numpy as np
import json
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

with open('/Users/chadvalencia/keys/esports.json') as f:
    data = json.load(f)
    api_key = data['esports-key']

base_url = 'http://api.esportsearnings.com/v0/LookupHighestEarningPlayersByGame?apikey='
api_url = api_key
game_offset = '&gameid=151&offset='
frmt = '&format=json'
player_list = []
for i in range(17):
    url = base_url+api_url+game_offset+str(i*100)+frmt
    print(url)
    s = requests.get(url)
    player_list.append(s.text)
    time.sleep(2)

p_df = pd.read_json(player_list[0])
for i in np.arange(1,17):
    temp_df = pd.read_json(player_list[i])
    p_df = p_df.append(temp_df)

# porting player_list_to_csv
# p_df.to_csv('starcraft_player_list.csv')

p_df['NameFirst']= p_df['NameFirst'].str.replace(' ', '-')
p_df['NameLast']= p_df['NameLast'].str.replace(' ', '-')

p_df['PlayerId']=p_df.PlayerId.astype(str)
p_df['kh']= p_df['PlayerId']+'-'+p_df['CurrentHandle']

p_df['Key_First']=p_df['kh'].where(p_df['NameFirst']=='-',p_df['kh']+'-'+p_df['NameFirst'])
p_df['Key']=p_df['Key_First'].where(p_df['NameLast']=='-',p_df['Key_First']+'-'+p_df['NameLast'])
p_df['Key_Last']=p_df['kh'].where(p_df['NameLast']=='-',p_df['kh']+'-'+p_df['NameLast'])
p_df['KL']=p_df['Key_Last'].where(p_df['NameFirst']=='-',p_df['Key_Last']+'-'+p_df['NameFirst'])

p_df.pop('Key_First')
p_df.pop('Key_Last')

# porting list to csv
# p_df.to_csv('starcraft_names_with_keys.csv')
# p_df = pd.read_csv('starcraft_names_with_keys.csv')

base_url = 'http://api.esportsearnings.com/v0/LookupPlayerById?apikey='+api_key+'&playerid='
frmt = '&format=json'
ttotal = []
for i in p_df['PlayerId']:
    url = base_url+i+frmt
    s = requests.get(url)
    ttotal.append(s.text)
    time.sleep(2)

tt_df=pd.DataFrame(json.loads(ttotal[0]),index=[0])
for i in np.arange(1,1683):
    temp_df = pd.DataFrame(json.loads(ttotal[i]),index=[0])
    tt_df = tt_df.append(temp_df)

len(tt_df['PlayerId'])
tt_df['PlayerId']=list(p_df['PlayerId'])
max(tt_df['TotalTournaments'])
tt_df['iter']=tt_df['TotalTournaments']
tt_df

sum(tt_df['TotalTournaments'])


url4 = 'http://api.esportsearnings.com/v0/LookupPlayerTournaments?apikey='+api_key+'&playerid=1000&offset=100'
q = requests.get(url4)
js2 = q.text
playerdf = pd.read_json(js2)
playerdf['PlayerId']=1000
playerdf.to_csv('tourney.csv',mode='a',header=False)

l = list(tt_df['iter'])
p = list(tt_df['PlayerId'])

url5 = 'http://api.esportsearnings.com/v0/LookupPlayerTournaments?apikey='+api_key+'&playerid='
offset = '&offset='
for i in np.arange(10,11):
    for j in range(l[i]+1):
        url = url5 + p[i] + offset + str(j*100)
        r = requests.get(url)
        js3 = r.text
        plr_df = pd.read_json(js3)
        plr_df['PlayerId]']=p[i]
        plr_df.to_csv('tourney.csv', mode='a', header=False)
        print(str(p[i])+'entered')
        time.sleep(2)

master_df =pd.read_csv('tourney.csv')
master_df.drop_duplicates

i = master_df['PlayerId']
i = master_df.PlayerId.astype(str)
list(i)

i = p_df['KL'][1].lower()
extracturl = urlopen('https://www.esportsearnings.com/players/'+i+'/team-history')
soup = BeautifulSoup(extracturl, 'html.parser')
b = soup.select('div.format_cell.info_text_value')[1]
dob = str(b.contents)
# print(dob)
soup2 = soup.select('table')
soup3 = soup2[0].select('td.detail_list_date')
soup4 = soup2[0].select('td.detail_list_player')
print(soup4[1])
d = {}
for i in range(len(soup3)):
    s4 = str(soup4[i].contents)
    soup4 = BeautifulSoup(s4,'lxml').text
    d[soup4] = str(soup3[i].contents)

player_data = {}
player_data['dob']=str(dob)
player_data['team_info']=d
df_blah = pd.DataFrame(player_data)
df_blah.to_csv('blah.csv')
df_blah.to_json('blah.json')


json_list = []
for i in range(p_df.shape[0]):
    if p_df['CountryCode'][i] in ['kr','jp','cn']:
        k = p_df['KL'][i].lower()
    else:
        k = p_df['Key'][i].lower()
    try:
        url = 'https://www.esportsearnings.com/players/'+k+'/team-history'
        urlop = requests.get(url)
        soup = BeautifulSoup(urlop.text, 'lxml')
        soup2 = soup.select('table')
        soup3 = soup2[0].select('td.detail_list_date')
        soup4 = soup2[0].select('td.detail_list_player')
        j = {}
        j["PlayerId"] = str( p_df['PlayerId'][i])
        d = []
        for i in range(len(soup3)):
            s4 = soup4[i].text
            s = {}
            s["team"]= s4
            s["history"] = parser(str(soup3[i].contents))
            d.append(s)
        j["team_history"] = d
        json_list.append(j)
        print(j["PlayerId"])
        time.sleep(2)
    except:
        time.sleep(2)
with open("thisbetterwork.json", "a") as data:
    data.write(json.dumps(json_list))

with open('team_dump.json', 'w') as f:
  json.dump(json_list, f)

j = {}
j['PlayerId'] = p_df['PlayerId'][i]
d = {}
for i in range(len(soup3)):
    s4 = str(soup4[i].contents)
    d[s4] = str(soup3[i].contents)
j['history'] = d
dfi = pd.DataFrame(j)

dfi.to_csv('blah.csv')

k = p_df['KL'][0].lower()
url = 'https://www.esportsearnings.com/players/'+k+'/team-history'
urlop = requests.get(url)
soup = BeautifulSoup(urlop.text, 'lxml')
soup2 = soup.select('table')
soup3 = soup2[0].select('td.detail_list_date')
soup4 = soup2[0].select('td.detail_list_player')
j = {}
j["PlayerId"] = str( p_df['PlayerId'][0])
d = []
for i in range(len(soup3)):
    s4 = soup4[i].text
    s = {}
    s["team"]= s4
    s["history"] = parser(str(soup3[i].contents))
    d.append(s)
j["team_history"] = d
json_string = json.dumps(j)
print(j["PlayerId"])

def parser(a):
    a = str(a).split("⇒")
    if len(a) == 1:
        soupy = BeautifulSoup(str(a).split(':')[0],'lxml')
        q = (soupy.p.text)
        j=[0,0]
        i = "[']"
        r = q.split(' ')[1].strip(i)
        j[0] = r[0:10]
#         print(j[0])
        j[1] = str(np.datetime64('2020-10-10'))
    else:
        a = [x.strip("['], ") for x in a]
        j = a
        for i in range(len(a)):
            if len(a[i])>10:
                soup = BeautifulSoup(a[i], 'lxml')
                k= soup.span.text
                if k == '<unknown>':
                    k = '2004-01-01'
                j[i] =k
    j = [str(np.datetime64(x)) for x in j]
    return j
